#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const args = process.argv.slice(2);

if (args[0] === 'run' && args[1]) {
  const filePath = path.resolve(args[1]);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }

  runEggCode(filePath);
} else {
  console.log('Usage: egg run <filename.egg>');
  process.exit(1);
}

function runEggCode(filePath) {
  console.log(`🐣 Running Egg code via Python interpreter...\n`);

  // Path to your Python interpreter script (egg.py)
  const eggPyPath = path.resolve(__dirname, '../egg.py');

  // Spawn python3 process with egg.py and the .egg file as argument
  const pythonProcess = spawn('python3', [eggPyPath, filePath], { stdio: 'inherit' });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python interpreter exited with code ${code}`);
      process.exit(code);
    }
  });
}
