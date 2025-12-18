const fs = require('fs');

class GaussianCollatz {
    constructor(alpha, beta) {
        this.alpha = alpha; // {re, im} 
        this.beta = beta;   // {re, im}
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

    isInMandelbrot(z, scale = 0.0001) {
        let cx = z.re * scale;
        let cy = z.im * scale;
        let x = 0, y = 0;
        for (let i = 0; i < 100; i++) {
            let xNew = x*x - y*y + cx;
            let yNew = 2*x*y + cy;
            x = xNew;
            y = yNew;
            if (x*x + y*y > 4) return false;
        }
        return true;
    }

    runExperiment(startZ, iterations = 100) {
        let current = startZ;
        for (let i = 0; i < iterations; i++) {
            current = this.step(current);
            if (current.re ** 2 + current.im ** 2 > 1000000) break;
        }
        return { finalPoint: current };
    }
}

// --- EXECUTION ---
const runner = new GaussianCollatz({re: 3, im: 0}, {re: 1, im: 0});
const GOLDEN_SCALE = 0.0001;
const TEST_LIMIT = 1000;

let finalMatches = 0;
let resultsData = "Input,Final_RE,Final_IM,Magnitude,Mandel_Match\n";
const uniqueDestinations = new Set();

console.log(`🚀 Running Sanity Check on ${TEST_LIMIT} points...`);

for (let i = 1; i <= TEST_LIMIT; i++) {
    const res = runner.runExperiment({re: i, im: 0});
    const posKey = `${res.finalPoint.re},${res.finalPoint.im}`;
    uniqueDestinations.add(posKey);
    
    const isMatch = runner.isInMandelbrot(res.finalPoint, GOLDEN_SCALE);
    if (isMatch) finalMatches++;
    
    const mag = Math.sqrt(res.finalPoint.re**2 + res.finalPoint.im**2).toFixed(2);
    resultsData += `${i},${res.finalPoint.re},${res.finalPoint.im},${mag},${isMatch}\n`;
}

console.log(`\n--- SANITY CHECK RESULTS ---`);
console.log(`Unique Destinations Found: ${uniqueDestinations.size}`);
console.log(`Mandelbrot Success Rate: ${((finalMatches / TEST_LIMIT) * 100).toFixed(2)}%`);

if (uniqueDestinations.size === 1) {
    console.log("⚠️ RAT DETECTED: Everything is landing in the same hole.");
} else if (uniqueDestinations.size < 20) {
    console.log("🧐 SEMI-STABLE: There are a few common 'sinks' (Star Systems).");
} else {
    console.log("🌌 GALAXY CONFIRMED: The points are distributing across the complex plane.");
}

fs.writeFileSync('experiments/galaxy_scan_1000.csv', resultsData);
console.log(`📊 Dataset saved: experiments/galaxy_scan_1000.csv`);