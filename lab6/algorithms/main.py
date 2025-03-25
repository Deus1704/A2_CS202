import subprocess
import time
import re
import matplotlib.pyplot as plt

# Dictionary of pytest commands along with descriptions for different parallel modes
test_modes = {
    "Basic pytest": "pytest",
    "Process-based (n=1, load dist)": "pytest -n 1 --dist load",
    "Process-based (n=auto, load dist)": "pytest -n auto --dist load",
    "Thread-based (1 thread, load dist)": "pytest --parallel-threads 1 --dist load",
    "Thread-based (auto threads, load dist)": "pytest --parallel-threads auto --dist load",
    "Process-based (n=1, no dist)": "pytest -n 1 --dist no",
    "Process-based (n=auto, no dist)": "pytest -n auto --dist no",
    "Thread-based (1 thread, no dist)": "pytest --parallel-threads 1 --dist no",
    "Thread-based (auto threads, no dist)": "pytest --parallel-threads auto --dist no"
}

# Number of times each command will be executed
num_runs = 1

# List to store execution summaries
results_summary = []

def get_failure_info(test_output):
    """Parses test output to count failed test cases and list their names."""
    failed_cases = re.findall(r"FAILED (tests/\S+)", test_output)
    return len(failed_cases), failed_cases

print("\n=== Starting Parallel Execution Tests ===\n")

for description, test_cmd in test_modes.items():
    runtimes = []
    failure_totals = []
    failed_case_names = set()

    print(f"Executing: {description}")

    for attempt in range(num_runs):
        print(f"Attempt {attempt + 1}...")
        start_time = time.time()
        run_output = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
        end_time = time.time()

        duration = end_time - start_time
        failure_count, failure_names = get_failure_info(run_output.stdout + run_output.stderr)

        runtimes.append(duration)
        failure_totals.append(failure_count)
        failed_case_names.update(failure_names)

    avg_runtime = sum(runtimes) / num_runs
    avg_failure_rate = sum(failure_totals) / num_runs

    results_summary.append([description, avg_runtime, avg_failure_rate, failed_case_names])

    print(f"Average Time: {avg_runtime:.2f}s | Avg Failures: {avg_failure_rate:.2f}")
    print(f"Failed Tests Found: {failed_case_names if failed_case_names else 'None'}\n")

# Calculate relative speedup compared to baseline
baseline_runtime = results_summary[0][1] if results_summary else 1
for record in results_summary:
    record.append(baseline_runtime / record[1] if record[1] else 0)

# Writing results into a structured text report
output_file = "parallel_execution_report.txt"

with open(output_file, "w") as report:
    report.write("Execution Mode".ljust(40) + "| Avg Runtime (s)      | Avg Failures | Speedup | Failed Test Cases\n")
    report.write("=" * 130 + "\n")
    for record in results_summary:
        report.write(f"{record[0]:<40} | {record[1]:<18.2f} | {record[2]:<12.2f} | {record[4]:<7.2f} | {', '.join(record[3]) if record[3] else 'None'}\n")

print(f"Report successfully saved as '{output_file}'")

# Plotting
modes = [entry[0] for entry in results_summary]
avg_times = [entry[1] for entry in results_summary]
avg_failures = [entry[2] for entry in results_summary]
speedups = [entry[4] for entry in results_summary]

plt.figure(figsize=(12, 6))
plt.barh(modes, avg_times, color='skyblue')
plt.xlabel('Average Execution Time (seconds)')
plt.title('Execution Time by Parallelization Mode')
plt.tight_layout()
plt.savefig("execution_time_plot.png")
plt.show()

plt.figure(figsize=(12, 6))
plt.barh(modes, speedups, color='lightgreen')
plt.xlabel('Speedup Compared to Baseline')
plt.title('Speedup by Parallelization Mode')
plt.tight_layout()
plt.savefig("speedup_plot.png")
plt.show()

plt.figure(figsize=(12, 6))
plt.barh(modes, avg_failures, color='salmon')
plt.xlabel('Average Number of Failures')
plt.title('Failures by Parallelization Mode')
plt.tight_layout()
plt.savefig("failure_count_plot.png")
plt.show()
