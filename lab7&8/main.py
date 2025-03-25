import os
import subprocess
import statistics

# Step 1: Clone repository
REPO_URL = "https://github.com/keon/algorithms.git"
REPO_DIR = "algorithms"

# Get the latest commit hash
os.chdir(REPO_DIR)
commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
print(f"Current commit hash: {commit_hash}")


# Step 3a: Sequential Execution
def run_tests_sequentially():
    times = []
    flaky_tests = set()
    print(f"current dir={os.getcwd()}")
    for _ in range(5):
        result = subprocess.run(["python", "-m", "pytest"], capture_output=True, text=True)
        # print(result.stdout)
        output = result.stdout
        failed_tests = set([line.split("::")[-1] for line in output.split("\n") if "FAILED" in line])
        # print(output.split("\n"))
        if failed_tests:
            # print(f"Flaky/Failing Tests: {failed_tests}")
            flaky_tests.update(failed_tests)
        nah = output.split("s\n")[-1].split(" ")[-2].rstrip('s')
        print(f"this->{nah}")
        execution_time = float(nah)
        times.append(execution_time)

    # Remove flaky tests
    print(f"Removing flaky tests: {flaky_tests}")
    Tseq = statistics.mean(times)  # Average of last 5 runs
    return Tseq, flaky_tests

Tseq, flaky_tests = run_tests_sequentially()
print(f"The Tseq={Tseq} \n and the flaky tests identified:\n{flaky_tests}")
# Step 3b: Parallel Execution
def run_tests_parallel(n_workers=4, dist_mode="load"):
    times = []
    failed_tests = set()

    for _ in range(3):
        cmd = ["python", "-m", "pytest", f"-n={n_workers}", f"--dist={dist_mode}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        execution_time = float(output.split("s\n")[-1].split(" ")[-2].rstrip('s'))
        times.append(execution_time)
        print(f"Execution Time: {execution_time:.2f}s")
        failed_tests.update(set([line.split("::")[-1] for line in output.split("\n") if "FAILED" in line]))

    Tpar = statistics.mean(times)
    return Tpar, failed_tests

Tpar_load, failed_tests_load = run_tests_parallel("auto", "load")
Tpar_no, failed_tests_no = run_tests_parallel("auto", "no")

# Step 4: Speedup Calculation
speedup_load = Tseq / Tpar_load
speedup_no = Tseq / Tpar_no

print(f"Speedup (load mode): {speedup_load}")
print(f"Speedup (no mode): {speedup_no}")

# Step 5: Report
report = f"""
## Parallel Test Execution Analysis

**Repository:** {REPO_URL}  
**Commit Hash:** {commit_hash}  

### Sequential Execution
- Average Time: {Tseq:.2f}s

### Parallel Execution
| Mode  | Average Time (s) | Speedup Ratio | Flaky Tests identified due to paralleization |
|-------|-----------------|---------------|-------------|
| Load  | {Tpar_load:.2f}s | {speedup_load:.2f}x | {failed_tests_load} |
| No    | {Tpar_no:.2f}s   | {speedup_no:.2f}x  | {failed_tests_no} |

### Observations:
- Identified flaky tests due to parallelization.
- Potential issues with shared resources/timing dependencies.
- Suggestions for improving pytest’s parallel execution stability.
"""

with open("lab6_report.md", "w") as f:
    f.write(report)

print("Lab report saved as lab6_report.md")
