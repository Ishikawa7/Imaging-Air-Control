import pandas as pd
import numpy as np
from queue import Queue
import pickle
from predictor import Predictor
from optimizer import Optimizer

class Simulator():
    people_thread_safe = Queue(maxsize=1)
    status_dict = {
        "CO(mg/m^3)": 0.2,
        "Volume(m^3)": 30,
        "N_people": 0,
        "Ambient-Air-Pump(L/min)": 680,
        "Ambient-Air-Pump_power(%)" : 0,
        "Ambient-Air-Pump_number": 0,
    }
    threshold = 5.150
    fault_active = False
    index = 0
    predictions = [0 for i in range(10)]
    columns = ['CO(mg/m^3)', 'Volume(m^3)', 'N_people', 'Ambient-Air-Pump(L/min)', 'Ambient-Air-Pump_power(%)', 'Ambient-Air-Pump_number', 'CO(mg/m^3)_Dt']
    CO_log = [status_dict["CO(mg/m^3)"]]
    active = False

    @staticmethod
    def update_people(n_people):
        Simulator.people_thread_safe.put(n_people)
        Simulator.status_dict["N_people"] = Simulator.people_thread_safe.get()
    
    @staticmethod
    def simulate_time_step():
        prediction_CO = Predictor.predict(Simulator.status_dict)
        prediction_CO += ((np.random.rand(1)[0]*2 -1)* 0.05 * 0.05)
        Simulator.predictions = Predictor.predict_n_steps(Simulator.status_dict, 10)
        Simulator.status_dict["Ambient-Air-Pump_power(%)"] = Optimizer.optimize_pump_power(Simulator.status_dict, Simulator.threshold)
        Simulator.CO_log.append(prediction_CO)
        Simulator.status_dict["CO(mg/m^3)"] = prediction_CO

