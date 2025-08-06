# Course Instance Setup Script

This Python script automates the creation and configuration of new course instances from the course-site-myst template.

## Features

- Creates new GitHub repositories from the course-site-myst template
- Automatically extracts course information from landing page repositories
- Updates `myst.yml` and `index.md` with course-specific information
- Supports dry-run mode to preview changes
- Auto-detects courses directory structure
- Can skip repository creation for existing repos

## Prerequisites

- Python 3.6+
- GitHub CLI (`gh`) installed and authenticated
- Access to the course-site-myst template repository

## Usage

### Basic Usage

Create a new course instance (run from your courses directory):

```bash
python setup-course-instance.py stat2 fall-2025
```

### Update Existing Repository

If you've already created the repository manually and just want to update the files:

```bash
python setup-course-instance.py stat2 fall-2025 --skip-repo-creation
```

### Dry Run

Preview what changes would be made without actually executing them:

```bash
python setup-course-instance.py stat2 fall-2025 --dry-run
```

### Custom Courses Directory

Specify a different courses directory:

```bash
python setup-course-instance.py stat2 fall-2025 --courses-dir /path/to/your/courses
```

## Directory Structure

The script expects the following directory structure:

```
{parent}/
├── course-site-myst/           # Template repository (this script)
├── stat2/
│   ├── berkeley-stat2.github.io/  # Landing page repository
│   └── fall-2025/                 # Course instance (created by script)
├── stat133/
│   ├── berkeley-stat133.github.io/
│   ├── fall-2024/
│   └── spring-2025/
└── ...
```

## What It Does

1. **Repository Creation**: Uses GitHub CLI to create a new repository from the course-site-myst template
2. **Information Extraction**: Reads course information from the landing page README.md:
   - Course title from the main heading
   - Course description from the Overview section
3. **File Updates**: Updates the following files in the new repository:
   - `myst.yml`: Updates project title, description, authors, GitHub URL, and domain
   - `index.md`: Updates title, subtitle, and course references

## Command Line Options

- `course_name`: Course name (e.g., stat2)
- `semester`: Semester in format season-year (e.g., fall-2025)
- `--dry-run`: Show what would be done without executing
- `--courses-dir`: Path to courses directory (auto-detected by default)
- `--skip-repo-creation`: Skip repository creation (use if repo already exists)

## Examples

```bash
# Standard usage from courses directory
cd ~/proj/courses
python course-site-myst/setup-course-instance.py stat2 fall-2025

# Update existing repo from anywhere
python ~/proj/courses/course-site-myst/setup-course-instance.py stat2 fall-2025 \
  --skip-repo-creation \
  --courses-dir ~/proj/courses

# Preview changes
python setup-course-instance.py stat156 spring-2025 --dry-run
```

## After Running the Script

The script will create/update your course repository. You'll still need to:

1. Review and customize the generated `myst.yml` file
2. Update `index.md` with actual instructor/GSI information
3. Customize `schedule.yml` with your course schedule
4. Update `syllabus.md`, `calendar.md`, and other content files
5. Commit and push your changes

The script will display these next steps after completion.
