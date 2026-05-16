import subprocess
import json
import time
import math
import threading
import sys

def get_gyro_samples(num_samples=50):
    """Capture raw gyroscope readings via Termux API."""
    try:
        # Call the sensor and request a specific number of samples
        result = subprocess.check_output(
            ["termux-sensor", "-s", "Gyroscope", "-n", str(num_samples)],
            text=True
        )
        data = json.loads(result)

        magnitudes = []  
        # Extract the 3D vectors (X, Y, Z) and calculate the overall vibration magnitude  
        for entry in data.get('Gyroscope', []):  
            values = entry.get('values', [0, 0, 0])  
            # Calculate the physical magnitude  
            mag = math.sqrt(values[0]**2 + values[1]**2 + values[2]**2)  
            magnitudes.append(mag)  
        return magnitudes  
    except Exception as e:  
        print(f"[!] Error communicating with sensor. Ensure Termux:API is installed.\nDetails: {e}")  
        return []

def cpu_stress():
    """Inject heavy computational load to increase CPU power consumption."""
    x = 1.0
    for _ in range(5000000):
        x = (x * 3.14159) ** 0.5

print("=" * 50)
print("[+] Starting Physical Eavesdropping Protocol (Gyroscope Side-Channel)")
print("=" * 50)

# 1. Idle State
print("\n[1] Measuring CPU pulse in Idle state...")
print("=> Please place the phone on a solid surface (table) and do not touch it.")
time.sleep(4) # Allow time for hand movement to settle
idle_samples = get_gyro_samples(50)

if not idle_samples:
    sys.exit()

# 2. Load State
print("\n[2] Injecting heavy computational load (simulating a wallet signature)...")

# Run the stress test in a separate thread so we can listen simultaneously
stress_thread = threading.Thread(target=cpu_stress)
stress_thread.start()

print("=> Measuring CPU pulse under physical load...")
load_samples = get_gyro_samples(50)
stress_thread.join()

# 3. Statistical Analysis of Mechanical Jitter (Variance)
def calculate_variance(samples):
    if not samples:
        return 0
    mean = sum(samples) / len(samples)
    return sum((x - mean) ** 2 for x in samples) / len(samples)

idle_var = calculate_variance(idle_samples)
load_var = calculate_variance(load_samples)

print("\n" + "=" * 50)
print("=== Physical Report ===")
print(f"Kinematic Variance (Idle) : {idle_var:.12f}")
print(f"Kinematic Variance (Load) : {load_var:.12f}")

if load_var > idle_var:
    diff = ((load_var - idle_var) / idle_var) * 100 if idle_var > 0 else 0
    print(f"\n[🚨 POSITIVE DETECTION] Excess mechanical vibration captured by {diff:.2f}%!")
    print("=> Physics doesn't lie. CPU vibration detected during computation.")
else:
    print("\n[🛡️ TOTAL SILENCE] No vibration detected. Either the sensor is software-limited (Low Polling Rate), or the motherboard is well-isolated.")

