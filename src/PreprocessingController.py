import joblib

class PreprocessingController():
    
    def normalize_pca(self, apks):

        apicalls_scaler = joblib.load("../dumps/apicalls_minMaxScaler.pkl")
        apicalls_pca = joblib.load("../dumps/apicalls_pca.pkl")

        opcodes_scaler = joblib.load("../dumps/opcodes_minMaxScaler.pkl")
        opcodes_pca = joblib.load("../dumps/opcodes_pca.pkl")

        perm_scaler = joblib.load("../dumps/perm_minMaxScaler.pkl")
        perm_pca = joblib.load("../dumps/perm_pca.pkl")

        for hash_key in apks:

            apk_opcodes = apks[hash_key]["opcodes"]
            apk_apicalls = apks[hash_key]["apicalls"]
            apk_perm = apks[hash_key]["perm"]


            apk_opcodes = opcodes_scaler.transform(apk_opcodes)
            apk_apicalls = apicalls_scaler.transform(apk_apicalls)
            apk_perm = perm_scaler.transform(apk_perm)

            apk_opcodes = opcodes_pca.transform(apk_opcodes)
            apk_apicalls = apicalls_pca.transform(apk_apicalls)
            apk_perm = perm_pca.transform(apk_perm)

            apks[hash_key]["opcodes"] = apk_opcodes
            apks[hash_key]["apicalls"] = apk_apicalls
            apks[hash_key]["perm"] = apk_perm

        return apks
    
    def selection_features(self, apks):

        # apicall range(100)
        # opcodes range(100, 200)
        # perm range(200, 300)

        feature_selection_dt = joblib.load("../dumps/feature-selection-dt.pkl")
        feature_selection_rf = joblib.load("../dumps/feature-selection-rf.pkl")
        feature_selection_knn = joblib.load("../dumps/feature-selection-knn.pkl")

        for apk in apks:

            features_selection = {}

            opcodes = apks[apk]["opcodes"][0]
            apicalls = apks[apk]["apicalls"][0]
            perm = apks[apk]["perm"][0]


            # dt for each view
            indices_keep = [i for i in range(100) if feature_selection_dt[i] >= 0.5]
            features_selection["apicalls_dt"] = apicalls[indices_keep].reshape(1, -1)
            indices_keep = [i - 100 for i in range(100, 200) if feature_selection_dt[i] >= 0.5]
            features_selection["opcodes_dt"] = opcodes[indices_keep].reshape(1, -1)
            indices_keep = [i - 200 for i in range(200, 300) if feature_selection_dt[i] >= 0.5]
            features_selection["perm_dt"] = perm[indices_keep].reshape(1, -1)

            # rf for each view
            indices_keep = [i for i in range(100) if feature_selection_rf[i] >= 0.5]
            features_selection["apicalls_rf"] = apicalls[indices_keep].reshape(1, -1)
            indices_keep = [i - 100 for i in range(100, 200) if feature_selection_rf[i] >= 0.5]
            features_selection["opcodes_rf"] = opcodes[indices_keep].reshape(1, -1)
            indices_keep = [i - 200 for i in range(200, 300) if feature_selection_rf[i] >= 0.5]
            features_selection["perm_rf"] = perm[indices_keep].reshape(1, -1)

            # knn for each view
            indices_keep = [i for i in range(100) if feature_selection_knn[i] >= 0.5]
            features_selection["apicalls_knn"] = apicalls[indices_keep].reshape(1, -1)
            indices_keep = [i  - 100 for i in range(100, 200) if feature_selection_knn[i] >= 0.5]
            features_selection["opcodes_knn"] = opcodes[indices_keep].reshape(1, -1)
            indices_keep = [i - 200 for i in range(200, 300) if feature_selection_knn[i] >= 0.5]
            features_selection["perm_knn"] = perm[indices_keep].reshape(1, -1)

            apks[apk]["features_selection"] = features_selection

        return apks
    
    def preprocessing(self, apks):
        
        print("Starting preprocessing...")
        
        print("Normalizing features and reducing dimensionality...")
        apks = self.normalize_pca(apks)
        print("Features normalized and dimensionality reduced.")
        print("Selecting features...")
        apks = self.selection_features(apks)
        print("Features selected.")
        
        return apks