
import os
import shutil

class InitialProcessController():
    
    def is_apk_file(self, file_path):
        return file_path.lower().endswith('.apk')
    
    def copy_apk_file(self, file_path, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(dest_dir, file_name)
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, dest_path)
            print(f"Copied: {file_path} to {dest_path}")
        else:
            print(f"File already exists in destination: {dest_path}")

    def process_file(self, file_path, dest_dir):
        if self.is_apk_file(file_path):
            self.copy_apk_file(file_path, dest_dir)
        else:
            print(f"Error: {file_path} is not an APK file.")

    def process_directory(self, directory_path, dest_dir):
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_apk_file(file_path):
                    self.copy_apk_file(file_path, dest_dir)

    def process_args(self, path, dest_dir):
        print("Initializing file(s) copy process...")
        if os.path.isfile(path):
            self.process_file(path, dest_dir)
        elif os.path.isdir(path):
            self.process_directory(path, dest_dir)
        else:
            print(f"Error: {path} is neither a file nor a directory.")
        print("Files copied.")