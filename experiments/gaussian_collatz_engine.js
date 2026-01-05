const fs = require('fs');
const path = require('path');

if (!fs.existsSync('experiments')) fs.mkdirSync('experiments');

// Helper to prevent overwriting: finds a unique filename
function getUniqueFileName(basePath) {
    let counter = 1;
    let ext = path.extname(basePath);
    let name = basePath.slice(0, -ext.length);
    let newPath = basePath;
    while (fs.existsSync(newPath)) {
        newPath = `${name}_v${counter}${ext}`;
        counter++;
    }
    return newPath;
}

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

    // Applies H-C v2: Logarithmic Magnitude [cite: 2025-12-16]
    applyHCv2(z, C_const = 1) {
        const A = z.re || 0.000001; // Prevent div by zero
        const B = z.im || 0.000001;
        const C = C_const;

        const logRatio = Math.log(Math.abs(B / A));
        const phase = (B * Math.PI) / A;
        const magnitude = C / A;

        return {
            h_re: magnitude * logRatio * Math.cos(phase),
            h_im: magnitude * logRatio * Math.sin(phase)
        };
    }

    isInMandelbrot(z, scale) {
        let cx = z.re * scale;
        let cy = z.im * scale;
        let x = 0, y = 0;
        for (let i = 0; i < 100; i++) {
            let xNew = x*x - y*y + cx;
            let yNew = 2*x*y + cy;
            x = xNew; y = yNew;
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
const BETAS = [{re: 1, im: 0}, {re: 2, im: 0}, {re: 1, im: 1}];

let summaryReport = "Beta,Scale,ResidencyRate,UniqueSinks\n";

BETAS.forEach((beta) => {
    const runner = new GaussianCollatz({re: 3, im: 0}, beta);
    SCALES.forEach((scale) => {
        let matches = 0;
        const sinks = new Set();
        let rawData = "Final_RE,Final_IM,Is_Stable,HCv2_RE,HCv2_IM\n";

        for (let i = 1; i <= SAMPLE_SIZE; i++) {
            const finalPoint = runner.runExperiment({re: i, im: 0});
            const isStable = runner.isInMandelbrot(finalPoint, scale);
            if (isStable) matches++;
            
            // Apply the Refined Hypothesis [cite: 2025-12-16]
            const hc = runner.applyHCv2(finalPoint);
            
            sinks.add(`${finalPoint.re.toFixed(4)},${finalPoint.im.toFixed(4)}`);
            rawData += `${finalPoint.re},${finalPoint.im},${isStable ? 1 : 0},${hc.h_re},${hc.h_im}\n`;
        }

        const rawFileName = getUniqueFileName(`experiments/raw_data_B${beta.re}_i${beta.im}_S${scale}.csv`);
        fs.writeFileSync(rawFileName, rawData);

        const rate = ((matches / SAMPLE_SIZE) * 100).toFixed(2);
        summaryReport += `${beta.re}+${beta.im}i,${scale},${rate},${sinks.size}\n`;
    });
});

const summaryFileName = getUniqueFileName(`experiments/stress_test_baseline_v4.csv`);
fs.writeFileSync(summaryFileName, summaryReport);
console.log(`✅ Data exported to ${summaryFileName}. No files were overwritten.`);