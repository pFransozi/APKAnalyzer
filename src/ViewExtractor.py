import pandas as pd
import os
import numpy as np

class ViewExtractor():
    
    def __init__(self, feature_extractor_dir):
        self.feature_extractor_dir = feature_extractor_dir
        
    def _get_andropytool_feature_dir(self):
        return f"./{self.feature_extractor_dir}/Features_files/"
    
    def _get_apk_files(self, dir):
        return sorted(os.scandir(dir), key=lambda e: e.name)
    
    def _is_an_analysis_json_file(self, filename):
        return filename.endswith("-analysis.json")
    
    def _get_apk_hash(self, filename):
        return str(os.path.basename(filename)).split("-")[0]
    
    def read_model_column_list(self, filename_model):
        feature_names = []

        with open(filename_model, "r") as f:
            feature_names = [line.strip() for line in f]

        return feature_names
    
    def generate_models(self):
        api_features = self.read_model_column_list("../schemas/apicall-features.txt")
        opcodes_features = self.read_model_column_list("../schemas/opcodes-features.txt")
        perm_features = self.read_model_column_list("../schemas/perm-features.txt")

        api_dict = {feature:0 for feature in api_features}
        opcode_dict = {feature:0 for feature in opcodes_features}
        perm_dict = {feature:0 for feature in perm_features}


        return (api_dict, opcode_dict, perm_dict)
    

    def generate_permission_dict(self, json_permission):
        perm_dict = {}

        for permission in json_permission:

            if permission not in perm_dict:
                perm_dict[permission] = 1
            else:
                perm_dict[permission] = perm_dict[permission] + 1

        return perm_dict
    
    def extract_views(self):

        files = self._get_apk_files(self._get_andropytool_feature_dir())
        apks = {}

        for file in files:

            if not self._is_an_analysis_json_file(file.name):
                continue

            views = {}

            apk_hash = self._get_apk_hash(file.name)
            pd_json = pd.read_json(file.path)

            opcodes = pd_json["Static_analysis"]["Opcodes"]
            apicalls = pd_json["Static_analysis"]["API calls"]
            permissions = self.generate_permission_dict(pd_json["Static_analysis"]["Permissions"])


            api_model, opcode_model, perm_model = self.generate_models()

            for feature, value in opcodes.items():
                if feature in opcode_model:
                    opcode_model[feature] = value if feature in opcode_model else 0

            for feature, value in apicalls.items():
                if feature in api_model:
                    api_model[feature] = value if feature in api_model else 0

            for feature, value in permissions.items():
                if feature in perm_model:
                    perm_model[feature] = value if feature in perm_model else 0

            views["opcodes"]  = np.array(list(opcode_model.values())).reshape(-1, len(opcode_model))
            views["apicalls"]  = np.array(list(api_model.values())).reshape(-1, len(api_model))
            views["perm"]  = np.array(list(perm_model.values())).reshape(-1, len(perm_model)) 

            apks[apk_hash] = views

        
        return apks
