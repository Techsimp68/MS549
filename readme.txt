#  Efficient Ride-Sharing Simulator

## Purpose / Design

This project simulates an event-driven ride-sharing system within a traffic-aware city map. 
It uses graph structures and a priority queue to dynamically assign cars to rider requests, compute optimal travel paths with variable traffic conditions, and track system performance over time. The simulation is designed to be modular, scalable, 
and extendable for future features like surge pricing and traffic congestion analysis.

## How to Run

1. Make sure the following files are in your working directory:
   - `simulation.py`
   - `graph.py`
   - `event.py`
   - `car.py`
   - `rider.py`
   - `map.csv`
   - `main.py`

2. In a terminal or command prompt, run the following command:

```bash
python main.py
