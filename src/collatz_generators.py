from typing import Dict

def generalized_collatz(n: int, a: int, b: int, c: int, max_iterations: int = 1000000) -> Dict:
    """
    MOD-BASED generalized Collatz sequence. (a: Divisor, b: Multiplier, c: Adder)
    """
    if n <= 0 or a <= 0:
        return {'sequence': [], 'status': 'invalid_input'}
    
    sequence = [n]
    visited = {n}
    current = n
    
    print(f"\n--- DEBUG START --- Parameters: (A={a}, B={b}, C={c}), Start N={n}")
    
    for i in range(max_iterations):
        
        # 1. Magnitude Safety Check
        if current > 10**50:
            print(f"--- DEBUG END --- Exit: Diverged.")
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

        # 2. Cycle Detection (Must come BEFORE Convergence Check)
        if next_val in visited:
            sequence.append(next_val)
            print(f"--- DEBUG END --- Exit: Cycled! Sequence: {sequence}")
            return {'sequence': sequence, 'status': 'cycled'}
        
        # 3. Convergence Check
        if next_val == 1:
            sequence.append(next_val)
            # LOGIC FLAW: For generalized rules, N=1 should not terminate unless standard rule.
            # We must be seeing this debug line print for Test 2.
            print(f"--- DEBUG END --- Exit: Converged! Sequence: {sequence}")
            return {'sequence': sequence, 'status': 'converged'}
            
        # 4. Continue Sequence
        sequence.append(next_val)
        visited.add(next_val)
        current = next_val
        
        print(f"DEBUG: Step {i+1}. Current: {current}. Sequence Length: {len(sequence)}")
        
    print(f"--- DEBUG END --- Exit: Max Iterations.")
    return {'sequence': sequence, 'status': 'max_iter'}