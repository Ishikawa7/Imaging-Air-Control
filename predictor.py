import pickle
import pandas as pd
class Predictor:
    model = pickle.load(open('predictor.pkl', 'rb'))

    @staticmethod
    def predict(status_dict):
        return Predictor.model.predict(pd.DataFrame([status_dict.values()], columns=status_dict.keys()))[0][0]
    
    @staticmethod
    def predict_n_steps(status_dict, n_steps):
        predictions = []
        for i in range(n_steps):
            status_dict["CO(mg/m^3)"] = Predictor.predict(status_dict)
            predictions.append(status_dict["CO(mg/m^3)"])
        return predictions