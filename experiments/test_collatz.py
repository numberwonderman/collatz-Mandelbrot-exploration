import sys
import os
import json

# Add parent directory (src/) to the path to import collatz_generators
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collatz_generators import generalized_collatz

def run_all_tests():
    """Runs a few critical tests for the generalized_collatz function."""
    print("--- Running Collatz Function Tests ---")

    # Test Case 1: Standard Collatz (a=2, b=3, c=1) starting at 6
    # Sequence: 6, 3, 10, 5, 16, 8, 4, 2, 1
    a1, b1, c1, n1 = 2, 3, 1, 6 
    expected_seq_1 = [6, 3, 10, 5, 16, 8, 4, 2, 1]
    
    result_1 = generalized_collatz(n1, a1, b1, c1)
    
    if result_1['sequence'] == expected_seq_1 and result_1['status'] == 'converged':
        print(f"✅ Test 1 (Standard Collatz 3n+1 @ 6): Passed")
    else:
        print(f"❌ Test 1 Failed!")
        print(f"   Expected: {expected_seq_1} | Status: converged")
        print(f"   Received: {result_1['sequence']} | Status: {result_1['status']}")

    print("-" * 35)
    
    # Test Case 2: A simple generalized case that cycles
    # Parameters: a=3, b=2, c=1. Rule: n mod 3? -> 2n+1 : n/3
    # Sequence starting at 2: 2 -> 5 -> 11 -> 23 -> 47 -> 95 -> 191 -> 383 -> 767 -> ... (likely diverges or max_iter)
    a2, b2, c2, n2 = 3, 4, 1, 2
    # Sequence: 2 -> 9/3=3 -> 13/.. -> 53/.. -> 213/3=71 -> 285/3=95 -> 381/3=127 -> 509/.. (Likely diverges or hits max_iter)
    
    # Let's test a simple 2-cycle case (a=2, b=-1, c=3) -> 1, 2, 1, 2...
    a3, b3, c3, n3 = 2, -1, 3, 2 
    expected_seq_3 = [2, 1, 2] # Should cycle back to 2
    result_3 = generalized_collatz(n3, a3, b3, c3, max_iterations=10)
    
    if result_3['status'] == 'cycled' and result_3['sequence'][0:3] == expected_seq_3:
        print(f"✅ Test 2 (Cyclic Case @ 2): Passed")
    else:
        print(f"❌ Test 2 Failed!")
        print(f"   Expected cycle: {expected_seq_3[0:3]} | Status: cycled")
        print(f"   Received: {result_3['sequence'][0:4]} | Status: {result_3['status']}")

    print("-" * 35)

if __name__ == "__main__":
    run_all_tests()
