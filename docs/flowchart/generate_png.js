const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const outputDir = path.join(__dirname, 'png');
fs.mkdirSync(outputDir, { recursive: true });

const mermaidFiles = fs.readdirSync(__dirname)
  .filter(file => path.extname(file).toLowerCase() === '.mermaid');

if (mermaidFiles.length === 0) {
  console.log('No .mermaid files found in the current directory');
  process.exit(0);
}

mermaidFiles.forEach(file => {
  const inputPath = path.join(__dirname, file);
  const outputPath = path.join(outputDir, path.basename(file, '.mermaid') + '.png');
  
  const result = spawnSync(
    path.join(__dirname, '../../node_modules/.bin/mmdc'),
    [
    //   '-t', 'dark',
      '-b', 'transparent',
      '-i', inputPath,
      '-o', outputPath
    ],
    {
      stdio: 'inherit' 
    }
  );

  if (result.error) {
    console.error(`Error converting ${file}:`, result.error.message);
  } else {
    console.log(`Successfully converted ${file} to ${outputPath}`);
  }
});

console.log('\nConversion complete!');