# In src/collatz_generators.py

def generalized_collatz(n: int, a: int, b: int, c: int, max_iterations: int = 1000000) -> Dict:
    """
    MOD-BASED generalized Collatz sequence.
    a: Divisor, b: Multiplier, c: Adder
    ...
    Returns: {'sequence': list, 'status': str}
    """
    if n <= 0 or a <= 0:
        return {'sequence': [], 'status': 'invalid_input'}
    
    sequence = [n]
    visited = {n}
    current = n
    
    for _ in range(max_iterations):
        
        # 1. Termination Check
        if current == 1:
            return {'sequence': sequence, 'status': 'converged'}
            
        # 2. Magnitude Safety Check
        if current > 10**50: 
            return {'sequence': sequence, 'status': 'diverged'} # Exit early with status
            
        # --- Core Logic ---
        if current % a == 0:
            current = current // a
        else:
            numerator = b * current + c
            
            if a == 2 and b == 3 and c == 1:
                current = numerator
            else:
                while numerator % a == 0 and numerator > 0:
                    numerator = numerator // a
                current = numerator

        # 3. Cycle Detection
        if current in visited:
            sequence.append(current)
            # Cycle detected before max_iter
            return {'sequence': sequence, 'status': 'cycled'}
            
        sequence.append(current)
        visited.add(current)
        
    # If loop finishes due to max_iterations
    return {'sequence': sequence, 'status': 'max_iter'}
