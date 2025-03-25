import os
import concurrent.futures

# Set required environment variable
os.environ["PYNGUIN_DANGER_AWARE"] = "YES"

# Base path of your project
project_path = "."

# Directory containing all 'dp' modules
dp_dir = os.path.join(project_path, "algorithms", "dp")

# Output directory for generated tests
output_dir = "generated_tests"

# Find all Python modules inside algorithms/dp/
modules = []
for root, _, files in os.walk(dp_dir):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            module = os.path.splitext(os.path.relpath(os.path.join(root, file), project_path))[0]
            module = module.replace(os.sep, ".")
            modules.append(module)

def run_pynguin(module):
    print(f"Generating tests for: {module}")
    os.system(f"pynguin --project-path={project_path} --output-path={output_dir} --module-name={module}")

# Parallel execution
if __name__ == "__main__":
    max_workers = min(8, len(modules))  # Adjust based on your CPU cores
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(run_pynguin, modules)
