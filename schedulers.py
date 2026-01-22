"""
Scheduling algorithms for 5G NR downlink
"""
import numpy as np
from config import ALPHA, BETA, GAMMA, MAX_BUFFER_SIZE


class Scheduler:
    def __init__(self, name):
        self.name = name
    
    def select_ue(self, ues, current_time):
        """Select UE for transmission - to be overridden"""
        raise NotImplementedError
    
    def get_data_rate(self, cqi):
        """Map CQI to data rate (simplified model)"""
        # Approximate mapping: CQI 1-15 to data rates
        rate_table = [
            0, 150, 300, 450, 600, 800, 1000, 1200,
            1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800
        ]
        return rate_table[cqi]


class RoundRobinScheduler(Scheduler):
    def __init__(self):
        super().__init__("Round Robin")
        self.last_scheduled = -1
    
    def select_ue(self, ues, current_time):
        """Cyclic selection of UEs"""
        num_ues = len(ues)
        for i in range(num_ues):
            idx = (self.last_scheduled + 1 + i) % num_ues
            if ues[idx].buffer:
                self.last_scheduled = idx
                return ues[idx]
        return None


class ProportionalFairScheduler(Scheduler):
    def __init__(self):
        super().__init__("Proportional Fair")
    
    def select_ue(self, ues, current_time):
        """Select UE based on CQI/avg_throughput ratio"""
        best_ue = None
        best_metric = -1
        
        for ue in ues:
            if ue.buffer:
                metric = ue.cqi / max(ue.avg_throughput, 0.001)
                if metric > best_metric:
                    best_metric = metric
                    best_ue = ue
        
        return best_ue


class MLWDFScheduler(Scheduler):
    """Modified Largest Weighted Delay First - Industry standard QoS scheduler"""
    def __init__(self):
        super().__init__("M-LWDF")
    
    def select_ue(self, ues, current_time):
        """Select UE using M-LWDF metric: priority * delay_ratio * channel_ratio"""
        best_ue = None
        best_metric = -1
        
        for ue in ues:
            if ue.buffer:
                # Delay ratio: current delay / delay threshold
                delay = ue.get_head_of_line_delay(current_time)
                delay_ratio = delay / ue.delay_threshold
                
                # Channel-aware component (PF-like)
                channel_ratio = ue.cqi / max(ue.avg_throughput, 0.001)
                
                # Priority weight
                priority_weight = ue.priority
                
                # M-LWDF metric: combines all factors multiplicatively
                metric = priority_weight * delay_ratio * channel_ratio
                
                if metric > best_metric:
                    best_metric = metric
                    best_ue = ue
        
        return best_ue


class HybridAdaptiveScheduler(Scheduler):
    """Advanced hybrid scheduler with dynamic mode switching"""
    def __init__(self):
        super().__init__("Hybrid Adaptive")
        self.urgency_threshold = 0.6  # Switch to urgency mode at 60% of delay threshold
    
    def select_ue(self, ues, current_time):
        """Hybrid approach: urgency-first for critical packets, then optimized selection"""
        # Phase 1: Check for urgent packets (URLLC or near-deadline)
        urgent_ue = self._select_urgent_ue(ues, current_time)
        if urgent_ue:
            return urgent_ue
        
        # Phase 2: Optimized selection for non-urgent traffic
        return self._select_optimized_ue(ues, current_time)
    
    def _select_urgent_ue(self, ues, current_time):
        """Select UE with urgent packets exceeding threshold"""
        best_ue = None
        best_urgency = -1
        
        for ue in ues:
            if ue.buffer:
                delay = ue.get_head_of_line_delay(current_time)
                urgency_ratio = delay / ue.delay_threshold
                
                # Prioritize packets approaching deadline
                if urgency_ratio > self.urgency_threshold:
                    # Urgency score: higher for URLLC and closer to deadline
                    urgency_score = (urgency_ratio ** 2) * ue.priority * ue.cqi
                    
                    if urgency_score > best_urgency:
                        best_urgency = urgency_score
                        best_ue = ue
        
        return best_ue
    
    def _select_optimized_ue(self, ues, current_time):
        """Optimized selection balancing throughput, fairness, and QoS"""
        best_ue = None
        best_metric = -1
        
        # Calculate system-wide statistics for normalization
        avg_system_throughput = np.mean([ue.avg_throughput for ue in ues if ue.buffer]) or 1
        
        for ue in ues:
            if ue.buffer:
                # Component 1: Channel efficiency (instantaneous rate / average rate)
                instantaneous_rate = self.get_data_rate(ue.cqi)
                channel_efficiency = instantaneous_rate / max(ue.avg_throughput, 0.001)
                
                # Component 2: Fairness factor (penalize high-throughput users)
                fairness_factor = avg_system_throughput / max(ue.avg_throughput, 0.001)
                
                # Component 3: QoS factor (delay-based with priority)
                delay = ue.get_head_of_line_delay(current_time)
                qos_factor = (1 + delay / ue.delay_threshold) * (ue.priority ** 1.5)
                
                # Component 4: Buffer occupancy (prioritize fuller buffers more aggressively)
                buffer_ratio = ue.buffer_size / MAX_BUFFER_SIZE
                buffer_factor = 1 + buffer_ratio * 0.8
                
                # Combined metric with adaptive weights
                metric = (channel_efficiency ** 0.35) * (fairness_factor ** 0.25) * \
                         (qos_factor ** 0.25) * (buffer_factor ** 0.15)
                
                if metric > best_metric:
                    best_metric = metric
                    best_ue = ue
        
        return best_ue


class EXPRuleScheduler(Scheduler):
    """EXP Rule scheduler - Exponential rule for delay-sensitive traffic"""
    def __init__(self):
        super().__init__("EXP Rule")
        self.tau = 10  # Time constant for exponential function
    
    def select_ue(self, ues, current_time):
        """Select UE using exponential rule metric"""
        best_ue = None
        best_metric = -1
        
        for ue in ues:
            if ue.buffer:
                # Delay component with exponential growth
                delay = ue.get_head_of_line_delay(current_time)
                delay_ratio = delay / ue.delay_threshold
                exp_delay = np.exp(delay_ratio / self.tau)
                
                # Channel-aware component
                channel_ratio = ue.cqi / max(ue.avg_throughput, 0.001)
                
                # Priority weight
                priority_weight = ue.priority
                
                # EXP Rule metric
                metric = priority_weight * exp_delay * channel_ratio
                
                if metric > best_metric:
                    best_metric = metric
                    best_ue = ue
        
        return best_ue
