class GaussianCollatz {
    constructor(alpha, beta) {
        this.alpha = alpha; // {re, im} 
        this.beta = beta;   // {re, im} - Keep this at {re: 1, im: 0}
    }

    isEven(z) {
        return Math.abs(z.re + z.im) % 2 === 0;
    }

    step(z) {
        if (this.isEven(z)) {
            return { re: (z.re + z.im) / 2, im: (z.im - z.re) / 2 };
        } else {
            return {
                re: (this.alpha.re * z.re - this.alpha.im * z.im) + this.beta.re,
                im: (this.alpha.re * z.im + this.alpha.im * z.re) + this.beta.im
            };
        }
    }

    // THE COOKIE CUTTER: Checks if point z (scaled) is in the Mandelbrot Set
    isInMandelbrot(z, scale = 0.01) {
        let cx = z.re * scale;
        let cy = z.im * scale;
        let x = 0, y = 0;
        
        // Standard Mandelbrot iteration: z = z^2 + c
        for (let i = 0; i < 100; i++) {
            let xNew = x*x - y*y + cx;
            let yNew = 2*x*y + cy;
            x = xNew;
            y = yNew;
            if (x*x + y*y > 4) return false; // Escaped!
        }
        return true; // Stayed stable (In the set)
    }

    runExperiment(startZ, iterations = 100) {
        let current = startZ;
        for (let i = 0; i < iterations; i++) {
            current = this.step(current);
            if (current.re ** 2 + current.im ** 2 > 1000000) break;
        }
        // Return if the final resting point is in our "Cookie Cutter"
        return {
            finalPoint: current,
            isStableInMandel: this.isInMandelbrot(current)
        };
    }
}

// TEST RUN with your B=1 "Gold Mine"
// --- MASTER EXECUTION BLOCK ---
// --- GALAXY SCANNER (N=1000) ---
const fs = require('fs');
const scanner = new GaussianCollatz({re: 3, im: 0}, {re: 1, im: 0});
const GOLDEN_SCALE = 0.0001;
const TEST_LIMIT = 1000;

let matches = 0;
let resultsData = "Input, Final_RE, Final_IM, Mandelbrot_Match\n";

console.log(`🚀 Scanning the Galaxy (N=${TEST_LIMIT}) at Scale ${GOLDEN_SCALE}...`);

for (let i = 1; i <= TEST_LIMIT; i++) {
    const res = scanner.runExperiment({re: i, im: 0});
    const isMatch = scanner.isInMandelbrot(res.finalPoint, GOLDEN_SCALE);
    
    if (isMatch) matches++;
    
    // Log the data row
    resultsData += `${i}, ${res.finalPoint.re}, ${res.finalPoint.im}, ${isMatch}\n`;
}

const successRate = ((matches / TEST_LIMIT) * 100).toFixed(2);

console.log(`\n--- SCAN COMPLETE ---`);
console.log(`Total Matches: ${matches} / ${TEST_LIMIT}`);
console.log(`Success Rate: ${successRate}%`);

// Save the full dataset for your Paper 3
fs.writeFileSync('experiments/galaxy_scan_1000.csv', resultsData);
console.log(`📊 Full dataset saved to experiments/galaxy_scan_1000.csv`);