import pickle
class Predictor:
    model = pickle.load(open('linear_regressor_predictor.pkl', 'rb'))

    @staticmethod
    def predict(input):
        return Predictor.model.predict(input)
    
    @staticmethod
    def predict_n_steps(status_dict, n):
        predictions = []
        for i in range(n):
            input["CO(mg/m^3)"] = Predictor.predict(input)
            predictions.append(input["CO(mg/m^3)"])
        return predictions