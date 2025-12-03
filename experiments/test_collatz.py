import sys
import os
import json
from typing import List, Dict

# Add parent directory (src/) to the path to import collatz_generators
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collatz_generators import generalized_collatz

def run_all_tests():
    """Runs a few critical tests for the generalized_collatz function."""
    print("--- Running Collatz Function Tests ---")

    # Test Case 1: Standard Collatz (a=2, b=3, c=1) starting at 6
    # The robust solver detects the full 4->2->1->4 cycle, hence the longer sequence.
    a1, b1, c1, n1 = 2, 3, 1, 6 
    expected_seq_1 = [6, 3, 10, 5, 16, 8, 4, 2, 1, 4] 
    expected_status_1 = 'converged' # Status is 'converged' because the cycle includes 1
    
    result_1 = generalized_collatz(n1, a1, b1, c1)
    
    if result_1['sequence'] == expected_seq_1 and result_1['status'] == expected_status_1:
        print(f"✅ Test 1 (Standard Collatz 3n+1 @ 6): Passed")
    else:
        print(f"❌ Test 1 Failed!")
        print(f"   Expected: {expected_seq_1} | Status: {expected_status_1}")
        print(f"   Received: {result_1['sequence']} | Status: {result_1['status']}")

    print("-" * 35)
    
    # Test Case 2: Simple 1-fixed point cycle (a=2, b=-1, c=3) -> 2 -> 1 -> 1...
    a3, b3, c3, n3 = 2, -1, 3, 2 
    expected_seq_3 = [2, 1, 1] # Correctly fixed point at 1.
    expected_status_3 = 'converged' # Status is 'converged' because the cycle includes 1

    result_3 = generalized_collatz(n3, a3, b3, c3, max_iterations=10)
    
    if result_3['status'] == expected_status_3 and result_3['sequence'][0:3] == expected_seq_3:
        print(f"✅ Test 2 (Cyclic Case @ 2): Passed")
    else:
        print(f"❌ Test 2 Failed!")
        print(f"   Expected cycle: {expected_seq_3[0:3]} | Status: {expected_status_3}")
        print(f"   Received: {result_3['sequence'][0:4]} | Status: {result_3['status']}")

    print("-" * 35)

if __name__ == "__main__":
    run_all_tests()