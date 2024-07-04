import os
import shutil

class FinalProcessController():

    def clear_directory(self, directory_path):
        print("Starting the process of cleaning the directory...")

        # Check if the script is being run as root
        if os.geteuid() != 0:
            print("Operational file deletion operation aborted.")
            print("This script needs to be run as root.")
            return

        # Check if the directory exists
        if not os.path.exists(directory_path):
            print(f"The directory {directory_path} does not exist.")
            return

        # Traverse all files and folders within the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)  # Remove file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory and its contents
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        
        print("Directory successfully cleaned.")