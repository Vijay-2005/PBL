"""
Configuration parameters for 5G NR Scheduling Simulation
"""

# Simulation Parameters
NUM_UES = 20
SIMULATION_TIME = 1000  # TTIs (Transmission Time Intervals)
TTI_DURATION = 1  # ms
BANDWIDTH = 20  # MHz
NUM_RBS = 100  # Resource Blocks

# Traffic Types
TRAFFIC_TYPES = {
    'eMBB': {'priority': 2, 'delay_threshold': 100, 'packet_size': 1500},
    'URLLC': {'priority': 3, 'delay_threshold': 10, 'packet_size': 200},
    'mMTC': {'priority': 1, 'delay_threshold': 1000, 'packet_size': 100}
}

# Channel Model
CQI_MIN = 1
CQI_MAX = 15
SNR_RANGE = (-5, 25)  # dB

# QoS-Aware Scheduler Weights
ALPHA = 0.4  # Channel quality weight
BETA = 0.4   # Delay weight
GAMMA = 0.2  # Priority weight

# Buffer Parameters
MAX_BUFFER_SIZE = 15000  # bytes (increased to reduce overflow)
PACKET_ARRIVAL_RATE = 0.5  # probability per TTI (reduced load)

# Output
VERBOSE = False
PLOT_RESULTS = True
