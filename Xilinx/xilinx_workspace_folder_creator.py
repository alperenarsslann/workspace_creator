import os
import shutil
import subprocess
import argparse

Vivado = "Vivado"
Vitis = "Vitis"
HLS = "Hls"
Files = "Files"
Temp_Files = os.path.join("Files", "temp_files")
xsa_files = os.path.join("Files", "xsa_files")
Config_Files = os.path.join("Files", "config_files")
Library = "Library"
Includes = "Includes"
Docs = "Docs"
Scripts = "Scripts"
README = "README.md"
TEMPLATE_FILES = os.path.join("Files", "temp_files", "templates")


VIVADO_BAT = "C:\\Xilinx\\Vivado\\2024.2\\bin\\vivado.bat"
TCL_TEMPLATE = "C:\\Workspaces\\Python_workspace\\scripts\\workspace_creator\\Xilinx\\Tcls\\creating_project.tcl"
TEMPLATE_FILES_TO_COPY = "C:\\Workspaces\\Xilinx_workspace\\Files\\Helper_files\\Template_Files"

def main():
    parser = argparse.ArgumentParser(description="Create Xilinx workspace + run Vivado TCL.")
    parser.add_argument("--b", required=True, help="Base directory path")
    parser.add_argument("--name", required=True, help="Project name")
    args = parser.parse_args()

    base_directory = os.path.normpath(args.b)
    project_name = args.name

    folder_names = [
        Vivado, Vitis, Files, Temp_Files, xsa_files, Library, Includes,
        Docs, Scripts, HLS, Config_Files, TEMPLATE_FILES
    ]

    # Create folders
    for folder in folder_names:
        os.makedirs(os.path.join(base_directory, folder), exist_ok=True)

    # README
    readme_path = os.path.join(base_directory, README)
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Xilinx Workspace Folder Structure\n")

    # Copy TCL into workspace/Scripts so the workspace is self-contained
    workspace_tcl = os.path.join(base_directory, Scripts, "creating_project.tcl")
    shutil.copyfile(TCL_TEMPLATE, workspace_tcl)

    # Run Vivado batch with tclargs
    try:
        proc = subprocess.Popen(
    [VIVADO_BAT, "-mode", "tcl", "-source", workspace_tcl,
     "-tclargs", base_directory, project_name],
    cwd=base_directory
        )
        print("Vivado project created successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Vivado TCL script: {e}")
        return
    except FileNotFoundError:
        print("Vivado not found. Check VIVADO_BAT path.")
        return

    # Copy template files
    template_destination = os.path.normpath(os.path.join(base_directory, TEMPLATE_FILES))
    os.makedirs(template_destination, exist_ok=True)
    try:
        subprocess.run(["xcopy", TEMPLATE_FILES_TO_COPY, template_destination, "/E", "/I", "/Y"], check=True)
        print(f"Template files copied to: {template_destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying template files: {e}")

    print("Workspace created at:", base_directory)

if __name__ == "__main__":
    main()
