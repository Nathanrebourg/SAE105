import re
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import webbrowser
import os
from datetime import datetime
import markdown







def parse_text_file_to_dataframe(file_path):


    main_info_pattern = re.compile(
        r"(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+(?P<src>[\w\.\-]+)\.(?P<src_port>\w+)\s+>\s+(?P<dst>[\w\.\-]+)\.(?P<dst_port>\w+):\s+Flags\s+\[(?P<flags>[^\]]+)\],\s+seq\s+(?P<seq>[0-9:]+),\s+ack\s+(?P<ack>\d+),\s+win\s+(?P<win>\d+),\s+.*length\s+(?P<length>\d+)"
    )

    with open(file_path, "r") as file:
        file_content = file.read()

    rows = []
    for match in main_info_pattern.finditer(file_content):
        rows.append(match.groupdict())

    df = pd.DataFrame(rows)
    return df




def plot_packet_frequency(df, frame):


    df_copy = df.copy()
    df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], format='%H:%M:%S.%f')
    df_copy.set_index('timestamp', inplace=True)
    packet_frequency = df_copy.resample('S').size()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(packet_frequency.index, packet_frequency.values, marker='o', linestyle='-', color='red')
    ax.set_title('Packet Frequency Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Packets')
    ax.grid(True, linestyle='--', alpha=0.7)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)



def plot_ip_traffic_pie_chart(df, frame):

    ip_traffic = df['src'].value_counts() + df['dst'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(ip_traffic, labels=ip_traffic.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('IP Traffic Distribution')
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

root = tk.Tk()
root.title("Ma Fenêtre Tkinter")

# Création d'un frame pour le graphique
frame = ttk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Exemple de DataFrame pour les flags TCP
data = {'flags': ['S', 'A', 'P', 'S', 'F', 'A', 'R', 'S', 'A', 'P']}
df = pd.DataFrame(data)

def plot_tcp_flags(df, frame):
    """
    Plot a bar chart showing the frequency of TCP flags with their full names.
    """

    flag_translations = {
        '.': 'No Flags',
        'S': 'SYN (Synchronize)',
        'P': 'PSH (Push)',
        'F': 'FIN (Finish)',
        'R': 'RST (Reset)',
        'A': 'ACK (Acknowledgment)',
        'U': 'URG (Urgent)',
        'E': 'ECE (ECN-Echo)',
        'W': 'CWR (Congestion Window Reduced)'
    }



    # Split the flags string and count occurrences
    flag_counts = {}
    for flags in df['flags']:
        for flag in flags.split():
            full_name = flag_translations.get(flag, flag)
            if full_name in flag_counts:
                flag_counts[full_name] += 1
            else:
                flag_counts[full_name] = 1




    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(flag_counts.keys(), flag_counts.values())
    ax.set_title('TCP Flags Distribution')
    ax.set_xlabel('Flags')
    ax.set_ylabel('Frequency')
    


    plt.xticks(rotation=45, ha='right')
    


    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')


    plt.tight_layout()


    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)



def generate_markdown_and_html_report(df):
    """
    Generate a comprehensive network traffic analysis report in HTML format.
    """
    # Current timestamp for the report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Markdown content with reordered sections
    md_content = [
        "# Network Traffic Analysis Report",
        f"**Report Generated On**: {timestamp}\n",
        "---\n",
        "## Port Analysis\n",
        "### Common Destination Ports\n",
        df['dst_port'].value_counts().head().to_frame().to_markdown(),
        "\n### Common Source Ports\n",
        df['src_port'].value_counts().head().to_frame().to_markdown(),
        "\n---\n",
        "## TCP Flags Summary\n",
        df['flags'].value_counts().to_frame().to_markdown(),
        "\n---\n",
        "## Most Active IPs\n",
        "### Top Destination IPs\n",
        df['dst'].value_counts().head().to_frame().to_markdown(),
        "\n### Top Source IPs\n",
        df['src'].value_counts().head().to_frame().to_markdown(),
        "\n---\n",
        "## Overview\n",
        f"- **Total Packets Analyzed**: {len(df)}",
        "\n---\n",
        "## Full Data Table\n",
        df.to_markdown(),
    ]

    # Join markdown content
    md_content_str = "\n".join(md_content)

    # Convert markdown to HTML
    body_html = markdown.markdown(md_content_str, extensions=['tables'])

    # Updated CSS for a fresh appearance
    css_style = """
    <style>
      body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        margin: 20px;
        background: #f5f5f5;
        color: #333;
      }
      h1, h2, h3 {
        color: #2c3e50;
        border-bottom: 2px solid #16a085;
        padding-bottom: 5px;
      }
      h1 {
        text-transform: uppercase;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
      }
      th, td {
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
      }
      th {
        background: #1abc9c;
        color: white;
      }
      tr:nth-child(odd) {
        background: #ecf0f1;
      }
      tr:hover {
        background: #dcdde1;
      }
      code {
        background: #f4f4f4;
        padding: 2px 4px;
      }
    </style>
    """

    # Full HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Network Traffic Analysis</title>
      {css_style}
    </head>
    <body>
      {body_html}
    </body>
    </html>
    """

    # Save the HTML report to the user's home directory
    report_path = os.path.join(os.path.expanduser('~'), 'network_traffic_analysis_report.html')
    with open(report_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    return report_path









def display_dataframe(df):

    root = tk.Tk()
    root.title("Packet Analysis - Multi-Capture View")


    frame_top = tk.Frame(root)
    frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    frame_bottom = tk.Frame(root)
    frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



    tree = ttk.Treeview(frame_top, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    


    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    


    scrollbar = ttk.Scrollbar(frame_top, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(expand=True, fill=tk.BOTH)




    # Create button frame
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=5)





    # Define current view index
    views = [plot_packet_frequency, plot_ip_traffic_pie_chart, plot_tcp_flags]
    current_view = [0]  # Use a list to allow modification within nested functions



    def show_graph():
        plot_tcp_flags(df, frame)

    # Ajout d'un troisième bouton pour afficher le graphique
    button_show_graph = ttk.Button(root, text="Afficher le Graphique", command=show_graph)
    button_show_graph.pack()




    def export_to_csv():
        """
        Export the DataFrame to a CSV file.
        """
        export_file_path = asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export data as CSV"
        )
        if export_file_path:
            df.to_csv(export_file_path, index=False, sep=';', encoding='utf-8')
            tk.messagebox.showinfo("Success", "Data exported successfully!")



    def open_markdown_html_report():
        """
        Génère et ouvre le rapport HTML (issu du Markdown).
        """
        try:
            report_path = generate_markdown_and_html_report(df)
            webbrowser.open('file://' + os.path.abspath(report_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")




    # Create button frame with all buttons side by side
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=5)



    # Add buttons
    
    export_button = tk.Button(button_frame, text="Export to CSV", command=export_to_csv)
    export_button.pack(side=tk.LEFT, padx=5)
    
    report_button = tk.Button(button_frame, text="View Report On Browser", command=open_markdown_html_report)
    report_button.pack(side=tk.LEFT, padx=5)


    # Initial plot
    views[current_view[0]](df, frame_bottom)



    root.mainloop()







if __name__ == "__main__":
    file_path = askopenfilename(title="Select the text file with captures",
                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    

    if file_path:
        packet_df = parse_text_file_to_dataframe(file_path)
        display_dataframe(packet_df)


    else:
        print("No file selected")