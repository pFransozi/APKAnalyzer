
import argparse

class ArgParserController():
    
    def __init__(self):
        parser = argparse.ArgumentParser(description="Process APK files.")
        parser.add_argument('path', type=str, help="Path to an APK file or directory containing APK files.")
        self.args = parser.parse_args()
        
    def get_path_arg(self):
        return self.args.path