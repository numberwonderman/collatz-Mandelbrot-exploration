import re
import pandas as pd
import os

def parse_raw_log(input_file, output_file):
    
    # Simplified Regex: ONLY captures parameters (a, b, c) and the Conv Rate
    # Note: This is designed to match the log format you provided.
    pattern = re.compile(
        # Group 1 (a), Group 2 (b), Group 3 (c)
        r"Sample \d+/\d+: \(a,b,c\)=\((\d+),(\d+),(\d+)\) \| Conv Rate: (\d+\.\d+) \|"
    )
    
    data = []
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    # Extracted values from the groups in the regex
                    a, b, c, conv_rate = match.groups()
                    
                    data.append({
                        'a_divisor': int(a),
                        'b_multiplier': int(b),
                        'c_adder': int(c),
                        'collatz_conv_rate': float(conv_rate)
                    })
        
        if not data:
            print("ERROR: No data matched the expected log pattern. Please check the content of the raw log file.")
            return

        df = pd.DataFrame(data)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        
        print(f"✅ Success! Recovered and saved {len(df)} samples to {output_file}")
        
    except FileNotFoundError:
        print(f"ERROR: Input log file not found at {input_file}.")

if __name__ == "__main__":
    # Defines the output path: ../data/results/experiment_01_results.csv
    output_path = os.path.join('..', 'data', 'results', 'experiment_01_results.csv')
    # Assumes the raw log is in the root directory
    parse_raw_log('raw_experiment_01_log.txt', output_path)


