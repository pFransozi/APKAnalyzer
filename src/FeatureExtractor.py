import subprocess
import sys
import os


class FeatureExtractor():
    
    
    def __init__(self, apk_dir):
        self.apk_dir = apk_dir
    
    
    
    def get_absolute_path(self, relative_path):
        return os.path.abspath(relative_path)
        
    def _run_andropytool(self):
        
        abs_path = self.get_absolute_path(self.apk_dir)
        # Defina o comando para executar o AndroPyTool
        command = ["docker", "run", "--volume", f"{abs_path}:/apks", "alexmyg/andropytool",  "-s", "/apks/", "-fw"]

        # Execute o comando
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the AndroPyTool: {e}")
            sys.exit(1)
        
    def feature_extractor(self):
        print("Starting feature extractor...")
        
        self._run_andropytool()
        
        print("Feature extractor completed.")