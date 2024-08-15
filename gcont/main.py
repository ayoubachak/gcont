import argparse
import os

import os
import fnmatch
import argparse
import subprocess
import yaml

# Map of file extensions to programming languages for code block syntax highlighting
EXTENSION_TO_LANGUAGE = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    '.xml': 'xml',
}

def detect_project_type(root_dir):
    """Detect the type of project based on common file structures."""
    if os.path.exists(os.path.join(root_dir, 'manage.py')) and os.path.exists(os.path.join(root_dir, 'requirements.txt')):
        return "django"
    elif os.path.exists(os.path.join(root_dir, 'app.py')) and os.path.exists(os.path.join(root_dir, 'requirements.txt')):
        return "flask"
    elif os.path.exists(os.path.join(root_dir, 'package.json')):
        if os.path.exists(os.path.join(root_dir, 'pages')) and os.path.exists(os.path.join(root_dir, 'next.config.js')):
            return "nextjs"
        elif os.path.exists(os.path.join(root_dir, 'src/App.js')) or os.path.exists(os.path.join(root_dir, 'src/App.tsx')):
            return "react"
        return "nodejs"
    elif os.path.exists(os.path.join(root_dir, 'pom.xml')):
        return "spring_boot"
    elif os.path.exists(os.path.join(root_dir, 'setup.py')) or os.path.exists(os.path.join(root_dir, 'pyproject.toml')):
        return "python_package"
    else:
        return "generic"

def detect_unwanted_directories(root_dir):
    """Detect common directories that should be excluded, such as node_modules, build, dist."""
    unwanted_dirs = []

    for root, dirs, _ in os.walk(root_dir):
        for d in dirs:
            if d in ["node_modules", "build", "dist", "__pycache__", ".git"]:
                unwanted_dirs.append(os.path.join(root, d))
        break  # Only need to inspect the top-level directories

    return unwanted_dirs

def get_changed_files():
    """Get a list of files that have changed since the last commit."""
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').splitlines()

def gather_code_files(root_dir, include_patterns, exclude_patterns, use_git_diff=False):
    """Gather files based on include and exclude patterns, optionally using Git diff."""
    gathered_files = []
    exclude_dirs = set(detect_unwanted_directories(root_dir))

    if use_git_diff:
        changed_files = get_changed_files()
        for file_path in changed_files:
            file_name = os.path.basename(file_path)
            if any(fnmatch.fnmatch(file_name, pattern) for pattern in exclude_patterns):
                continue
            if any(fnmatch.fnmatch(file_path, pattern) for pattern in include_patterns):
                gathered_files.append(file_path)
    else:
        for root, dirs, files in os.walk(root_dir):
            # Debugging: print current directory
            print(f"Traversing directory: {root}")

            # Exclude directories detected dynamically
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]

            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                
                # Skip files in excluded directories or matching exclude patterns
                if any(fnmatch.fnmatch(file_name, pattern) for pattern in exclude_patterns):
                    continue

                # Check if the file matches any of the include patterns
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in include_patterns):
                    gathered_files.append(file_path)
    
    # Debugging: Print excluded directories
    if exclude_dirs:
        print("Excluded directories:")
        for d in exclude_dirs:
            print(f"- {d}")

    return gathered_files

def get_language_by_extension(file_path):
    """Determine the language based on the file extension."""
    _, ext = os.path.splitext(file_path)
    return EXTENSION_TO_LANGUAGE.get(ext, '')

def write_to_context_md(gathered_files, output_file="context.md"):
    """Write gathered files to a Markdown file."""
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for file_path in gathered_files:
            language = get_language_by_extension(file_path)
            md_file.write(f"## {file_path}\n\n")
            md_file.write(f"```{language}\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as code_file:
                    md_file.write(code_file.read())
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {file_path}")
            md_file.write("\n```\n\n")

def get_patterns_by_project_type(project_type):
    """Return include and exclude patterns based on the project type."""
    global_exclude_patterns = [".git/*", "*__pycache__/*", "*.egg-info/*"]
    
    if project_type == "django":
        include_patterns = ["*.py"]
        exclude_patterns = ["test_*.py", "*.md", "migrations/*"]
    elif project_type == "flask":
        include_patterns = ["*.py"]
        exclude_patterns = ["test_*.py", "*.md"]
    elif project_type == "nodejs":
        include_patterns = ["*.js", "*.ts"]
        exclude_patterns = ["*.test.js", "*.md"]
    elif project_type == "react":
        include_patterns = ["*.js", "*.jsx", "*.ts", "*.tsx"]
        exclude_patterns = ["*.test.js", "*.test.jsx", "*.md"]
    elif project_type == "nextjs":
        include_patterns = ["*.js", "*.jsx", "*.ts", "*.tsx"]
        exclude_patterns = ["*.test.js", "*.test.jsx", "*.test.ts", "*.test.tsx", "*.md"]
    elif project_type == "spring_boot":
        include_patterns = ["*.java", "*.xml"]
        exclude_patterns = ["*.md", "target/*"]
    elif project_type == "python_package":
        include_patterns = ["*.py"]
        exclude_patterns = ["test_*.py", "*.md", "build/*", "dist/*"]
    else:  # Generic
        include_patterns = ["*.py", "*.js", "*.java", "*.html", "*.css"]
        exclude_patterns = ["test_*.py", "*.test.js", "*.md"]

    return include_patterns, global_exclude_patterns + exclude_patterns

def load_config_from_yaml(root_dir):
    """Load configuration from config.gcont.yml if it exists."""
    config_path = os.path.join(root_dir, 'config.gcont.yml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    return {}


def main():
    parser = argparse.ArgumentParser(description="Gather important code files for context documentation.")
    parser.add_argument("--project", type=str, help="Specify the project type (e.g., django, flask, nodejs, react, nextjs, spring_boot, python_package, generic).")
    parser.add_argument("--root", type=str, default=".", help="Specify the root directory to search for files.")
    parser.add_argument("--include", type=str, nargs='*', help="Additional include patterns (e.g., '*.html', '*.css').")
    parser.add_argument("--exclude", type=str, nargs='*', help="Additional exclude patterns (e.g., '*.log', '*.tmp').")
    parser.add_argument("--git-diff", action='store_true', help="Only include files that have changed since the last commit.")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose output to list all gathered files before writing them.")
    args = parser.parse_args()

    # Load configuration from YAML if available
    yaml_config = load_config_from_yaml(args.root)
    
    # Override command-line arguments with YAML configuration if present
    project_type = yaml_config.get('project', args.project)
    if not project_type:
        project_type = detect_project_type(args.root)
    else:
        project_type = project_type.lower()

    root_dir = yaml_config.get('root', args.root)
    include_patterns = yaml_config.get('include', args.include) or []
    exclude_patterns = yaml_config.get('exclude', args.exclude) or []
    use_git_diff = yaml_config.get('git_diff', args.git_diff)
    verbose = yaml_config.get('verbose', args.verbose)

    print(f"Detected project type: {project_type}")

    # Get default patterns based on project type
    default_include_patterns, default_exclude_patterns = get_patterns_by_project_type(project_type)
    include_patterns = default_include_patterns + include_patterns
    exclude_patterns = default_exclude_patterns + exclude_patterns

    # Gather the code files
    gathered_files = gather_code_files(root_dir, include_patterns, exclude_patterns, use_git_diff=use_git_diff)

    # Verbose output: List all gathered files before writing them
    if verbose:
        print("\nGathered files:")
        for file in gathered_files:
            print(f"- {file}")
        print("\n")

    # Write the gathered files to context.md
    write_to_context_md(gathered_files)
    
    print(f"Context.md file has been generated with {len(gathered_files)} files.")

if __name__ == "__main__":
    main()
