"""
User Equipment (UE) class for 5G NR simulation
"""
import numpy as np
from config import TRAFFIC_TYPES, MAX_BUFFER_SIZE


class Packet:
    def __init__(self, size, arrival_time, traffic_type):
        self.size = size
        self.arrival_time = arrival_time
        self.traffic_type = traffic_type


class UserEquipment:
    def __init__(self, ue_id, traffic_type):
        self.ue_id = ue_id
        self.traffic_type = traffic_type
        self.priority = TRAFFIC_TYPES[traffic_type]['priority']
        self.delay_threshold = TRAFFIC_TYPES[traffic_type]['delay_threshold']
        self.packet_size = TRAFFIC_TYPES[traffic_type]['packet_size']
        
        self.buffer = []
        self.buffer_size = 0
        
        self.total_throughput = 0
        self.throughput_history = []
        self.avg_throughput = 0.001
        
        self.total_delay = 0
        self.served_packets = 0
        self.dropped_packets = 0
        
        self.cqi = np.random.randint(1, 16)
    
    def generate_packet(self, current_time):
        """Generate a new packet and add to buffer"""
        packet = Packet(self.packet_size, current_time, self.traffic_type)
        if self.buffer_size + packet.size <= MAX_BUFFER_SIZE:
            self.buffer.append(packet)
            self.buffer_size += packet.size
        else:
            self.dropped_packets += 1
    
    def update_cqi(self):
        """Update channel quality with temporal correlation"""
        change = np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])
        self.cqi = np.clip(self.cqi + change, 1, 15)
    
    def get_head_of_line_delay(self, current_time):
        """Get delay of the oldest packet in buffer"""
        if self.buffer:
            return current_time - self.buffer[0].arrival_time
        return 0
    
    def transmit(self, current_time, data_rate):
        """Transmit data and update statistics"""
        transmitted = 0
        while self.buffer and transmitted < data_rate:
            packet = self.buffer[0]
            if transmitted + packet.size <= data_rate:
                self.buffer.pop(0)
                self.buffer_size -= packet.size
                transmitted += packet.size
                
                delay = current_time - packet.arrival_time
                self.total_delay += delay
                self.served_packets += 1
            else:
                break
        
        if transmitted > 0:
            self.total_throughput += transmitted
            self.throughput_history.append(transmitted)
            self.avg_throughput = 0.9 * self.avg_throughput + 0.1 * transmitted
        
        return transmitted
    
    def check_and_drop_expired(self, current_time):
        """Drop packets exceeding delay threshold"""
        while self.buffer:
            packet = self.buffer[0]
            if current_time - packet.arrival_time > self.delay_threshold:
                self.buffer.pop(0)
                self.buffer_size -= packet.size
                self.dropped_packets += 1
            else:
                break
