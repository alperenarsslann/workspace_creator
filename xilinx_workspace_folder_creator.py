import os
import subprocess


# Define folder names
Vivado = "Vivado"
Vitis = "Vitis"
HLS = "Hls"
Files = "Files"
Temp_Files = "Files/temp_files"
xsa_files = "Files/xsa_files"
Config_Files = "Files/config_files"
Library = "Library"
Includes = "Includes"
Docs = "Docs"
Scripts = "Scripts"
README = "README.md"
TEMPLATE_FILES = "Files/temp_files/templates"


TEMPLATE_FILES_TO_BE_COPIED_FROM_DIRECTORUY = "C:\\Workspaces\\Xilinx_workspace\\Files\\Helper_files\\Template_Files"

def main():
    #create a list of folder names to be created for Xilinx Workspace
    folder_names = [Vivado, Vitis, Files, Temp_Files, xsa_files, Library, Includes, Docs, Scripts, HLS, Config_Files, TEMPLATE_FILES]
    

    # Ask the directory from the user
    base_directory = input("Enter the path where you want to create the Xilinx workspace folders: ").strip()
    
    
    # Create the folders
    for folder_name in folder_names:
        os.makedirs(os.path.join(base_directory, folder_name), exist_ok=True)
    
    
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

    with open(readme_path, 'w') as readme_file:
        readme_file.write("# Xilinx Workspace Folder Structure\n")
        readme_file.write("This directory contains the standard folder structure for Xilinx projects.\n\n")
        readme_file.write("## Folder Descriptions:\n")
        readme_file.write("- **Vivado/**: Contains Vivado project files and related resources.\n")
        readme_file.write("- **Vitis/**: Contains Vitis project files and related resources.\n")
        readme_file.write("- **Files/**: General files related to the project.\n")
        readme_file.write("  - **Temp_files/**: Temporary files generated during the build process.\n")
        readme_file.write("  - **XSA_files/**: XSA (Xilinx Shell Archive) files for hardware platforms.\n")
        readme_file.write("- **Library/**: Custom libraries and IP cores used in the project.\n")
        readme_file.write("- **Includes/**: Header files and other include files for the project.\n")
        readme_file.write("- **Docs/**: Documentation related to the project.\n")

    print("Xilinx workspace folder structure created successfully at:", base_directory)


    # COPY TEMPLATE FILES TO THE TEMPLATE FILES DIRECTORY
    template_destination = os.path.normpath(os.path.join(base_directory, TEMPLATE_FILES))
    try:
        subprocess.run(['xcopy', TEMPLATE_FILES_TO_BE_COPIED_FROM_DIRECTORUY, template_destination, '/E', '/I', '/Y'], check=True)
        print(f"Template files copied to: {template_destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error copying template files: {e}")


if __name__ == "__main__":
    main()