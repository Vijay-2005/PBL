# Advanced Scheduling Algorithms

## Overview

This project implements five scheduling algorithms for 5G NR downlink, ranging from classical baselines to advanced QoS-aware approaches.

---

## 1. Round Robin (RR) - Baseline

**Type**: Time-based fairness

**Metric**: Cyclic allocation

**Characteristics**:
- Ensures equal time allocation to all UEs
- No channel awareness
- No QoS differentiation
- Simple and predictable

**Use Case**: Baseline comparison, fair time sharing

---

## 2. Proportional Fair (PF) - Baseline

**Type**: Throughput-fairness balanced

**Metric**: 
```
M_i = CQI_i / avg_throughput_i
```

**Characteristics**:
- Balances system throughput and user fairness
- Channel-aware scheduling
- No delay or QoS awareness
- Industry standard for non-QoS traffic

**Use Case**: Best-effort traffic, throughput optimization

---

## 3. Modified Largest Weighted Delay First (M-LWDF) - Advanced

**Type**: QoS-aware with delay prioritization

**Metric**:
```
M_i = priority_i × (delay_i / delay_threshold_i) × (CQI_i / avg_throughput_i)
```

**Characteristics**:
- Multiplicative combination of delay, priority, and channel quality
- Exponentially prioritizes packets approaching deadline
- Proven algorithm used in LTE/5G systems
- Balances QoS requirements with channel efficiency

**Advantages**:
- Strong delay performance for URLLC traffic
- Service differentiation through priority weights
- Channel-aware resource allocation
- Mathematically proven stability

**Use Case**: Mixed traffic with strict delay requirements

---

## 4. EXP Rule Scheduler - Advanced

**Type**: Exponential delay-based scheduling

**Metric**:
```
M_i = priority_i × exp(delay_ratio_i / τ) × (CQI_i / avg_throughput_i)
```

Where τ is a time constant (default: 10 TTI)

**Characteristics**:
- Exponential urgency function for delay-sensitive traffic
- Aggressive prioritization as packets approach deadline
- Tunable urgency through τ parameter
- Suitable for ultra-low latency requirements

**Advantages**:
- Excellent for URLLC with strict latency bounds
- Smooth transition from normal to urgent state
- Prevents deadline violations
- Maintains channel awareness

**Use Case**: Ultra-reliable low-latency communications (URLLC)

---

## 5. Hybrid Adaptive Scheduler - Novel

**Type**: Multi-phase adaptive scheduling

**Algorithm**:
```
Phase 1: Urgency Check
  IF delay_ratio > 0.7:
    urgency_score = delay_ratio × priority × CQI
    SELECT max(urgency_score)

Phase 2: Optimized Selection
  metric = (channel_efficiency^0.4) × (fairness_factor^0.2) × 
           (qos_factor^0.3) × (buffer_factor^0.1)
  SELECT max(metric)
```

**Characteristics**:
- Two-phase decision process
- Dynamic mode switching based on urgency
- Multi-objective optimization
- Adaptive to traffic conditions

**Components**:
1. **Channel Efficiency**: Instantaneous rate / average rate
2. **Fairness Factor**: System average / user average (penalizes high-throughput users)
3. **QoS Factor**: (1 + delay_ratio) × priority
4. **Buffer Factor**: Considers buffer occupancy

**Advantages**:
- Best overall balance across all metrics
- Prevents deadline violations through urgency mode
- Maintains fairness through explicit fairness factor
- Adapts to heterogeneous traffic dynamically
- Novel contribution combining multiple strategies

**Use Case**: Heterogeneous 5G networks with mixed eMBB, URLLC, and mMTC traffic

---

## Performance Comparison

| Scheduler | Throughput | Delay | Packet Loss | Fairness | Complexity |
|-----------|------------|-------|-------------|----------|------------|
| Round Robin | Medium | High | High | Excellent | Low |
| Proportional Fair | High | High | Medium | Good | Low |
| M-LWDF | Medium-High | Low | Low | Good | Medium |
| EXP Rule | Medium-High | Very Low | Low | Medium | Medium |
| Hybrid Adaptive | High | Low | Very Low | Excellent | High |

---

## Key Innovations in Hybrid Adaptive

1. **Urgency-First Approach**: Prevents deadline violations by checking urgency before optimization
2. **Multi-Factor Optimization**: Balances four key factors with empirically tuned exponents
3. **Dynamic Adaptation**: Switches between urgency and optimization modes automatically
4. **Fairness Awareness**: Explicitly penalizes users with high historical throughput
5. **Buffer-Aware**: Considers queue state to prevent buffer overflow

---

## Configuration

Scheduler parameters can be tuned in `config.py`:

```python
# M-LWDF and Hybrid Adaptive use traffic-specific priorities
TRAFFIC_TYPES = {
    'eMBB': {'priority': 2, 'delay_threshold': 100},
    'URLLC': {'priority': 3, 'delay_threshold': 10},
    'mMTC': {'priority': 1, 'delay_threshold': 1000}
}
```

For EXP Rule, adjust the time constant:
```python
# In schedulers.py - EXPRuleScheduler.__init__()
self.tau = 10  # Lower = more aggressive urgency
```

For Hybrid Adaptive, adjust urgency threshold:
```python
# In schedulers.py - HybridAdaptiveScheduler.__init__()
self.urgency_threshold = 0.7  # 70% of delay threshold
```

---

## References

- M-LWDF: Andrews et al., "Providing Quality of Service over a Shared Wireless Link"
- EXP Rule: Shakkottai & Stolyar, "Scheduling for Multiple Flows Sharing a Time-Varying Channel"
- Hybrid Adaptive: Novel contribution of this project
