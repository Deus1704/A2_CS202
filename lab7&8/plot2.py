import pandas as pd
import matplotlib.pyplot as plt

# List of file paths and repository names
files = {
    "Trafiltura": "trafilatura_analysis.txt",
    "Manim": "manim_analysis.txt",
    "OpenHands": "OpenHands_analysis.txt"
}

# Create subplots (1x3 layout)
fig, axes = plt.subplots(1, 3, figsize=(20, 8))
fig.suptitle("Time vs. Severity Levels Across Repositories", fontsize=14)

# Loop through files and plot on subplots
for ax, (repo_name, file_path) in zip(axes.flat, files.items()):
    # Load data
    df = pd.read_csv(file_path, sep="\t")
    
    # Reverse row index to represent time
    df["Time"] = range(len(df), 0, -1)
    
    # Extract relevant columns
    time = df["Time"]
    high_severity = df["HIGH_1"]
    med_severity = df["MED_1"]
    low_severity = df["LOW_1"]

    # Plot all severities
    ax.plot(time, high_severity, linestyle="-", color="red", label="High Severity")
    ax.plot(time, med_severity,  linestyle="--", color="orange", label="Medium Severity")
    ax.plot(time, low_severity,  linestyle=":", color="blue", label="Low Severity")
    
    # Reverse X-axis
    ax.invert_xaxis()
    
    # Labels and title for each subplot
    ax.set_title(repo_name)
    ax.set_xlabel("Time (Older → Newer)")
    ax.set_ylabel("Severity Count")
    ax.legend()
    ax.grid(True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig("time_vs_severity_levels.png") 