const fs = require('fs');

// v2: Added a timestamp so every run is unique
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const outputCSV = `experiments/stress_test_v2_${timestamp}.csv`;

class GaussianCollatz {
    constructor(alpha, beta) {
        this.alpha = alpha;
        this.beta = beta;
    }

    isEven(z) {
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

const SCALES = [0.001, 0.0001, 0.00001];
const SAMPLE_SIZE = 1000;
const BETAS = [
    {re: 1, im: 0}, 
    {re: 2, im: 0}, 
    {re: 1, im: 1}  
];

let finalReport = "Beta,Scale,ResidencyRate,UniqueSinks\n";

console.log(`🧪 Running V2: Cleaning up the "Garbage" results...`);

BETAS.forEach((beta, bIndex) => {
    // Fresh runner for every Beta
    const runner = new GaussianCollatz({re: 3, im: 0}, beta);
    
    SCALES.forEach((scale, sIndex) => {
        let matches = 0;
        const sinks = new Set();

        // This loop ensures we aren't just repeating the same point
        for (let i = 1; i <= SAMPLE_SIZE; i++) {
            const finalPoint = runner.runExperiment({re: i, im: 0});
            sinks.add(`${finalPoint.re.toFixed(4)},${finalPoint.im.toFixed(4)}`);
            if (runner.isInMandelbrot(finalPoint, scale)) matches++;
        }

        const rate = ((matches / SAMPLE_SIZE) * 100).toFixed(2);
        const betaLabel = `${beta.re}+${beta.im}i`;
        
        console.log(`> Beta: ${betaLabel} | Scale: ${scale} | Rate: ${rate}%`);
        finalReport += `${betaLabel},${scale},${rate},${sinks.size}\n`;
        
        // Note: If you have a draw function, call it HERE 
        // passing (beta, scale) to ensure the image is unique!
    });
});

fs.writeFileSync(outputCSV, finalReport);
console.log(`\n✅ Success. V2 Data saved to: ${outputCSV}`);