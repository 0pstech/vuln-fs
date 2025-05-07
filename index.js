#!/usr/bin/env node

const { PythonShell } = require('python-shell');
const path = require('path');

// main.py의 절대경로
const scriptPath = path.join(__dirname, 'main.py');

// PythonShell을 사용해 main.py 실행
PythonShell.run(scriptPath, { stdio: 'inherit' }, function (err) {
  if (err) {
    console.error('Failed to run main.py:', err);
    process.exit(1);
  }
});