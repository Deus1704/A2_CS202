import pandas as pd
import matplotlib.pyplot as plt

# Repository file mapping
repos = {
    "Trafiltura": "trafilatura_analysis.txt",
    "Manim": "manim_analysis.txt",
    "OpenHands": "OpenHands_analysis.txt"
}

# Create subplots for each repository
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Trend of High Severity Vulnerabilities Over Time", fontsize=16)

# Plot for each repository
for ax, (repo, file) in zip(axes, repos.items()):
    data = pd.read_csv(file, sep="\t")
    data["Time"] = range(len(data), 0, -1)  # Older commits on the left
    
    ax.plot(data["Time"], data["HIGH_1"], color="red", linewidth=2)
    ax.set_title(repo, fontsize=12)
    ax.set_xlabel("Time (Older → Newer)")
    ax.set_ylabel("High Severity Count")
    ax.invert_xaxis()
    ax.grid(True)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("high_severity_trend_three_repos.png")
plt.show()
