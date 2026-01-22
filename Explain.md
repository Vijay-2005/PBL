# 5G Scheduling Algorithms - Simple Explanation

## What Are We Doing?

Imagine a 5G cell tower (base station) that needs to send data to 20 different phones. But here's the problem: **the tower can only send data to ONE phone at a time**. So every millisecond, it must decide: "Which phone should I send data to right now?"

This decision-making process is called **scheduling**, and different algorithms make this choice differently.

---

## The Challenge

Different apps need different things:
- **Video streaming (eMBB)**: Needs lots of data, can tolerate some delay
- **Self-driving car commands (URLLC)**: Needs data FAST (within 10ms), or accidents happen!
- **Smart home sensors (mMTC)**: Sends tiny data, delay doesn't matter much

A good scheduler must balance:
1. **Speed** (throughput) - send lots of data
2. **Fairness** - don't ignore some users
3. **Delay** - urgent data gets priority
4. **Quality of Service (QoS)** - treat different traffic types appropriately

---

## The 5 Scheduling Algorithms

### 1. Round Robin (RR) - "Take Turns"

**Simple Idea**: Like kids taking turns on a slide - everyone gets a turn in order.

**How It Works**:
- User 1 → User 2 → User 3 → ... → User 20 → back to User 1
- Completely fair in terms of time

**Pros**:
- ✅ Super fair - everyone gets equal turns
- ✅ Simple to implement
- ✅ Predictable

**Cons**:
- ❌ Ignores channel quality (sends even when signal is bad)
- ❌ Ignores urgency (treats emergency data same as regular data)
- ❌ Wastes resources on users with poor signal

**Best For**: When you want absolute fairness and simplicity

**Performance**: 
- Throughput: Medium
- Delay: High (urgent data waits its turn)
- Fairness: Excellent

---

### 2. Proportional Fair (PF) - "Help Those With Good Signal"

**Simple Idea**: Prioritize users who currently have good signal AND haven't received much data recently.

**How It Works**:
```
Score = Current Signal Quality / Average Past Throughput
Pick user with highest score
```

**Example**: 
- User A: Good signal, already got lots of data → Lower score
- User B: Good signal, hasn't got much data → Higher score ✓
- User C: Bad signal, hasn't got much data → Lower score

**Pros**:
- ✅ Maximizes total system throughput
- ✅ Balances fairness and efficiency
- ✅ Industry standard for regular internet traffic

**Cons**:
- ❌ Ignores packet delay
- ❌ No priority for urgent traffic
- ❌ Can starve users with consistently poor signal

**Best For**: Regular internet browsing, downloads, streaming

**Performance**:
- Throughput: High
- Delay: High (doesn't care about urgency)
- Fairness: Good

---

### 3. M-LWDF - "Urgency × Signal × Priority"

**Full Name**: Modified Largest Weighted Delay First

**Simple Idea**: Multiply three factors together - the more urgent, higher priority, and better signal, the higher the score.

**How It Works**:
```
Score = Priority × (Delay / Deadline) × (Signal / Avg Throughput)
Pick user with highest score
```

**Example**:
- Self-driving car data waiting 8ms (deadline: 10ms) → Very high urgency!
- Video streaming waiting 50ms (deadline: 100ms) → Medium urgency
- Sensor data waiting 200ms (deadline: 1000ms) → Low urgency

**Pros**:
- ✅ Prevents deadline violations
- ✅ Differentiates traffic types (URLLC gets priority)
- ✅ Still considers channel quality
- ✅ Proven algorithm used in real 4G/5G networks

**Cons**:
- ❌ Can reduce fairness (urgent users dominate)
- ❌ Multiplicative metric can be aggressive

**Best For**: Mixed traffic with strict delay requirements

**Performance**:
- Throughput: Medium-High
- Delay: Low (especially for URLLC)
- Fairness: Good

---

### 4. EXP Rule - "Exponential Panic Mode"

**Full Name**: Exponential Rule Scheduler

**Simple Idea**: As packets get closer to their deadline, panic exponentially! Like a student cramming for an exam - the closer the deadline, the more urgent it feels.

**How It Works**:
```
Urgency = e^(Delay/Deadline)  ← This grows exponentially!
Score = Priority × Urgency × (Signal / Avg Throughput)
Pick user with highest score
```

**Example**:
- Packet at 50% of deadline: Urgency = e^0.5 = 1.6
- Packet at 80% of deadline: Urgency = e^0.8 = 2.2
- Packet at 95% of deadline: Urgency = e^0.95 = 2.6 (PANIC!)

**Pros**:
- ✅ Excellent for ultra-low latency (URLLC)
- ✅ Smooth urgency escalation
- ✅ Very few deadline violations
- ✅ Mathematically elegant

**Cons**:
- ❌ Can be too aggressive
- ❌ May sacrifice some fairness for delay performance

**Best For**: Ultra-reliable low-latency communications (autonomous vehicles, remote surgery)

**Performance**:
- Throughput: Medium-High
- Delay: Very Low
- Fairness: Medium

---

### 5. Hybrid Adaptive - "Smart Two-Phase Decision" ⭐ (Our Novel Contribution)

**Simple Idea**: First check for emergencies, then optimize everything else. Like a hospital ER - critical patients first, then optimize for others.

**How It Works** (Two Phases):

**Phase 1: Emergency Check**
```
IF any packet is > 70% of its deadline:
    Score = (Delay/Deadline) × Priority × Signal
    Pick the most urgent one
    DONE!
```

**Phase 2: Smart Optimization** (if no emergencies)
```
Score = (Channel Efficiency)^0.4 × 
        (Fairness Factor)^0.2 × 
        (QoS Factor)^0.3 × 
        (Buffer Factor)^0.1

Where:
- Channel Efficiency = Current Rate / Average Rate
- Fairness Factor = System Average / User Average (helps underserved users)
- QoS Factor = (1 + Delay/Deadline) × Priority
- Buffer Factor = Considers how full the buffer is
```

**Why This Is Smart**:
1. **Prevents disasters**: Emergency mode catches critical packets
2. **Balances everything**: When no emergency, optimizes 4 factors simultaneously
3. **Explicit fairness**: Actively helps users who got less data
4. **Buffer-aware**: Prevents overflow by considering queue state

**Example Scenario**:
- Self-driving car packet at 95% deadline → Phase 1 catches it! ✓
- No emergencies? → Phase 2 balances video streaming, sensor data, etc.

**Pros**:
- ✅ Best overall balance across ALL metrics
- ✅ Prevents deadline violations (emergency mode)
- ✅ Maintains fairness (explicit fairness factor)
- ✅ Adapts to traffic conditions dynamically
- ✅ Considers buffer state (prevents packet loss)
- ✅ Novel contribution combining multiple strategies

**Cons**:
- ❌ More complex to implement
- ❌ Higher computational cost

**Best For**: Real-world 5G networks with mixed traffic (eMBB + URLLC + mMTC)

**Performance**:
- Throughput: High
- Delay: Low
- Packet Loss: Very Low
- Fairness: Excellent

---

## Quick Comparison Table

| Algorithm | When to Use | Main Strength | Main Weakness |
|-----------|-------------|---------------|---------------|
| **Round Robin** | Need absolute fairness | Everyone gets equal turns | Ignores everything else |
| **Proportional Fair** | Regular internet traffic | High throughput | Ignores delay |
| **M-LWDF** | Mixed traffic with deadlines | Delay-aware | Can be unfair |
| **EXP Rule** | Ultra-low latency needed | Prevents deadline violations | Aggressive |
| **Hybrid Adaptive** ⭐ | Real 5G networks | Balances everything | Complex |

---

## Key Terms Explained

### Abbreviations

- **5G NR**: 5G New Radio (the latest wireless standard)
- **gNB**: Next-generation NodeB (5G base station/cell tower)
- **UE**: User Equipment (your phone)
- **TTI**: Transmission Time Interval (1 millisecond time slot)
- **CQI**: Channel Quality Indicator (signal strength, 1-15 scale)
- **QoS**: Quality of Service (different treatment for different traffic)
- **eMBB**: Enhanced Mobile Broadband (video streaming, downloads)
- **URLLC**: Ultra-Reliable Low-Latency Communications (self-driving cars)
- **mMTC**: Massive Machine-Type Communications (IoT sensors)
- **RR**: Round Robin
- **PF**: Proportional Fair
- **M-LWDF**: Modified Largest Weighted Delay First

### Important Concepts

**Throughput**: How much data is sent (bytes per millisecond)
- Higher = Better

**Delay**: How long packets wait before being sent (milliseconds)
- Lower = Better

**Packet Loss**: Percentage of packets dropped (timeout or buffer full)
- Lower = Better

**Fairness (Jain's Index)**: How equally resources are distributed (0 to 1)
- 1.0 = Perfect fairness
- 0.5 = Some users get much more than others
- Higher = Better

**Buffer**: Queue where packets wait before transmission
- Like a waiting line at a store

**Channel Quality**: Signal strength between tower and phone
- Changes constantly due to movement, obstacles, interference

---

## Which Algorithm Is Best?

**There's no single "best" - it depends on your goal:**

1. **Need absolute fairness?** → Round Robin
2. **Want maximum throughput?** → Proportional Fair
3. **Have strict delay requirements?** → M-LWDF or EXP Rule
4. **Need to balance everything?** → **Hybrid Adaptive** ⭐

**For modern 5G networks with mixed traffic, Hybrid Adaptive is the best choice** because:
- It handles emergencies (URLLC)
- Maintains high throughput (eMBB)
- Stays fair to all users
- Prevents packet loss
- Adapts to changing conditions

---

## How Our Simulation Works

1. **Setup**: Create 20 virtual phones with different traffic types
   - 10 phones: Video streaming (eMBB)
   - 6 phones: Self-driving car data (URLLC)
   - 4 phones: IoT sensors (mMTC)

2. **Run**: Simulate 1000 milliseconds
   - Each millisecond: Generate packets, update signal quality, pick one user, send data

3. **Compare**: Run all 5 algorithms with identical conditions
   - Same users, same traffic, same channel conditions
   - Fair comparison!

4. **Measure**: Calculate performance metrics
   - Throughput, delay, packet loss, fairness

5. **Visualize**: Generate graphs showing which algorithm performs best

---

## Real-World Impact

**Why This Matters**:

- **Self-driving cars**: Need data within 10ms or accidents happen
  - Bad scheduler → Delayed commands → Crash ❌
  - Good scheduler → Fast commands → Safe ✅

- **Video calls**: Need consistent data flow
  - Bad scheduler → Freezing, lag ❌
  - Good scheduler → Smooth video ✅

- **Fairness**: Everyone should get service
  - Bad scheduler → Some users starved ❌
  - Good scheduler → Everyone served ✅

**Our Hybrid Adaptive scheduler solves all these problems simultaneously!**

---

## Summary

We built a 5G scheduling simulator that compares 5 algorithms:

1. **Round Robin**: Fair but simple
2. **Proportional Fair**: Fast but ignores urgency
3. **M-LWDF**: Delay-aware industry standard
4. **EXP Rule**: Aggressive delay prevention
5. **Hybrid Adaptive**: Our smart solution that balances everything ⭐

The Hybrid Adaptive scheduler is our novel contribution - it uses a two-phase approach (emergency check + optimization) to achieve the best overall performance across all metrics.

**Result**: Better 5G networks that are fast, fair, and reliable for everyone!
