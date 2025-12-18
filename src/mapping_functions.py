import numpy as np # Ensure this line is present at the top
def map_params_to_complex_v1(a: int, b: int, c: int) -> complex:
    """
    Mapping Function V1: c_complex = (b/a) + (c/a)*i
    
    - Real axis represents the Multiplier/Divisor ratio (B/A).
    - Imaginary axis represents the Adder/Divisor ratio (C/A).
    """
    if a == 0:
        raise ValueError("Divisor 'a' cannot be zero for mapping.")
        
    real_part = b / a
    imaginary_part = c / a
    
    return complex(real_part, imaginary_part)


# --- HYPOTHESIS B: LOGARITHMIC MAPPING (The Scaling Correction) ---
def map_params_logarithmic(a: int, b: int, c: int) -> complex:
    """
    Hypothesis B: Logarithmically scales the Collatz growth ratios (b/a, c/a) 
    and centers the data near the critical Mandelbrot boundary (c=-1).
    """
    # Real part: ln(b/a), shifted by -1.0
    real_part = np.log(b / a) - 1.0 
    
    # Imaginary part: ln(c/a), shifted by -1.0
    imag_part = np.log(c / a) - 1.0
    
    return complex(real_part, imag_part)
# --- HYPOTHESIS C: TRIGONOMETRIC/POLAR MAPPING ---
def map_params_polar(a: int, b: int, c: int) -> complex:
    """
    Hypothesis C: Maps parameters to a complex number using Polar Coordinates,
    where magnitude (r) is the sum/divisor and the angle (theta) is based on the ratio.
    """
    # 1. Calculate Polar Components
    r = (b + c) / a
    
    # Calculate angle (theta) based on c/b ratio. Using arctan2 is safer against division by zero.
    # We use abs(c/b) to keep the angle in the first quadrant for consistency.
    theta = np.arctan(c / b) 
    
    # 2. Convert to Cartesian Coordinates (x + iy)
    real_part = r * np.cos(theta)
    imag_part = r * np.sin(theta)
    
    return complex(real_part, imag_part)

# --- HYPOTHESIS D: RECIPROCAL PRODUCTS MAPPING (The Inverse Stability Test) ---
def map_params_reciprocal_products(a: int, b: int, c: int) -> complex:
    """
    Hypothesis D: Reciprocal of Paired Products.
    Tests inverse stability: Real = 1/(a*b), Imaginary = 1/(a*c).
    """
    # Real part: Inverse of the multiplier product
    real_part = 1.0 / (a * b)
    
    # Imaginary part: Inverse of the offset product
    imag_part = 1.0 / (a * c)
    
    return complex(real_part, imag_part)

   # Line 64:
def map_params_polar_v2(a: int, b: int, c: int) -> complex:
    # Everything below here MUST be indented
    try:
        ratio_ba = b / a
        log_factor = np.log(ratio_ba) 
        
        magnitude = (c / a) * log_factor
        
        angle = (b * np.pi) / a
        
        return magnitude * np.cos(angle) + 1j * magnitude * np.sin(angle)
        
    except ValueError:
        return 0.0 + 0.0j 
# Ensure the line AFTER the function (line 79 or so) is unindented if it's new code.python experiments/run_experiment_paper_2.py
def map_params_power_squared(a: int, b: int, c: int) -> complex:
    # Hypothesis E: B/A Dominance (Squared)
    try:
        real_part = (b / a) ** 2
        imag_part = -(c / a)
        return real_part + imag_part * 1j
    except ZeroDivisionError:
        return 0.0 + 0.0j