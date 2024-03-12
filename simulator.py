import pandas as pd
import numpy as np
from queue import Queue

class Simulator():
    people_thread_safe = Queue(maxsize=1)
    status_dict = {
        "CO(mg/m^3)": 0.015,
        "Volume(m^3)": 30,
        "N_people": 0,
        "Ambient-Air-Pump(L/min)": 680,
        "Ambient-Air-Pump_power(%)" : 0,
        "Ambient-Air-Pump_number": 0,
    }
    threshold = 10.305
    fault_active = False
    index = 0
        #CO(mg/m^3),Volume(m^3),N_people,Ambient-Air-Pump(L/min),Ambient-Air-Pump_power(%),Ambient-Air-Pump_number,CO(mg/m^3)_Dt
    predictions = [0 for i in range(10)]
    columns = ['CO(mg/m^3)', 'Volume(m^3)', 'N_people', 'Ambient-Air-Pump(L/min)', 'Ambient-Air-Pump_power(%)', 'Ambient-Air-Pump_number', 'CO(mg/m^3)_Dt']
    CO_log = []
    active = False

    @staticmethod
    def update_people(n_people):
        Simulator.people_thread_safe.put(n_people)
        Simulator.status_dict["N_people"] = Simulator.people_thread_safe.get()
    
    @staticmethod
    def simulate_time_step():
        return Simulator.status_dict
        #self.people_now = self.people_now
        #self.pump_power = self.optimize(self.predict(self.CO, self.pump_power))
        #df_new = self.modell_call(self.CO, self.volume, self.pumps_l_min, self.pump_power, self.n_pumps, self.index)
        #df_new['CO(mg/m^3)_final'] += (np.random.rand(1)[0]*2 -1)* 0.01 * df_new['CO(mg/m^3)_final']
        #self.CO = df_new['CO(mg/m^3)_final'].values[0]
        #self.df_sim = pd.concat([self.df_sim,df_new])
        #self.index += 1
