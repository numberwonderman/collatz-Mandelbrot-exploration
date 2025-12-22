const fs = require('fs');

class GaussianCollatz {
    constructor(alpha, beta) {
        this.alpha = alpha; // {re, im} 
        this.beta = beta;   // {re, im}
    }

    isEven(z) {
        // Your established parity rule
        return (Math.abs(z.re) + Math.abs(z.im)) % 2 === 0;
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

    isInMandelbrot(z, scale) {
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
        return current;
    }
}

// --- AUTOMATED STRESS TEST SUITE ---
const SCALES = [0.001, 0.0001, 0.00001]; // Testing scale sensitivity
const SAMPLE_SIZE = 1000;
const BETAS = [
    {re: 1, im: 0}, // Your current B=1
    {re: 2, im: 0}, // Integer Shift
    {re: 1, im: 1}  // Complex Shift (i+1)
];

let finalReport = "Beta,Scale,ResidencyRate,UniqueSinks\n";

console.log(`🧪 Starting Stress Tests for Mr K...`);

BETAS.forEach(beta => {
    const runner = new GaussianCollatz({re: 3, im: 0}, beta);
    
    SCALES.forEach(scale => {
        let matches = 0;
        const sinks = new Set();

        for (let i = 1; i <= SAMPLE_SIZE; i++) {
            const finalPoint = runner.runExperiment({re: i, im: 0});
            sinks.add(`${finalPoint.re},${finalPoint.im}`);
            if (runner.isInMandelbrot(finalPoint, scale)) matches++;
        }

        const rate = ((matches / SAMPLE_SIZE) * 100).toFixed(2);
        const betaLabel = `${beta.re}+${beta.im}i`;
        
        console.log(`> Beta: ${betaLabel.padEnd(5)} | Scale: ${scale.toString().padEnd(7)} | Rate: ${rate}%`);
        finalReport += `${betaLabel},${scale},${rate},${sinks.size}\n`;
    });
});

fs.writeFileSync('experiments/stress_test_master.csv', finalReport);
console.log(`\n✅ Done. Results saved to experiments/stress_test_master.csv`);