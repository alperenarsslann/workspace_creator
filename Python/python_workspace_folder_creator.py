import os
import subprocess
import argparse

# Define folder names
CONFIG = "config"
SRC = "src"
SERVICES = "services"
BUILD = "build"
TESTS = "tests"
UTILS = "utils"
CORE = "src/core"


# Files
README = "README.md"
MAIN_PY = "src/main.py"
APP_PY = "src/app.py"
ERROR_PY = "src/core/error_handler/error_handler.py"
YAML = "config/config.yaml"
REQUIREMENTS = "requirements.txt"


def main():
    #create a list of folder names to be created for Xilinx Workspace
    folder_names = [CONFIG, SRC, SERVICES, BUILD, TESTS, UTILS, CORE]
    file_names = [README, MAIN_PY, APP_PY, ERROR_PY, YAML, REQUIREMENTS]
    
    # Parse command line arguments for base directory
    parser = argparse.ArgumentParser(description="Create Xilinx workspace folder structure.")
    parser.add_argument("--b", required=True, help="Base directory path for the workspace")
    args = parser.parse_args()
    base_directory = args.b

    # Create the folders
    for folder_name in folder_names:
        os.makedirs(os.path.join(base_directory, folder_name), exist_ok=True)
    # Create the files
    for file_name in file_names:
        file_path = os.path.join(base_directory, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            pass
    
    # Initialize git in the base directory (entire workspace)
    try:
        subprocess.run(['git', 'init'], cwd=base_directory, check=True)
        print(f"Git repository initialized in: {base_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing git: {e}")
    except FileNotFoundError:
        print("Git is not installed or not found in the system PATH.")
    
    # Create a README file in the base directory
    readme_path = os.path.join(base_directory, README)
    app_py_path = os.path.join(base_directory, APP_PY)
    main_py_path = os.path.join(base_directory, MAIN_PY)

### WRITE AN README ###
    with open(readme_path, 'w') as readme_file:
        readme_file.write("# Python Workspace\n\nThis is the Python workspace folder structure.")

### WRITE AN APP.PY FILE ###
    with open(app_py_path, 'w') as app_py:
        pass

### WRITE AN INITIAL ARGUMENTS AND IMPORTS TO FILE ###
    with open(main_py_path, 'w') as main_py:
       main_py.write("#!/usr/bin/env python3\n\n")
       main_py.write("import sys\n\n")
       main_py.write("import os\n\n")
       main_py.write("from app import app\n\n")
       main_py.write("from core.error_handler import handle_error\n\n")
       main_py.write("# Add additional imports here\n\n")
       main_py.write("def main():\n")
       main_py.write("    print('Hello, World!')\n\n")
       main_py.write("if __name__ == '__main__':\n")
       main_py.write("    main()\n")
    

    print("Python workspace folder structure created successfully at:", base_directory)


if __name__ == "__main__":
    main()