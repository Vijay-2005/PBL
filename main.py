"""
Main execution script for 5G NR Scheduling Simulation
"""
import numpy as np
from simulator import Simulator
from schedulers import RoundRobinScheduler, ProportionalFairScheduler, QoSAwareScheduler
from visualizer import Visualizer
from config import NUM_UES, SIMULATION_TIME, PLOT_RESULTS


def main():
    print("\n" + "="*80)
    print("5G NR DOWNLINK SCHEDULING SIMULATION")
    print("="*80)
    print(f"Configuration: {NUM_UES} UEs, {SIMULATION_TIME} TTIs")
    print(f"Traffic Mix: 50% eMBB, 30% URLLC, 20% mMTC")
    print("="*80 + "\n")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Initialize schedulers
    schedulers = [
        RoundRobinScheduler(),
        ProportionalFairScheduler(),
        QoSAwareScheduler()
    ]
    
    results = []
    
    # Run simulations
    for scheduler in schedulers:
        print(f"Simulating: {scheduler.name}...")
        sim = Simulator(scheduler)
        metrics = sim.run()
        results.append(metrics)
        print(f"✓ {scheduler.name} completed\n")
    
    # Display results
    visualizer = Visualizer(results)
    visualizer.print_summary_table()
    
    # Generate plots
    if PLOT_RESULTS:
        print("Generating performance plots...")
        visualizer.plot_all()
    
    print("\nSimulation completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
