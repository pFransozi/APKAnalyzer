import os
import subprocess
import sys
import pkg_resources
import importlib

class DependenciesChecker:

    def __init__(self):
        self.CONFIG_FILE = '.config'

    def _read_config(self):
        if not os.path.isfile(self.CONFIG_FILE):
            return False
        with open(self.CONFIG_FILE, 'r') as f:
            for line in f:
                if line.strip().lower() == 'check_dependencies=true':
                    return True
        return False

    def _write_config(self, value):
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(f'check_dependencies={str(value).lower()}')

    def _check_files_exist(self, file_paths):
        missing_files = [file for file in file_paths if not os.path.isfile(file)]
        if missing_files:
            print("The following files are missing:")
            for file in missing_files:
                print(file)
            sys.exit(1)
        else:
            print("All necessary files are present.")

    def _check_docker_image(self, image_name):
        try:
            result = subprocess.run(["docker", "images", "-q", image_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stdout.strip():
                print(f"Imagem Docker '{image_name}' está disponível.")
            else:
                print(f"Imagem Docker '{image_name}' não está disponível. Puxe a imagem para continuar.")
                sys.exit(1)
        except subprocess.CalledProcessError:
            print("Erro ao verificar a imagem Docker.")
            sys.exit(1)

    def _check_docker_installed(self):
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Docker is installed.")
        except FileNotFoundError:
            print("Docker not found. Please ensure Docker is installed and available in the system PATH.")
            sys.exit(1)
        except subprocess.CalledProcessError:
            print("Docker is not installed correctly or is not functioning properly. Please install Docker to proceed.")
            sys.exit(1)

    def _check_docker_without_sudo(self):
        try:
            result = subprocess.run(["docker", "info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print("Docker is configured to run without sudo.")
            else:
                print("Docker is not configured to run without sudo. Please configure Docker to run without sudo.")
                sys.exit(1)
        except subprocess.CalledProcessError:
            print("Failed to check if Docker is configured to run without sudo. Please configure Docker to run without sudo.")
            sys.exit(1)

    def _check_python_dependencies(self, dependencies):
        missing_deps = []
        for dep, version in dependencies.items():
            try:
                pkg_resources.require(f"{dep}>={version}")
                print(f"{dep} (>= {version}) is installed.")
            except pkg_resources.DistributionNotFound:
                missing_deps.append((dep, version))
            except pkg_resources.VersionConflict as e:
                print(f"Version conflict for {dep}: {e.report()}")
                missing_deps.append((dep, version))
        
        if missing_deps:
            print("The following Python dependencies are missing or have incorrect versions:")
            for dep, version in missing_deps:
                print(f"{dep} (>= {version})")
            sys.exit(1)
        else:
            print("All Python dependencies are installed.")


    def check_dependencies(self):
        files_to_check = ["../schemas/apicall-features.txt" 
                        , "../schemas/opcodes-features.txt"
                        , "../schemas/perm-features.txt"
                        , "../dumps/feature-selection-dt.pkl"
                        , "../dumps/feature-selection-knn.pkl"
                        , "../dumps/feature-selection-rf.pkl"
                        , "../dumps/apicalls-dt-pca-las.pkl"
                        , "../dumps/apicalls-knn-pca-las.pkl"
                        , "../dumps/apicalls-rf-pca-las.pkl"
                        , "../dumps/apicalls_minMaxScaler.pkl"
                        , "../dumps/apicalls_pca.pkl"
                        , "../dumps/opcodes-dt-pca-las.pkl"
                        , "../dumps/opcodes-knn-pca-las.pkl"
                        , "../dumps/opcodes-rf-pca-las.pkl"
                        , "../dumps/opcodes_minMaxScaler.pkl"
                        , "../dumps/opcodes_pca.pkl"
                        , "../dumps/perm-dt-pca-las.pkl"
                        , "../dumps/perm-knn-pca-las.pkl"
                        , "../dumps/perm-rf-pca-las.pkl"
                        , "../dumps/perm_minMaxScaler.pkl"
                        , "../dumps/perm_pca.pkl"]
        
        python_dependencies = {
            "joblib": "1.4.2",
            "numpy": "1.26.4",
            "pandas": "2.2.2",
            "scikit-learn": "1.4.0",
            "tabulate": "0.9.0"
        }
        docker_image = "alexmyg/andropytool:latest"

        check_deps = self._read_config()

        if not check_deps:

            print("Starting dependency checks...")
            print("Checking Docker installation...")
            self._check_docker_installed()
            print("Checked Docker installation.")
            
            print("Checking if Docker is configured to run without sudo...")
            self._check_docker_without_sudo()
            print("Checked if Docker is configured to run without sudo.")
            
            print("Checking Docker image...")
            self._check_docker_image(docker_image)
            print("Checked Docker image.")

            print("Checking required files...")
            self._check_files_exist(files_to_check)
            print("Checked required files.")

            print("Checking Python dependencies...")
            self._check_python_dependencies(python_dependencies)
            print("Checked Python dependencies.")

            self._write_config(True)
            print("All dependencies are met. The program can run.")
    