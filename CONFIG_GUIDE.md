# Configuration Guide - Understanding config.py

This file explains every parameter in `config.py`, what it represents, and how changing it impacts your simulation results.

---

## 1. Simulation Parameters

### `NUM_UES = 20`
**What it is**: Number of User Equipment (phones/devices) in the simulation

**Impact**:
- **Increase (e.g., 50)**: 
  - ✅ More realistic large-scale scenario
  - ❌ Higher congestion, more packet loss
  - ❌ Longer simulation time
  - 📊 Fairness becomes more important
  
- **Decrease (e.g., 10)**:
  - ✅ Less congestion, lower packet loss
  - ✅ Faster simulation
  - ❌ Less realistic
  - 📊 All schedulers perform better

**Recommended**: 20-30 for balanced testing

---

### `SIMULATION_TIME = 1000`
**What it is**: Duration of simulation in TTIs (milliseconds)

**Impact**:
- **Increase (e.g., 5000)**:
  - ✅ More statistically reliable results
  - ✅ Better captures long-term behavior
  - ❌ Takes longer to run
  
- **Decrease (e.g., 500)**:
  - ✅ Faster results
  - ❌ Less reliable statistics
  - ❌ May not capture scheduler behavior fully

**Recommended**: 1000-2000 for good balance

---

### `TTI_DURATION = 1`
**What it is**: Length of each time slot in milliseconds

**Impact**:
- Fixed at 1ms for 5G NR standard
- Don't change unless simulating different technology
- All delays are measured in multiples of this

---

### `BANDWIDTH = 20` and `NUM_RBS = 100`
**What it is**: System bandwidth and number of resource blocks

**Impact**:
- Currently not actively used in simplified model
- In advanced implementations, affects data rates
- Represents system capacity

---

## 2. Traffic Types - THE MOST IMPORTANT SECTION

### `TRAFFIC_TYPES` Dictionary

This defines the three types of 5G traffic. **This is crucial for QoS-aware schedulers!**

#### **eMBB (Enhanced Mobile Broadband)**
```python
'eMBB': {'priority': 2, 'delay_threshold': 100, 'packet_size': 1500}
```

**What it is**: Video streaming, web browsing, downloads

**Parameters**:
- **priority: 2** (Medium)
  - Change to 3: eMBB gets more resources (better video quality)
  - Change to 1: eMBB gets less (may buffer/lag)
  
- **delay_threshold: 100 ms**
  - Increase to 200: More tolerant (packets can wait longer)
  - Decrease to 50: Stricter (forces faster delivery)
  
- **packet_size: 1500 bytes**
  - Increase to 3000: Larger video chunks (more realistic HD streaming)
  - Decrease to 500: Smaller packets (lower quality)

**Impact on Results**:
- Higher priority → eMBB users get better throughput
- Higher threshold → Lower packet loss for eMBB
- Larger packets → Higher throughput but more buffer usage

---

#### **URLLC (Ultra-Reliable Low-Latency Communications)**
```python
'URLLC': {'priority': 3, 'delay_threshold': 10, 'packet_size': 200}
```

**What it is**: Self-driving cars, remote surgery, industrial automation

**Parameters**:
- **priority: 3** (Highest) - **CRITICAL!**
  - This is why QoS schedulers prioritize URLLC
  - Change to 2: URLLC loses advantage (dangerous!)
  - Keep at 3 for realistic 5G
  
- **delay_threshold: 10 ms** - **VERY STRICT!**
  - This is the key challenge for schedulers
  - Increase to 20: Easier to meet (less realistic)
  - Decrease to 5: Extremely challenging (real-time control)
  
- **packet_size: 200 bytes**
  - Small control messages
  - Increase to 500: Larger commands
  - Keep small for realistic URLLC

**Impact on Results**:
- **This is what separates good schedulers from bad ones!**
- M-LWDF, EXP Rule, Hybrid Adaptive excel here
- Round Robin and PF fail to meet 10ms deadline
- Lower threshold → Higher packet loss for bad schedulers

---

#### **mMTC (Massive Machine-Type Communications)**
```python
'mMTC': {'priority': 1, 'delay_threshold': 1000, 'packet_size': 100}
```

**What it is**: IoT sensors, smart meters, environmental monitoring

**Parameters**:
- **priority: 1** (Lowest)
  - Gets resources only when others don't need them
  - Change to 2: Better service for IoT
  
- **delay_threshold: 1000 ms** (Very relaxed)
  - Can wait a long time
  - Decrease to 500: Slightly more urgent
  
- **packet_size: 100 bytes**
  - Tiny sensor readings
  - Very small impact on system

**Impact on Results**:
- Lowest priority → Often starved by other traffic
- High threshold → Rarely drops packets
- Small packets → Minimal throughput impact

---

## 3. Channel Model

### `CQI_MIN = 1` and `CQI_MAX = 15`
**What it is**: Channel Quality Indicator range (signal strength scale)

**Impact**:
- CQI 1 = Very poor signal (150 bytes/TTI)
- CQI 15 = Excellent signal (2800 bytes/TTI)
- **Don't change** - this is 5G standard

**How it affects results**:
- PF scheduler heavily depends on CQI
- Higher CQI → User gets selected more often
- Channel-aware schedulers (PF, M-LWDF, Hybrid) benefit

---

### `SNR_RANGE = (-5, 25)`
**What it is**: Signal-to-Noise Ratio range in decibels

**Impact**:
- Currently not actively used (CQI is used instead)
- In advanced models, maps to CQI values
- Represents realistic wireless conditions

---

## 4. QoS-Aware Scheduler Weights

### `ALPHA = 0.4` (Channel quality weight)
**What it is**: How much the scheduler cares about signal quality

**Impact**:
- **Increase to 0.6**:
  - ✅ More throughput (uses good channels)
  - ❌ Less fair (ignores poor signal users)
  - 📊 PF-like behavior
  
- **Decrease to 0.2**:
  - ✅ More fair
  - ❌ Lower throughput
  - 📊 Less channel-aware

---

### `BETA = 0.4` (Delay weight)
**What it is**: How much the scheduler cares about packet delay

**Impact**:
- **Increase to 0.6**:
  - ✅ Lower delays (prioritizes waiting packets)
  - ❌ May sacrifice throughput
  - 📊 Better for URLLC
  
- **Decrease to 0.2**:
  - ✅ Higher throughput
  - ❌ Higher delays
  - 📊 Worse for URLLC

---

### `GAMMA = 0.2` (Priority weight)
**What it is**: How much the scheduler cares about traffic priority

**Impact**:
- **Increase to 0.4**:
  - ✅ Stronger QoS differentiation
  - ❌ Lower priority traffic starved
  - 📊 URLLC dominates
  
- **Decrease to 0.1**:
  - ✅ More equal treatment
  - ❌ Weaker QoS
  - 📊 Less differentiation

**Note**: These weights should sum to 1.0 for balanced behavior

---

## 5. Buffer Parameters - CRITICAL FOR PACKET LOSS

### `MAX_BUFFER_SIZE = 15000`
**What it is**: Maximum queue size per user in bytes

**Impact**:
- **Increase to 20000**:
  - ✅ Lower packet loss (more storage)
  - ❌ Higher delays (packets wait longer)
  - ❌ More memory usage
  - 📊 All schedulers show lower loss
  
- **Decrease to 10000**:
  - ✅ Lower delays (less queuing)
  - ❌ Higher packet loss (overflow)
  - 📊 Schedulers differentiate more

**Current value (15000)**: Good balance between loss and delay

---

### `PACKET_ARRIVAL_RATE = 0.5`
**What it is**: Probability of new packet arriving each TTI (0.0 to 1.0)

**Impact** - **THIS IS THE SYSTEM LOAD KNOB!**

- **Increase to 0.7** (70% load):
  - ❌ Higher congestion
  - ❌ More packet loss
  - ❌ Higher delays
  - 📊 Schedulers differentiate more (stress test)
  - 📊 Bad schedulers fail dramatically
  
- **Increase to 0.9** (90% load):
  - ❌ Extreme congestion
  - ❌ Very high packet loss (>80%)
  - 📊 Only best schedulers survive
  
- **Decrease to 0.3** (30% load):
  - ✅ Low congestion
  - ✅ Low packet loss
  - ✅ Low delays
  - 📊 All schedulers perform well (too easy)

**Current value (0.5)**: Moderate load, good for comparison

---

## 6. Output Parameters

### `VERBOSE = False`
**What it is**: Print detailed simulation progress

**Impact**:
- `True`: See every step (useful for debugging)
- `False`: Clean output (recommended for results)

---

### `PLOT_RESULTS = True`
**What it is**: Generate performance graphs

**Impact**:
- `True`: Show plots (recommended)
- `False`: Only print table (faster for batch runs)

---

## How to Tune for Different Scenarios

### Scenario 1: Stress Test (Find Best Scheduler)
```python
NUM_UES = 30
PACKET_ARRIVAL_RATE = 0.7
MAX_BUFFER_SIZE = 10000
```
**Result**: High congestion, clear winner emerges

---

### Scenario 2: Realistic 5G Network
```python
NUM_UES = 20
PACKET_ARRIVAL_RATE = 0.5
MAX_BUFFER_SIZE = 15000
TRAFFIC_TYPES = {
    'eMBB': {'priority': 2, 'delay_threshold': 100, 'packet_size': 1500},
    'URLLC': {'priority': 3, 'delay_threshold': 10, 'packet_size': 200},
    'mMTC': {'priority': 1, 'delay_threshold': 1000, 'packet_size': 100}
}
```
**Result**: Balanced, shows real-world performance

---

### Scenario 3: URLLC-Heavy (Autonomous Vehicles)
```python
# In simulator.py, change traffic distribution:
# 30% eMBB, 60% URLLC, 10% mMTC
TRAFFIC_TYPES = {
    'URLLC': {'priority': 3, 'delay_threshold': 5, 'packet_size': 200},  # Stricter!
}
```
**Result**: Delay becomes critical metric

---

### Scenario 4: Easy Mode (All Schedulers Succeed)
```python
NUM_UES = 10
PACKET_ARRIVAL_RATE = 0.3
MAX_BUFFER_SIZE = 20000
```
**Result**: Low differentiation, not useful for comparison

---

## Key Relationships

### Packet Loss is affected by:
1. **PACKET_ARRIVAL_RATE** ↑ → Loss ↑ (more traffic)
2. **MAX_BUFFER_SIZE** ↑ → Loss ↓ (more storage)
3. **NUM_UES** ↑ → Loss ↑ (more competition)
4. **delay_threshold** ↓ → Loss ↑ (stricter deadlines)

### Delay is affected by:
1. **PACKET_ARRIVAL_RATE** ↑ → Delay ↑ (more queuing)
2. **MAX_BUFFER_SIZE** ↑ → Delay ↑ (longer queues)
3. **BETA** ↑ → Delay ↓ (scheduler prioritizes delay)
4. **Scheduler choice** (biggest impact!)

### Throughput is affected by:
1. **ALPHA** ↑ → Throughput ↑ (channel-aware)
2. **packet_size** ↑ → Throughput ↑ (larger packets)
3. **Scheduler choice** (PF and Hybrid excel)

### Fairness is affected by:
1. **Scheduler choice** (RR best, EXP worst)
2. **ALPHA** ↓ → Fairness ↑ (less channel bias)
3. **GAMMA** ↓ → Fairness ↑ (less priority bias)

---

## Recommended Settings for Your Project

**For demonstrating Hybrid Adaptive superiority:**
```python
NUM_UES = 20
SIMULATION_TIME = 1000
PACKET_ARRIVAL_RATE = 0.5
MAX_BUFFER_SIZE = 15000
ALPHA = 0.4
BETA = 0.4
GAMMA = 0.2
```

**For stress testing:**
```python
NUM_UES = 30
PACKET_ARRIVAL_RATE = 0.7
MAX_BUFFER_SIZE = 12000
```

**For publication-quality results:**
```python
NUM_UES = 25
SIMULATION_TIME = 2000
PACKET_ARRIVAL_RATE = 0.6
```

---

## Summary

The `config.py` file is the **control panel** for your simulation:

- **Traffic Types**: Define QoS requirements (most important!)
- **Arrival Rate**: Controls system load (stress test knob)
- **Buffer Size**: Balances loss vs delay
- **Weights (α, β, γ)**: Tune scheduler behavior
- **Num UEs**: Scale of simulation

**Pro Tip**: Run multiple simulations with different `PACKET_ARRIVAL_RATE` values (0.3, 0.5, 0.7) to show how schedulers perform under light, medium, and heavy load!
