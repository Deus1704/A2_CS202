mkdir -p bandit_output
while read commit; do
    # touch /bandit_output/bandit_output_${commit}.json
    git checkout $commit
    bandit -r . -f json -o ./bandit_output/bandit_output_${commit}.json
done < commits.txt


## "https://github.com/adbar/trafilatura.git"