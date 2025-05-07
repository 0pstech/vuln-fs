#!/usr/bin/env node

const { execSync } = require('child_process');
const { PythonShell } = require('python-shell');
const path = require('path');

// main.py (또는 실제 이름이 main.py가 아니라면 그 파일 이름) 실행
const scriptPath = path.join(__dirname, 'main.py');
PythonShell.run(scriptPath, { stdio: 'inherit' }, function (err) {
  if (err) {
    console.error('[vuln-fs] Failed to run main.py:', err);
    process.exit(1);
  }
});
