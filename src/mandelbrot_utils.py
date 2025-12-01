def mandelbrot_escape_time(c: complex, max_iter: int = 1000) -> int:
    """
    Calculates the number of iterations before a complex number c escapes 
    the radius of 2 under the iteration z = z*z + c, or max_iter if bounded.
    """
    z = 0 + 0j
    for i in range(max_iter):
        if abs(z) > 2.0:
            return i
        z = z*z + c
    return max_iter

def is_in_mandelbrot_set(c: complex, threshold: int = 1000) -> bool:
    """True if c is in the Mandelbrot set (i.e., remains bounded)."""
    return mandelbrot_escape_time(c, threshold) == threshold
