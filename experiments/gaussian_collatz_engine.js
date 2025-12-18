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
const fs = require('fs');
const masterEngine = new GaussianCollatz({re: 3, im: 0}, {re: 1, im: 0});
const scales = [0.0001, 0.0002, 0.0005, 0.001];

let logContent = "--- GALAXY INTEGER DISCOVERY LOG ---\n";
logContent += `Date: ${new Date().toLocaleString()}\n`;
logContent += "Hypothesis: Gaussian Collatz resting points inhabit the Mandelbrot Set at 10^-4 scale.\n\n";

console.log("🚀 Starting Discovery Run...");

[7, 13, 27].forEach(input => {
    const result = masterEngine.runExperiment({re: input, im: 0});
    logContent += `Input ${input} landed at: (${result.finalPoint.re}, ${result.finalPoint.im})\n`;
    
    scales.forEach(s => {
        const isMatch = masterEngine.isInMandelbrot(result.finalPoint, s);
        logContent += `  Scale ${s}: ${isMatch ? "✅ MATCH!" : "❌ Miss"}\n`;
    });
    logContent += "\n";
});

// Save to the experiments folder
try {
    fs.writeFileSync('experiments/discovery_log.txt', logContent);
    console.log("📁 Success! Evidence saved to experiments/discovery_log.txt");
    console.log(logContent); // Also print it so you can see it now
} catch (err) {
    // Fallback if folder structure is different
    fs.writeFileSync('discovery_log.txt', logContent);
    console.log("📁 Saved to root directory as discovery_log.txt");
}