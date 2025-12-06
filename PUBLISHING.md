# Publishing to PyPI

This document describes how to publish new versions of the `polinations` package to PyPI.

## Automated Publishing (Recommended)

The repository is configured with GitHub Actions to automatically publish to PyPI when a new release is created.

### Publishing a New Release

1. Update the version number in `pyproject.toml` and `polinations/__init__.py`
2. Commit and push your changes
3. Create a new release on GitHub:
   - Go to the repository's "Releases" page
   - Click "Draft a new release"
   - Create a new tag (e.g., `v0.1.1`)
   - Fill in the release title and description
   - Click "Publish release"
4. The GitHub Actions workflow will automatically:
   - Build the package
   - Publish it to PyPI

### Testing with TestPyPI

You can test the publishing process using TestPyPI before publishing to the real PyPI:

1. Go to the "Actions" tab in the repository
2. Select the "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select "true" for the TestPyPI option
5. The package will be published to https://test.pypi.org/

## Manual Publishing (Alternative)

If you need to publish manually:

### Prerequisites

```bash
pip install build twine
```

### Build the Package

```bash
# Clean any previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/polinations-X.Y.Z.tar.gz` (source distribution)
- `dist/polinations-X.Y.Z-py3-none-any.whl` (wheel distribution)

### Verify the Package

```bash
# Check the package metadata (note: may show warnings, but package is valid)
twine check dist/*

# Install locally to test
pip install dist/polinations-*.whl
```

### Publish to PyPI

```bash
# Upload to PyPI (requires PyPI credentials)
twine upload dist/*
```

Or to TestPyPI first:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

## Configuration

The package configuration is defined in:

- **`pyproject.toml`** - Main package metadata and build configuration
- **`setup.py`** - Minimal setup file for backward compatibility
- **`.github/workflows/publish-to-pypi.yml`** - GitHub Actions workflow for automated publishing

## GitHub Environments

The GitHub Actions workflow uses GitHub Environments for security:

- **`pypi`** - Production PyPI environment
- **`testpypi`** - TestPyPI environment for testing

These environments use Trusted Publishing (OIDC) which eliminates the need for API tokens. The repository maintainers need to configure these environments in the repository settings.

## Setting up Trusted Publishing

To enable automated publishing, the repository owner needs to:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new "pending publisher":
   - PyPI Project Name: `polinations`
   - Owner: `gpt4free`
   - Repository name: `polinations`
   - Workflow name: `publish-to-pypi.yml`
   - Environment name: `pypi`

Repeat for TestPyPI at https://test.pypi.org/manage/account/publishing/

## Version Management

Version numbers should follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner  
- **PATCH** version for backward compatible bug fixes

Update the version in both locations (keep them in sync):
1. `pyproject.toml` (line with `version = "X.Y.Z"`)
2. `polinations/__init__.py` (line with `__version__ = "X.Y.Z"`)

**Note**: Future improvement could use dynamic versioning with `setuptools_scm` or read version from `__init__.py` to maintain a single source of truth.
