"""
5G NR Downlink Scheduling Simulator
"""
import numpy as np
from user_equipment import UserEquipment
from config import (NUM_UES, SIMULATION_TIME, PACKET_ARRIVAL_RATE, 
                    TRAFFIC_TYPES, VERBOSE)


class Simulator:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.ues = []
        self.current_time = 0
        self.initialize_ues()
    
    def initialize_ues(self):
        """Create UEs with different traffic types"""
        traffic_types = list(TRAFFIC_TYPES.keys())
        for i in range(NUM_UES):
            # Distribute traffic types: 50% eMBB, 30% URLLC, 20% mMTC
            if i < NUM_UES * 0.5:
                traffic_type = 'eMBB'
            elif i < NUM_UES * 0.8:
                traffic_type = 'URLLC'
            else:
                traffic_type = 'mMTC'
            
            ue = UserEquipment(i, traffic_type)
            self.ues.append(ue)
    
    def run(self):
        """Execute simulation"""
        if VERBOSE:
            print(f"\n{'='*60}")
            print(f"Running {self.scheduler.name} Scheduler")
            print(f"{'='*60}")
        
        for tti in range(SIMULATION_TIME):
            self.current_time = tti
            
            # Update channel conditions
            for ue in self.ues:
                ue.update_cqi()
            
            # Generate packets
            for ue in self.ues:
                if np.random.random() < PACKET_ARRIVAL_RATE:
                    ue.generate_packet(self.current_time)
            
            # Drop expired packets
            for ue in self.ues:
                ue.check_and_drop_expired(self.current_time)
            
            # Schedule and transmit
            selected_ue = self.scheduler.select_ue(self.ues, self.current_time)
            if selected_ue:
                data_rate = self.scheduler.get_data_rate(selected_ue.cqi)
                selected_ue.transmit(self.current_time, data_rate)
        
        if VERBOSE:
            print(f"Simulation completed: {SIMULATION_TIME} TTIs\n")
        
        return self.collect_metrics()
    
    def collect_metrics(self):
        """Collect performance metrics"""
        metrics = {
            'scheduler': self.scheduler.name,
            'avg_throughput': [],
            'avg_delay': [],
            'packet_loss_ratio': [],
            'throughput_per_ue': [],
            'delay_per_ue': [],
            'served_packets': [],
            'dropped_packets': []
        }
        
        total_throughput = 0
        total_delay = 0
        total_served = 0
        total_dropped = 0
        
        for ue in self.ues:
            throughput = ue.total_throughput / SIMULATION_TIME
            metrics['throughput_per_ue'].append(throughput)
            total_throughput += throughput
            
            if ue.served_packets > 0:
                avg_delay = ue.total_delay / ue.served_packets
                metrics['delay_per_ue'].append(avg_delay)
                total_delay += ue.total_delay
                total_served += ue.served_packets
            else:
                metrics['delay_per_ue'].append(0)
            
            metrics['served_packets'].append(ue.served_packets)
            metrics['dropped_packets'].append(ue.dropped_packets)
            total_dropped += ue.dropped_packets
        
        metrics['avg_throughput'] = total_throughput / NUM_UES
        metrics['avg_delay'] = total_delay / total_served if total_served > 0 else 0
        metrics['packet_loss_ratio'] = total_dropped / (total_served + total_dropped) if (total_served + total_dropped) > 0 else 0
        metrics['fairness_index'] = self.calculate_fairness(metrics['throughput_per_ue'])
        
        return metrics
    
    def calculate_fairness(self, throughputs):
        """Calculate Jain's Fairness Index"""
        n = len(throughputs)
        if n == 0:
            return 0
        sum_throughput = sum(throughputs)
        sum_squared = sum([t**2 for t in throughputs])
        if sum_squared == 0:
            return 1
        return (sum_throughput ** 2) / (n * sum_squared)
