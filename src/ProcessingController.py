import joblib

class ProcessingController():
    
    def predict(self, apks):

        dt_apicalls = joblib.load("../dumps/apicalls-dt-pca-las.pkl")
        dt_opcodes = joblib.load("../dumps/opcodes-dt-pca-las.pkl")
        dt_perm = joblib.load("../dumps/perm-dt-pca-las.pkl")

        knn_apicalls = joblib.load("../dumps/apicalls-knn-pca-las.pkl")
        knn_opcodes = joblib.load("../dumps/opcodes-knn-pca-las.pkl")
        knn_perm = joblib.load("../dumps/perm-knn-pca-las.pkl")

        rf_apicalls = joblib.load("../dumps/apicalls-rf-pca-las.pkl")
        rf_opcodes = joblib.load("../dumps/opcodes-rf-pca-las.pkl")
        rf_perm = joblib.load("../dumps/perm-rf-pca-las.pkl")


        for apk in apks:

            predict = {}

            dt_apicalls_prediction = dt_apicalls.predict(apks[apk]["features_selection"]["apicalls_dt"])
            dt_opcodes_prediction = dt_opcodes.predict(apks[apk]["features_selection"]["opcodes_dt"])
            dt_perm_prediction = dt_perm.predict(apks[apk]["features_selection"]["perm_dt"])

            predict["dt"] = 0 if dt_apicalls_prediction[0] + dt_opcodes_prediction[0] + dt_perm_prediction[0] < 2 else 1

            rf_apicalls_prediction = rf_apicalls.predict(apks[apk]["features_selection"]["apicalls_rf"])
            rf_opcodes_prediction = rf_opcodes.predict(apks[apk]["features_selection"]["opcodes_rf"])
            rf_perm_prediction = rf_perm.predict(apks[apk]["features_selection"]["perm_rf"])

            predict["rf"] = 0 if rf_apicalls_prediction[0] + rf_opcodes_prediction[0] + rf_perm_prediction[0] < 2 else 1

            knn_apicalls_prediction = knn_apicalls.predict(apks[apk]["features_selection"]["apicalls_knn"])
            knn_opcodes_prediction = knn_opcodes.predict(apks[apk]["features_selection"]["opcodes_knn"])
            knn_perm_prediction = knn_perm.predict(apks[apk]["features_selection"]["perm_knn"])

            predict["knn"] = 0 if knn_apicalls_prediction[0] + knn_opcodes_prediction[0] + knn_perm_prediction[0] < 2 else 1
            predict["total"] = 0 if predict["dt"] + predict["rf"] + predict["knn"] < 2 else 1

            apks[apk]["prediction"] = predict

        return apks
    
    def processing(self, apks):
        
        print("Starting prediction...")
        
        apks = self.predict(apks)
        
        print("Prediction done.")
        return apks





