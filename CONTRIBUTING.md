# Contributing to GIFverse

Thank you for your interest in contributing to GIFverse! This document provides guidelines for contributing to the project.

## Commit Message Convention

This project uses [Conventional Commits](https://conventionalcommits.org/) for commit messages. This allows for automated versioning and changelog generation.

### Commit Message Format

```txt
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

### Examples

```bash
feat: add support for animated GIF processing
fix: resolve memory leak in image processing
docs: update API documentation
style: format code according to PEP 8
refactor: extract GIF validation logic into separate function
perf: optimize image resizing algorithm
test: add unit tests for GIF processor
chore: update dependencies
```

### Breaking Changes

If your commit introduces a breaking change, add `BREAKING CHANGE:` in the footer:

```bash
feat: change API endpoint structure

BREAKING CHANGE: The /api/gif endpoint has been moved to /api/v2/gif
```

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies
5. Run tests

```bash
git clone https://github.com/your-username/gifverse.git
cd gifverse
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the commit message convention
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Release Process

This project uses semantic-release for automated versioning and releases. The release process is triggered by:

- Pushes to the `main` branch
- Manual workflow dispatch

The version is determined by analyzing commit messages according to the Conventional Commits specification.
