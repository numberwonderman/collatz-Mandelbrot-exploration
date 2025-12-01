from .collatz_generators import generalized_collatz # Now imports YOUR updated function

def measure_collatz_behavior(a, b, c, test_range=(1, 50)):
    """
    Runs the sequence for a range of starting integers (n) to determine
    the convergence rate of the parameter set (a, b, c).
    """
    results = {
        'converged': 0,
        'diverged_or_max': 0,
        'cycled': 0,
    }
    total_steps_for_converged = 0
    total_tests = test_range[1] - test_range[0]
    
    for n in range(test_range[0], test_range[1]):
        # Run simulation using YOUR updated function
        res = generalized_collatz(n, a, b, c)
        status = res['status']
        
        if status == 'converged':
            results['converged'] += 1
            # Note: We use YOUR function's returned sequence length
            total_steps_for_converged += len(res['sequence'])
        elif status == 'cycled':
            results['cycled'] += 1
        else: # 'diverged', 'max_iter', 'invalid_input'
            results['diverged_or_max'] += 1

    # Calculate metrics
    convergence_rate = results['converged'] / total_tests if total_tests > 0 else 0
    avg_steps = total_steps_for_converged / results['converged'] if results['converged'] > 0 else 0
    
    return {
        'convergence_rate': convergence_rate, # The key metric for Mandelbrot correlation
        'divergence_rate': (results['diverged_or_max'] / total_tests),
        'cycle_rate': (results['cycled'] / total_tests),
        'avg_steps_to_one': avg_steps
    }
