#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get version from command line argument
const version = process.argv[2];
if (!version) {
  console.error('Usage: node update-readme-version.js <version>');
  process.exit(1);
}

const readmePath = path.join(__dirname, '..', 'README.md');

try {
  // Read README content
  let content = fs.readFileSync(readmePath, 'utf8');

  // Extract major.minor from version (e.g., 1.0.6 -> 1.0)
  const [major, minor] = version.split('.');
  const majorMinor = `${major}.${minor}`;

  // Replace version patterns
  // Replace full version (e.g., 1.0.6)
  content = content.replace(
    /wsams\/gifverse:\d+\.\d+\.\d+/g,
    `wsams/gifverse:${version}`
  );

  // Replace major.minor version (e.g., 1.0)
  content = content.replace(
    /wsams\/gifverse:\d+\.\d+(?![\.\d])/g,
    `wsams/gifverse:${majorMinor}`
  );

  // Write updated content back
  fs.writeFileSync(readmePath, content, 'utf8');

  console.log(`✅ Updated README.md with version ${version} (${majorMinor})`);
} catch (error) {
  console.error('❌ Error updating README:', error.message);
  process.exit(1);
}
