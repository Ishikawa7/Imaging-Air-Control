import numpy as np
import pandas as pd
from predictor import Predictor
class Optimizer:
    @staticmethod
    def optimize_pump_power(status_dict, threshold):
        # Recursive search for the best threshold
        status_dict_min = status_dict.copy()
        if status_dict["Ambient-Air-Pump_power(%)"] >=5:
            status_dict_min["Ambient-Air-Pump_power(%)"] -= 5

        status_dict_max = status_dict.copy()
        if status_dict["Ambient-Air-Pump_power(%)"] <= 95:
            status_dict_max["Ambient-Air-Pump_power(%)"] += 5

        pred_current_power = Predictor.predict_n_steps(status_dict, 10)
        pred_power_min = Predictor.predict_n_steps(status_dict_min, 10)
        pred_power_max = Predictor.predict_n_steps(status_dict_max, 10)

        thresholds = np.full((1, 10), threshold) * 1.0
        
        sub_current = pred_current_power - thresholds
        sub_min = pred_power_min - thresholds
        sub_max = pred_power_max - thresholds
        
        sub_current[sub_current < 0] = 0
        sub_min[sub_min < 0] = 0
        sub_max[sub_max < 0] = 0
        
        absolute_current = np.abs(sub_current)
        absolute_min = np.abs(sub_min)
        absolute_max = np.abs(sub_max)
        
        sum_absolute_current = np.sum(absolute_current)
        sum_absolute_min = np.sum(absolute_min)
        sum_absolute_max = np.sum(absolute_max)
        
        if sum_absolute_current <= sum_absolute_min and sum_absolute_current <= sum_absolute_max:
            if sum_absolute_current == sum_absolute_min:
                return status_dict_min["Ambient-Air-Pump_power(%)"]
            return status_dict["Ambient-Air-Pump_power(%)"]
        elif sum_absolute_min < sum_absolute_max:
            return Optimizer.optimize_pump_power(status_dict_min, threshold)
        else:
            return Optimizer.optimize_pump_power(status_dict_max , threshold)