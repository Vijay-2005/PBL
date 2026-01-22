# Implementation and Evaluation of an Adaptive 5G Scheduler  
### (Comparison with Round Robin and Proportional Fair)

---

## 1. Project Motivation

In 5G New Radio (NR) systems, the scheduler at the gNB plays a critical role in determining system performance by allocating radio resources to multiple users. Classical scheduling algorithms such as **Round Robin (RR)** and **Proportional Fair (PF)** are widely used in academic and industrial studies. However, these schedulers have notable limitations:

- **Round Robin** ensures fairness but ignores channel conditions and QoS requirements.
- **Proportional Fair** balances throughput and fairness but does not consider packet delay or service differentiation.

Modern 5G networks support **heterogeneous traffic** such as eMBB, URLLC, and mMTC, each with different QoS requirements. This motivates the need for a **more adaptive and QoS-aware scheduling approach**.

---

## 2. Project Objective

The primary objectives of this project are:

- To implement baseline 5G schedulers: **Round Robin (RR)** and **Proportional Fair (PF)**
- To design a **new adaptive QoS-aware scheduler**
- To compare the performance of the proposed scheduler against RR and PF
- To evaluate improvements using a **Python-based simulation framework**

---

## 3. Technology Stack

### Programming Language
- **Python 3**

### Libraries
- **NumPy** – numerical computation
- **Matplotlib** – plotting and visualization
- **(Optional) SimPy** – discrete event simulation support

### Tools
- VS Code / PyCharm
- Git (for version control)

### Reason for Choosing Python
- Rapid prototyping of algorithms
- Easy visualization of results
- Ideal for algorithm-level evaluation of schedulers
- Widely accepted for academic simulations

---

## 4. System Model and Assumptions

- Single gNB (base station)
- Multiple UEs (10–50)
- Time-slotted system (1 ms Transmission Time Interval)
- Downlink scheduling
- Independent CQI values per UE per TTI
- Finite buffer queues at each UE

---

## 5. Traffic Model

The simulation considers mixed 5G traffic types:

| Traffic Type | Description | Delay Sensitivity | Priority |
|-------------|------------|------------------|----------|
| eMBB | High data rate | Medium | Medium |
| URLLC | Low latency | Very High | High |
| mMTC | Massive IoT | Low | Low |

Each UE is assigned a traffic type with corresponding QoS parameters.

---

## 6. Baseline Scheduling Algorithms

### 6.1 Round Robin (RR)
- Cyclic allocation of resources among UEs
- Ensures time-based fairness
- No awareness of channel quality or QoS

### 6.2 Proportional Fair (PF)
- Scheduling metric:
  
  \[
  M_i = \frac{CQI_i}{\overline{T}_i}
  \]

- Balances throughput and fairness
- Does not consider packet delay or service priority

---

## 7. Proposed Scheduler: Adaptive QoS-Aware Scheduler

### Key Idea
The proposed scheduler dynamically adapts resource allocation based on:
- Channel quality
- Past throughput
- Packet delay
- Service priority

### Scheduling Metric

\[
M_i = \alpha \cdot \frac{CQI_i}{\overline{T}_i}
+ \beta \cdot \frac{Delay_i}{Delay_{max}}
+ \gamma \cdot Priority_i
\]

Where:
- \(CQI_i\): Channel Quality Indicator
- \(\overline{T}_i\): Average past throughput
- \(Delay_i\): Head-of-line packet delay
- \(Priority_i\): Service class weight
- \(\alpha, \beta, \gamma\): Tunable weighting factors

### Advantages
- QoS-aware
- Delay-sensitive
- Fair and adaptive
- Suitable for mixed 5G traffic scenarios

---

## 8. Simulation Approach

### Execution Flow
1. Initialize UEs and traffic queues
2. Generate CQI values per TTI
3. Apply selected scheduling algorithm
4. Transmit data for scheduled UE
5. Update throughput, delay, and queue state
6. Repeat for total simulation duration

### Scheduler Comparison
- Same simulation environment
- Same traffic and channel conditions
- Fair and unbiased evaluation

---

## 9. Performance Metrics

The following metrics are used for evaluation:

- **Average Throughput**
- **Average Packet Delay**
- **Packet Loss Ratio**
- **Jain’s Fairness Index**
- **Spectral Efficiency**

---

## 10. Results and Evaluation

The performance of the proposed scheduler is compared with RR and PF using:
- Line plots
- Bar charts
- Tabular comparisons

Expected observations:
- Higher throughput than RR
- Lower delay than PF for URLLC traffic
- Comparable fairness
- Reduced packet loss

---

## 11. Project Outcomes

- Demonstrated limitations of classical schedulers
- Designed an adaptive scheduler aligned with 5G QoS requirements
- Developed a modular Python-based simulation framework
- Provided quantitative performance comparison through plots and metrics

---

## 12. Future Scope

- Integration of reinforcement learning for dynamic weight tuning
- Extension to multi-cell scenarios
- Validation using ns-3 or MATLAB 5G Toolbox
- Uplink scheduling analysis

---

## 13. Conclusion

This project presents a practical and extensible approach to 5G scheduling by introducing a QoS-aware adaptive scheduler. Through systematic simulation and comparison, the proposed method demonstrates improved performance for heterogeneous 5G traffic, making it suitable for modern wireless systems research.

---
