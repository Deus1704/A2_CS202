import pandas as pd
from collections import Counter

# List of file paths and repository names
files = {
    "Trafiltura": "trafilatura_analysis.txt",
    "Manim": "manim_analysis.txt",
    "OpenHands": "OpenHands_analysis.txt"
}

# Dictionary to store CWE frequency
cwe_counter = Counter()

# Loop through files and count unique CWEs per file
for repo_name, file_path in files.items():
    df = pd.read_csv(file_path, sep="\t")
    
    # Ensure CWE_IDS column exists
    if "CWE_IDS" in df.columns:
        unique_cwes = set()  # Store unique CWEs per file
        for cwe_list in df["CWE_IDS"].dropna():
            cwe_ids = {cwe.strip() for cwe in str(cwe_list).split(",")}  # Strip spaces & use a set
            unique_cwes.update(cwe_ids)  # Collect unique CWEs for this file

        # Update the global counter with the unique CWEs from this file
        cwe_counter.update(unique_cwes)

# Print the most common CWE IDs in a structured format
print("\nMost Frequent CWEs Across Repositories:")
print("=" * 40)
print(f"{'CWE ID':<10} | {'Occurrences':<10}")
print("-" * 40)

for cwe, count in cwe_counter.most_common(10):  # Show top 10
    print(f"CWE-{cwe:<7} | {count:<10}")

print("=" * 40)