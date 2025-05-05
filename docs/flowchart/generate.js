// Used to convert .mermaid files to .svg using mermaid-cli
// This script reads all .mermaid files in the current directory, converts them to SVG using mermaid-cli, and saves them with the same name but with a .svg extension.
// It also checks for a corresponding .css file for each .mermaid file and applies the styles if available.
// Usage: node generate.js
// Ensure you have mermaid-cli installed globally or adjust the path to the mmdc executable accordingly.
// Make sure to run this script in the directory where your .mermaid files are located.
// This script uses Node.js built-in modules: fs, path, and child_process.

// npm install @mermaid-js/mermaid-cli

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function convertMermaidToSvg(mermaidCode, css = '') {
  const tempDir = fs.mkdtempSync('mermaid-');
  const inputPath = path.join(tempDir, 'input.mmd');
  const cssPath = path.join(tempDir, 'style.css');
  const outputPath = path.join(tempDir, 'output.svg');

  try {
    fs.writeFileSync(inputPath, mermaidCode);
    if (css) fs.writeFileSync(cssPath, css);

    let command = `../../node_modules/.bin/mmdc -i "${inputPath}" -o "${outputPath}" --quiet`;
    if (css) command += ` --cssFile "${cssPath}"`;

    execSync(command);
    return fs.readFileSync(outputPath, 'utf-8');
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

function processMermaidFiles() {
  const currentDir = process.cwd();
  
  // Get all .mermaid files
  const mermaidFiles = fs.readdirSync(currentDir)
    .filter(file => file.endsWith('.mermaid'));

  if (!mermaidFiles.length) {
    console.log('No .mermaid files found in directory');
    return;
  }

  // Process each file
  mermaidFiles.forEach(file => {
    const baseName = path.basename(file, '.mermaid');
    const svgFile = `${baseName}.svg`;
    
    try {
      // Read Mermaid content
      const mermaidContent = fs.readFileSync(file, 'utf-8');
      
      // Check for matching CSS file
      let cssContent = '';
      const cssFile = `${baseName}.css`;
      if (fs.existsSync(cssFile)) {
        cssContent = fs.readFileSync(cssFile, 'utf-8');
      }

      // Convert to SVG
      const svgContent = convertMermaidToSvg(mermaidContent, cssContent);
      
      // Save SVG
      fs.writeFileSync(svgFile, svgContent);
      console.log(`Converted ${file} -> ${svgFile}`);
    } catch (err) {
      console.error(`Error processing ${file}:`, err.message);
    }
  });
}

// Run the conversion
processMermaidFiles();