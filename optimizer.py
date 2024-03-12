class Optimizer:
    @staticmethod
    def optimize(input):
        return input
    
    def search_threshold(self, power_min, power_max):
    # Check if input is valid
        if power_min >= power_max:
            raise ValueError("power_min must be less than power_max")
        # Define a constant for the threshold to stop the search
        THRESHOLD_DIFF = 5
        # Recursive search for the best threshold
        pred_power_min = self.predict(self.CO, power_min)
        pred_power_max = self.predict(self.CO, power_max)
        # Initialize thresholds
        num_thresholds = 10
        thresholds = np.full((1, num_thresholds), self.threshold) * 1.0
        
        sub_min = pred_power_min - thresholds
        sub_max = pred_power_max - thresholds
        
        sub_min[sub_min < 0] = 0
        sub_max[sub_max < 0] = 0
        
        absolute_min = np.abs(sub_min)
        absolute_max = np.abs(sub_max)
        
        sum_absolute_min = np.sum(absolute_min)
        sum_absolute_max = np.sum(absolute_max)
        
        if sum_absolute_min < sum_absolute_max:
            if power_max - power_min < THRESHOLD_DIFF:
                return power_min, pred_power_min
            else:
                return self.search_threshold(power_min, (power_min + power_max) // 2)
        else:
            if power_max - power_min < THRESHOLD_DIFF:
                return power_max, pred_power_max
            else:
                return self.search_threshold((power_min + power_max) // 2, power_max)
    
    def optimize(self, predictions):
        #print("CALL OPTIMIZE")
        best_pump_power = self.pump_power
        best_result = 9999
        best_predictions = 0
        for power in [0, 25, 50, 60, 65, 70, 75, 80, 85, 90, 95, 100]:
            predictions = self.predict(self.CO, power)
            thresholds = np.full((1, 10), self.threshold) * 1.0
            sub = predictions - thresholds
            # divide negative values by 10
            sub[sub < 0] = sub[sub < 0] * 0.0
            absolute = np.abs(sub)
            sum_absolute = np.sum(absolute)
            if sum_absolute < best_result:
                best_result = sum_absolute
                best_pump_power = power
                best_predictions = predictions
        self.predictions = best_predictions.flatten()
        #best_pump_power, best_predictions = self.search_threshold(0, 100)
        #self.predictions = best_predictions.flatten()
        return best_pump_power