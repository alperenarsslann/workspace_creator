import os
import subprocess
import argparse

# Define base name of the directory to be created
Folders = ["Files", 
           "Scripts", 
           "Temp_files", 
           "Docs", 
           "Trash_files", 
           "Zip_files", 
           "Library", 
           "Include"]
Files = ["README.md", ".gitignore", "LICENSE"]


def creating_folders(base_path):
    for folder in Folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

def creating_files(base_path):
    for file in Files:
        file_path = os.path.join(base_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")
    

def initialize_git(base_path):
    try:
        subprocess.run(['git', 'init'], cwd=base_path, check=True)
        print(f"Git repository initialized in: {base_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing git: {e}")
    except FileNotFoundError:
        print("Git is not installed or not found in the system PATH.")

def main():
    parser = argparse.ArgumentParser(description="Create workspace directories.")
    parser.add_argument("--b", help="Name of the workspace to create")
    args = parser.parse_args()
    if args.b:
        base_path = os.path.join(os.getcwd(), args.b)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            print(f"Created base directory: {base_path}")
        else:
            print(f"Base directory already exists: {base_path}")
        
        creating_folders(base_path)
        creating_files(base_path)
        initialize_git(base_path)
    else:
        print("Please provide a name for the workspace using --b argument.")

if __name__ == "__main__":
    main()