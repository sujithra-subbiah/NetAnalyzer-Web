from flask import Flask, render_template
from scapy.all import sniff
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

packet_sizes = []

# -----------------------------
# Packet Capture Function
# -----------------------------
def capture_packets():
    global packet_sizes
    packet_sizes = []

    def process_packet(packet):
        packet_sizes.append(len(packet))

    sniff(count=20, prn=process_packet)

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/capture")
def capture():
    capture_packets()

    total_packets = len(packet_sizes)
    average_size = sum(packet_sizes) / total_packets if total_packets > 0 else 0

    # Save CSV inside static folder
    csv_path = os.path.join("static", "packets.csv")
    df = pd.DataFrame(packet_sizes, columns=["Packet Size"])
    df.to_csv(csv_path, index=False)

    # Save Graph
    graph_path = os.path.join("static", "graph.png")

    plt.figure()
    plt.plot(packet_sizes)
    plt.title("Packet Size Analysis")
    plt.xlabel("Packet Number")
    plt.ylabel("Packet Size (bytes)")
    plt.savefig(graph_path)
    plt.close()

    return render_template(
        "dashboard.html",
        total=total_packets,
        average=round(average_size, 2),
        graph=True
    )

if __name__ == "__main__":
    app.run(debug=True)