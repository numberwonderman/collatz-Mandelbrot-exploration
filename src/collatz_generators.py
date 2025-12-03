from typing import Dict

def generalized_collatz(n: int, a: int, b: int, c: int, max_iterations: int = 1000000) -> Dict:
    """
    MOD-BASED generalized Collatz sequence. (a: Divisor, b: Multiplier, c: Adder)
    Terminates only on cycle detection or max_iter/divergence.
    The status 'converged' is now defined as 'cycling and including 1'.
    """
    if n <= 0 or a <= 0:
        return {'sequence': [], 'status': 'invalid_input'}
    
    sequence = [n]
    # visited now stores the index to accurately find the cycle start
    visited = {n: 0} 
    current = n
    
    # We will remove the DEBUG print statements for a cleaner run now
    
    for i in range(max_iterations):
        
        # 1. Magnitude Safety Check
        if current > 10**50:
            return {'sequence': sequence, 'status': 'diverged'}
            
        # --- Calculate Next Value (next_val) ---
        if current % a == 0:
            next_val = current // a
        else:
            numerator = b * current + c
            
            if a == 2 and b == 3 and c == 1:
                next_val = numerator
            else:
                while numerator % a == 0 and numerator > 0:
                    numerator = numerator // a
                next_val = numerator

        # 2. Cycle Detection (The ONLY termination check besides max_iter/divergence)
        if next_val in visited:
            sequence.append(next_val)
            
            # Check if 1 is part of the detected cycle
            cycle_start_index = visited[next_val]
            cycle_elements = sequence[cycle_start_index:]
            
            if 1 in cycle_elements:
                # Sequence 2, 1, 2 is now correctly labeled 'converged' (cycling to 1)
                return {'sequence': sequence, 'status': 'converged'} 
            else:
                # Non-trivial cycle that does not include 1
                return {'sequence': sequence, 'status': 'cycled'} 

        # 3. Continue Sequence
        sequence.append(next_val)
        visited[next_val] = len(sequence) - 1 # Store index of number
        current = next_val
        
    return {'sequence': sequence, 'status': 'max_iter'}