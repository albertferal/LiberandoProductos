module.exports = {
    branches: ['main'], // Rama principal de tu repositorio
    plugins: [
      '@semantic-release/commit-analyzer',
      '@semantic-release/release-notes-generator',
      '@semantic-release/changelog',
      '@semantic-release/github',
      '@semantic-release/git',
    ],
  };
  