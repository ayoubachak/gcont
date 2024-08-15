# gcont

`gcont` is a command-line tool designed to help developers gather important code files and generate a documentation context in Markdown format. It can automatically detect the project type, include/exclude specific files, and support Git integration to document only changed files.

## Features

- **Automatic Project Detection**: Automatically detects the type of project (e.g., Django, Flask, React) and applies relevant file gathering rules.
- **Customizable**: Supports include and exclude patterns via command-line arguments or a configuration file (`config.gcont.yml`).
- **Git Integration**: Optionally gathers only the files that have changed since the last Git commit.
- **Markdown Output**: Generates a `context.md` file that includes the gathered files, organized and syntax-highlighted for easy reference.

## Installation

You can install `gcont` via `pip`:

```bash
pip install gcont
```

## Usage

### Basic Usage

To run `gcont` with default settings:

```bash
gcont --root /path/to/your/project
```

Or if you are already in the directory, you can just run 
```bash
gcount
```

### Custom Include/Exclude Patterns

You can specify additional include or exclude patterns:

```bash
gcont --include '*.html' '*.css' --exclude '*.log' '*.tmp'
```

### Using a Configuration File (Optional)

Create a `config.gcont.yml` in your project root directory to avoid passing options every time:

```yaml
project: react
root: .
include:
  - '*.html'
  - '*.css'
exclude:
  - '*.test.js'
  - '*.test.jsx'
  - 'node_modules/*'
git_diff: false
verbose: true
```

Then simply run:

```bash
gcont
```

### Git Integration

To gather only files that have changed since the last Git commit:

```bash
gcont --git-diff
```

## Development

### Running Tests

To run the tests for this project:

```bash
pytest
```


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please feel free to reach out.
