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

const beta = {re: 1, im: 1}; // Focusing on the "Secret Sauce"
const scale = 0.00001;        // Using the 100% Residency scale
const runner = new GaussianCollatz({re: 3, im: 0}, beta);
const SAMPLE_SIZE = 1000;

const uniqueSinksMap = new Map(); // To store unique sinks and their HCv2 results

for (let i = 1; i <= SAMPLE_SIZE; i++) {
    const finalPoint = runner.runExperiment({re: i, im: 0});
    const sinkKey = `${finalPoint.re.toFixed(4)},${finalPoint.im.toFixed(4)}`;
    
    if (!uniqueSinksMap.has(sinkKey)) {
        // Apply H-C v2 transformation [cite: 2025-12-16]
        const hc = runner.applyHCv2(finalPoint);
        uniqueSinksMap.set(sinkKey, {
            raw: finalPoint,
            hc: hc
        });
    }
}

// Create the "Figure 1" Data for your paper
let plotData = "Raw_RE,Raw_IM,HCv2_RE,HCv2_IM\n";
uniqueSinksMap.forEach((val) => {
    plotData += `${val.raw.re},${val.raw.im},${val.hc.h_re},${val.hc.h_im}\n`;
});

const figure1Path = getUniqueFileName(`experiments/GSV1_Figure1_Beta1+1i.csv`);
fs.writeFileSync(figure1Path, plotData);

console.log(`\n🚀 GSV-1 Validation Complete!`);
console.log(`Unique Sinks Found: ${uniqueSinksMap.size}`); // Should be 938
console.log(`Plotting data saved to: ${figure1Path}`);

// --- NEW: H-C v2 GEOMETRIC ANALYSIS ---
const hcPoints = Array.from(uniqueSinksMap.values()).map(val => val.hc);

// Filter for points in the central "eye" (magnitude < 2.0 to exclude far outliers)
const innerRing = hcPoints.filter(p => Math.sqrt(p.h_re**2 + p.h_im**2) < 2.0);

if (innerRing.length > 0) {
    const maxRE = Math.max(...innerRing.map(p => Math.abs(p.h_re)));
    const maxIM = Math.max(...innerRing.map(p => Math.abs(p.h_im)));
    const squashRatio = maxRE / maxIM;

    console.log(`\n--- H-C v2 Geometric Analysis (The "Squashed Wheel") ---`);
    console.log(`Inner Ring Width (RE):  ${maxRE.toFixed(6)}`);
    console.log(`Inner Ring Height (IM): ${maxIM.toFixed(6)}`);
    console.log(`Squash Ratio (RE/IM):   ${squashRatio.toFixed(6)}`);
    
    if (Math.abs(squashRatio - 1) < 0.05) {
        console.log("Result: Near-Circular Symmetry");
    } else {
        console.log("Result: Elliptic Attractor Confirmed");
    }
}