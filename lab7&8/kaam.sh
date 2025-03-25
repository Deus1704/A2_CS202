#!/bin/bash

# Ensure Bandit with TOML support is installed
pip install --upgrade bandit[toml]

# Process each repo in repos.txt
while IFS= read -r repo || [ -n "$repo" ]; do
    echo "Processing repository: $repo"
    repo_dir=$(basename "$repo" .git)

    # Clone repository
    git clone "$repo" "$repo_dir" || { echo "Failed to clone $repo, skipping..."; continue; }
    cd "$repo_dir" || { echo "Could not enter directory $repo_dir, skipping..."; cd ..; continue; }

    # Get last 100 non-merge commits
    git log --no-merges -n 100 --pretty=format:"%H" > commits.txt || { echo "Git log failed, skipping..."; cd ..; continue; }

    # Create temp analysis script
    cat > temp.sh << 'EOL'
#!/bin/bash
mkdir -p bandit_output
while read commit || [ -n "$commit" ]; do
    git checkout "$commit" --quiet || { echo "Checkout failed for commit $commit"; continue; }
    bandit -r . -f json -o "./bandit_output/bandit_output_${commit}.json"
done < commits.txt
EOL

    chmod +x temp.sh
    ./temp.sh
    rm temp.sh  # Clean up the temporary script

    # Generate confidence report
    jq -r '
      ["COMMIT_CONFIDENCE", "HIGH_1", "MED_1", "LOW_1"] | @tsv,
      (inputs |
        [input_filename | capture("bandit_output_(?<commit>.*).json").commit] as $commit |
        .results |
        group_by(.issue_confidence) |
        map({
          key: (.[0].issue_confidence | sub("MEDIUM"; "MED")),
          value: length
        }) | from_entries |
        [$commit[], .HIGH//0, .MED//0, .LOW//0] | @tsv
      )
    ' bandit_output/bandit_output_*.json > confidence_report.tsv

    # Generate severity report
    jq -r '
      ["COMMIT_SEVERITY", "HIGH_2", "MED_2", "LOW_2"] | @tsv,
      (inputs |
        [input_filename | capture("bandit_output_(?<commit>.*).json").commit] as $commit |
        .results |
        group_by(.issue_severity) |
        map({
          key: (.[0].issue_severity | sub("MEDIUM"; "MED")),
          value: length
        }) | from_entries |
        [$commit[], .HIGH//0, .MED//0, .LOW//0] | @tsv
      )
    ' bandit_output/bandit_output_*.json > severity_report.tsv

    # Generate CWE report
    jq -r '
      ["COMMIT_CWES", "UNIQUE_CWES", "CWE_IDS"] | @tsv,
      (inputs |
        [input_filename | capture("bandit_output_(?<commit>.*).json").commit] as $commit |
        [.results[].issue_cwe | select(. != null and has("id"))? | .id] |
        unique as $cwes |
        [$commit[], ($cwes | length), ($cwes | join(", "))] | @tsv
      )
    ' bandit_output/bandit_output_*.json > cwe_report.tsv

    # Combine reports into a single analysis file
    paste confidence_report.tsv severity_report.tsv cwe_report.tsv > ../"${repo_dir}_analysis.txt"

    # Clean up repo
    cd .. || exit
    rm -rf "$repo_dir"

    echo "Completed analysis for $repo"
    echo "-----------------------------------------"

done < repos.txt
