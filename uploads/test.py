import re
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from fpdf import FPDF
import os


# Fonction pour parser le fichier texte en DataFrame
def parse_text_file_to_dataframe(file_path):
    pattern = re.compile(
        r"(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+(?P<src>[\w\.\-]+)\.(?P<src_port>\w+)\s+>\s+(?P<dst>[\w\.\-]+)\.(?P<dst_port>\w+):\s+Flags\s+\[(?P<flags>[^\]]+)\],\s+seq\s+(?P<seq>[0-9:]+),\s+ack\s+(?P<ack>\d+),\s+win\s+(?P<win>\d+),\s+.*length\s+(?P<length>\d+)"
    )
    with open(file_path, "r") as file:
        rows = [match.groupdict() for match in pattern.finditer(file.read())]
    return pd.DataFrame(rows)


# Fonction pour exporter les données en Markdown
def export_to_markdown(df):
    markdown = df.to_markdown(index=False)
    file_path = asksaveasfilename(
        title="Save as Markdown",
        defaultextension=".md",
        filetypes=[("Markdown files", "*.md")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(markdown)
        messagebox.showinfo("Success", f"Markdown file saved at {file_path}")


# Fonction pour afficher et interagir avec les graphiques
def plot_graph_with_toolbar(frame, plot_function, df):
    for widget in frame.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_function(df, ax)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)


# Fonctions pour différents types de graphiques
def plot_packet_frequency(df, ax):
    df_copy = df.copy()
    df_copy["timestamp"] = pd.to_datetime(df_copy["timestamp"], format="%H:%M:%S.%f")
    df_copy.set_index("timestamp", inplace=True)
    packet_frequency = df_copy.resample("S").size()
    ax.plot(packet_frequency.index, packet_frequency.values, marker="o", linestyle="-")
    ax.set_title("Packet Frequency Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Packets")
    ax.grid(True)


def plot_ip_traffic_pie_chart(df, ax):
    ip_traffic = df["src"].value_counts() + df["dst"].value_counts()
    ax.pie(ip_traffic, labels=ip_traffic.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("IP Traffic Distribution")
    ax.axis("equal")


def plot_tcp_flags(df, ax):
    flag_translations = {
        ".": "No Flags",
        "S": "SYN (Synchronize)",
        "P": "PSH (Push)",
        "F": "FIN (Finish)",
        "R": "RST (Reset)",
        "A": "ACK (Acknowledgment)",
        "U": "URG (Urgent)",
        "E": "ECE (ECN-Echo)",
        "W": "CWR (Congestion Window Reduced)",
    }
    flag_counts = {}
    for flags in df["flags"]:
        for flag in flags.split():
            full_name = flag_translations.get(flag, flag)
            flag_counts[full_name] = flag_counts.get(full_name, 0) + 1
    bars = ax.bar(flag_counts.keys(), flag_counts.values())
    ax.set_title("TCP Flags Distribution")
    ax.set_xlabel("Flags")
    ax.set_ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{int(bar.get_height())}",
            ha="center",
            va="bottom",
        )


# Génération du rapport PDF
def generate_pdf_report(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Network Traffic Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Total Packets: {len(df)}", ln=True)
    pdf.cell(0, 10, f"Unique Source IPs: {df['src'].nunique()}", ln=True)
    pdf.cell(0, 10, f"Unique Destination IPs: {df['dst'].nunique()}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, "Top 5 Source IPs:", ln=True)
    pdf.set_font("Arial", size=10)
    for ip, count in df["src"].value_counts().head().items():
        pdf.cell(0, 10, f"{ip}: {count}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, "Top 5 Destination IPs:", ln=True)
    pdf.set_font("Arial", size=10)
    for ip, count in df["dst"].value_counts().head().items():
        pdf.cell(0, 10, f"{ip}: {count}", ln=True)
    report_path = os.path.join(
        os.path.expanduser("~"), "network_traffic_analysis_report.pdf"
    )
    pdf.output(report_path)
    messagebox.showinfo("PDF Generated", f"Report saved to {report_path}")


# Affichage principal de l'interface utilisateur
def display_dataframe(df):
    root = tk.Tk()
    root.title("Enhanced Packet Analysis Dashboard")
    root.geometry("1200x900")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    frame_top = tk.Frame(root)
    frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
    frame_graph = tk.LabelFrame(root, text="Graphs", padx=5, pady=5)
    frame_graph.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    tree = ttk.Treeview(frame_top, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(expand=True, fill=tk.BOTH)
    scrollbar = ttk.Scrollbar(frame_top, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    ttk.Button(
        button_frame, text="Export as PDF", command=lambda: generate_pdf_report(df)
    ).pack(side=tk.LEFT, padx=10)
    ttk.Button(
        button_frame,
        text="Export as Markdown",
        command=lambda: export_to_markdown(df),
    ).pack(side=tk.LEFT, padx=10)
    ttk.Button(
        button_frame,
        text="Packet Frequency",
        command=lambda: plot_graph_with_toolbar(frame_graph, plot_packet_frequency, df),
    ).pack(side=tk.LEFT, padx=10)
    ttk.Button(
        button_frame,
        text="IP Traffic Distribution",
        command=lambda: plot_graph_with_toolbar(
            frame_graph, plot_ip_traffic_pie_chart, df
        ),
    ).pack(side=tk.LEFT, padx=10)
    ttk.Button(
        button_frame,
        text="TCP Flags Distribution",
        command=lambda: plot_graph_with_toolbar(frame_graph, plot_tcp_flags, df),
    ).pack(side=tk.LEFT, padx=10)

    root.mainloop()


# Exécution principale
if __name__ == "__main__":
    file_path = askopenfilename(
        title="Select the text file with captures", filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        packet_df = parse_text_file_to_dataframe(file_path)
        display_dataframe(packet_df)
    else:
        print("No file selected")
