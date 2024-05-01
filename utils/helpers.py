
import numpy as np

def calculate_stress(hrv, min_hrv, max_hrv, low_threshold, high_threshold):
    # Normalize HRV to a stress scale (0-100)
    normalized_hrv = (hrv - min_hrv) / (max_hrv - min_hrv) * 100
    # Define thresholds for stress levels
    if normalized_hrv < low_threshold:
        stress_level =  0   # Low
    elif low_threshold <= normalized_hrv <= high_threshold:
        stress_level = 1  #Moderate
    else:
        stress_level = 2 #High
    return stress_level





def calculate_sdnn(rr_intervals):
    # Step 1: Calculate mean of RR intervals
    mean_rr_interval = np.mean(rr_intervals)
    # Step 2: Calculate variance of RR intervals
    variance = np.mean((rr_intervals - mean_rr_interval) ** 2)
    # Step 3: Calculate SDNN
    sdnn = np.sqrt(variance)
    return sdnn
