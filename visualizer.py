"""
Visualization module for simulation results
"""
import matplotlib.pyplot as plt
import numpy as np


class Visualizer:
    def __init__(self, results):
        self.results = results
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_all(self):
        """Generate all comparison plots"""
        self.plot_throughput_comparison()
        self.plot_delay_comparison()
        self.plot_packet_loss_comparison()
        self.plot_fairness_comparison()
        self.plot_per_ue_throughput()
        self.plot_per_ue_delay()
        plt.show()
    
    def plot_throughput_comparison(self):
        """Bar chart: Average throughput"""
        schedulers = [r['scheduler'] for r in self.results]
        throughputs = [r['avg_throughput'] for r in self.results]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        plt.figure(figsize=(10, 5))
        bars = plt.bar(schedulers, throughputs, color=colors[:len(schedulers)], alpha=0.8)
        plt.ylabel('Average Throughput (bytes/TTI)', fontsize=11)
        plt.title('Average Throughput Comparison', fontsize=13, fontweight='bold')
        plt.xticks(rotation=15, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
    
    def plot_delay_comparison(self):
        """Bar chart: Average packet delay"""
        schedulers = [r['scheduler'] for r in self.results]
        delays = [r['avg_delay'] for r in self.results]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        plt.figure(figsize=(10, 5))
        bars = plt.bar(schedulers, delays, color=colors[:len(schedulers)], alpha=0.8)
        plt.ylabel('Average Packet Delay (TTI)', fontsize=11)
        plt.title('Average Packet Delay Comparison', fontsize=13, fontweight='bold')
        plt.xticks(rotation=15, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
    
    def plot_packet_loss_comparison(self):
        """Bar chart: Packet loss ratio"""
        schedulers = [r['scheduler'] for r in self.results]
        loss_ratios = [r['packet_loss_ratio'] * 100 for r in self.results]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        plt.figure(figsize=(10, 5))
        bars = plt.bar(schedulers, loss_ratios, color=colors[:len(schedulers)], alpha=0.8)
        plt.ylabel('Packet Loss Ratio (%)', fontsize=11)
        plt.title('Packet Loss Ratio Comparison', fontsize=13, fontweight='bold')
        plt.xticks(rotation=15, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
    
    def plot_fairness_comparison(self):
        """Bar chart: Jain's Fairness Index"""
        schedulers = [r['scheduler'] for r in self.results]
        fairness = [r['fairness_index'] for r in self.results]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        plt.figure(figsize=(10, 5))
        bars = plt.bar(schedulers, fairness, color=colors[:len(schedulers)], alpha=0.8)
        plt.ylabel("Jain's Fairness Index", fontsize=11)
        plt.title("Fairness Comparison", fontsize=13, fontweight='bold')
        plt.ylim([0, 1.1])
        plt.xticks(rotation=15, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
    
    def plot_per_ue_throughput(self):
        """Line plot: Per-UE throughput distribution"""
        plt.figure(figsize=(10, 5))
        
        for result in self.results:
            throughputs = sorted(result['throughput_per_ue'], reverse=True)
            plt.plot(range(len(throughputs)), throughputs, 
                    marker='o', label=result['scheduler'], linewidth=2, markersize=4)
        
        plt.xlabel('UE Index (sorted by throughput)', fontsize=11)
        plt.ylabel('Throughput (bytes/TTI)', fontsize=11)
        plt.title('Per-UE Throughput Distribution', fontsize=13, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(alpha=0.3)
        plt.tight_layout()
    
    def plot_per_ue_delay(self):
        """Box plot: Per-UE delay distribution"""
        plt.figure(figsize=(10, 5))
        
        data = [result['delay_per_ue'] for result in self.results]
        labels = [result['scheduler'] for result in self.results]
        
        bp = plt.boxplot(data, labels=labels, patch_artist=True,
                        boxprops=dict(facecolor='lightblue', alpha=0.7),
                        medianprops=dict(color='red', linewidth=2))
        
        plt.ylabel('Packet Delay (TTI)', fontsize=11)
        plt.title('Per-UE Delay Distribution', fontsize=13, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
    
    def print_summary_table(self):
        """Print performance metrics table"""
        print("\n" + "="*80)
        print("PERFORMANCE COMPARISON SUMMARY")
        print("="*80)
        print(f"{'Scheduler':<25} {'Throughput':<15} {'Delay':<12} {'Loss %':<12} {'Fairness':<10}")
        print("-"*80)
        
        for result in self.results:
            print(f"{result['scheduler']:<25} "
                  f"{result['avg_throughput']:<15.2f} "
                  f"{result['avg_delay']:<12.2f} "
                  f"{result['packet_loss_ratio']*100:<12.2f} "
                  f"{result['fairness_index']:<10.3f}")
        
        print("="*80 + "\n")
