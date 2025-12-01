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
