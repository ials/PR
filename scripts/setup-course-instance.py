#!/usr/bin/env python3
"""
Course instance setup script

This script automates the creation and configuration of a new course instance
from the course-site-myst template.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

from ruamel.yaml import YAML
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096  # Prevent line wrapping

def run_command(cmd: list, cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def validate_semester(semester: str) -> bool:
    """Validate semester format (fall-2025, spring-2025, etc.)."""
    parts = semester.split('-')
    if len(parts) != 2:
        return False
    
    season, year = parts
    valid_seasons = ['fall', 'spring', 'summer']
    
    if season not in valid_seasons:
        return False
    
    try:
        year_int = int(year)
        return 1900 <= year_int <= 2100  # Reasonable year range
    except ValueError:
        return False


def extract_course_info(landing_page_path: Path) -> Tuple[str, str, str]:
    """Extract course information from the landing page README."""
    readme_path = landing_page_path / "README.md"
    
    if not readme_path.exists():
        print(f"Warning: README.md not found at {readme_path}")
        return "", "", ""
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return "", "", ""
    
    # Extract title from first heading or title field
    title = ""
    title_match = re.search(r'^# (.+?)(?:\s*\{.*\})?$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
    
    # Extract description from Overview section
    description = ""
    overview_match = re.search(
        r'^## Overview\s*\n\n([^\n]+)', 
        content, 
        re.MULTILINE
    )
    if overview_match:
        description = overview_match.group(1).strip()
    
    # Default authors (can be customized)
    authors = "Instructor Name"
    
    return title, description, authors


def format_semester_display(semester: str) -> str:
    """Format semester for display (fall-2025 -> Fall 2025)."""
    parts = semester.split('-')
    season = parts[0].capitalize()
    year = parts[1]
    return f"{season} {year}"


def detect_courses_directory() -> Path:
    """Try to detect the courses directory based on current working directory."""
    cwd = Path.cwd()
    
    # If we're already in a courses directory
    if cwd.name == 'courses':
        return cwd
    
    # If we're in a subdirectory of courses (like stat2, course-site-myst, etc.)
    if cwd.parent.name == 'courses':
        return cwd.parent
    
    # If we're in a deeper subdirectory (like stat2/fall-2024)
    for parent in cwd.parents:
        if parent.name == 'courses':
            return parent
    
    # Default to current directory
    return cwd


def update_myst_yml(course_name: str, semester: str, title: str, description: str, authors: str, dry_run: bool = False) -> None:
    """Update the existing myst.yml file with course-specific information."""
    myst_file = Path('myst.yml')
    
    if not myst_file.exists():
        print(f"Error: myst.yml not found at {myst_file}")
        return
    
    try:
        with open(myst_file, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"Error reading myst.yml: {e}")
        return
    
    # Extract course name and description from title
    # e.g., "Stat 2: Introduction to Statistics" -> "Stat 2" and "Introduction to Statistics"
    if ':' in title:
        course_title = title.split(':')[0].strip()
        course_description = title.split(':', 1)[1].strip()
    else:
        course_title = title
        course_description = description
    
    # Update project fields
    if 'project' not in data:
        data['project'] = {}
    
    data['project']['title'] = course_title
    data['project']['description'] = course_description
    data['project']['authors'] = [authors]
    data['project']['github'] = f"https://github.com/berkeley-{course_name}/{semester}"
    
    # Update site fields
    if 'site' not in data:
        data['site'] = {}
    
    data['site']['title'] = course_title
    data['site']['domains'] = [f"{course_name}.berkeley.edu"]
    
    if dry_run:
        print("\n--- Updated myst.yml content ---")
        from io import StringIO
        stream = StringIO()
        yaml.dump(data, stream)
        print(stream.getvalue())
    else:
        with open(myst_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)


def update_index_md(title: str, semester_display: str, course_name: str, dry_run: bool = False) -> None:
    """Update the existing index.md file with course-specific information."""
    index_file = Path('index.md')
    
    if not index_file.exists():
        print(f"Error: index.md not found at {index_file}")
        return
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading index.md: {e}")
        return
    
    if content.startswith('---'):
        # Parse frontmatter with YAML
        try:
            # Split frontmatter and content
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                body_content = parts[2]
                
                # Parse and update frontmatter using ruamel.yaml to preserve formatting
                from io import StringIO
                frontmatter_stream = StringIO(frontmatter_str)
                frontmatter = yaml.load(frontmatter_stream)
                
                frontmatter['title'] = title
                frontmatter['subtitle'] = f"UC Berkeley, {semester_display}"
                
                # Reconstruct the frontmatter
                updated_frontmatter_stream = StringIO()
                yaml.dump(frontmatter, updated_frontmatter_stream)
                updated_frontmatter = updated_frontmatter_stream.getvalue()
                
                # Reconstruct the file
                updated_content = f"---\n{updated_frontmatter}---{body_content}"
                
                # Update attention block reference in body content (using regex for text processing)
                course_name_formatted = title.split(':')[0].strip() if ':' in title else course_name.replace('stat', 'Stat ')
                updated_content = re.sub(
                    r"(Welcome to \[Week 2\]\(#week2\) of )[^!]*(!)", 
                    f"\\1{course_name_formatted}\\2", 
                    updated_content
                )
            else:
                print("Warning: Could not parse frontmatter properly")
                updated_content = content
                
        except Exception as e:
            print(f"Error parsing frontmatter YAML: {e}")
            updated_content = content
    else:
        print("Warning: No frontmatter found in index.md")
        updated_content = content
    
    if dry_run:
        print("\n--- Updated index.md content ---")
        print(updated_content)
    else:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)


def main():
    parser = argparse.ArgumentParser(
        description="Automate the creation and configuration of a new course instance from the course-site-myst template.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new repo and set it up (run from courses directory)
  python setup-course-instance.py stat2 fall-2025
  
  # Update existing repo files only (skip repo creation)
  python setup-course-instance.py stat2 fall-2025 --skip-repo-creation
  
  # Specify custom courses directory
  python setup-course-instance.py stat2 fall-2025 --courses-dir /path/to/courses
  
  # Dry run to see what would be changed
  python setup-course-instance.py stat2 fall-2025 --dry-run

This script will:
1. Create a new repository from the course-site-myst template (unless skipped)
2. Extract course information from the landing page repository
3. Update myst.yml and index.md with course-specific information
        """
    )
    
    parser.add_argument('course_name', help='Course name (e.g., stat2)')
    parser.add_argument('semester', help='Semester in format season-year (e.g., fall-2025)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without executing')
    parser.add_argument('--courses-dir', type=Path, help='Path to courses directory (default: auto-detect)', default=None)
    parser.add_argument('--skip-repo-creation', action='store_true', help='Skip repository creation (use if repo already exists)')
    
    args = parser.parse_args()
    
    course_name = args.course_name
    semester = args.semester
    courses_dir = args.courses_dir if args.courses_dir else detect_courses_directory()
    
    # Validate semester format
    if not validate_semester(semester):
        print("Error: Semester should be in format 'fall-2025', 'spring-2025', etc.")
        sys.exit(1)
    
    print(f"Setting up course instance: {course_name} for {semester}")
    print(f"Working in courses directory: {courses_dir}")
    
    # Check if we're in dry-run mode
    if args.dry_run:
        print("DRY RUN MODE - No actual changes will be made")
    
    # Create the repository (unless skipped or already exists)
    repo_name = f"berkeley-{course_name}/{semester}"
    semester_dir = courses_dir / course_name / semester
    
    if args.skip_repo_creation:
        print(f"Skipping repository creation for {repo_name} (--skip-repo-creation flag set)")
    elif semester_dir.exists():
        print(f"Directory {semester_dir} already exists. Skipping repository creation.")
        print("Use --skip-repo-creation flag to suppress this message.")
    else:
        print(f"Creating repository {repo_name}...")
        
        if not args.dry_run:
            # Change to the courses directory first
            original_cwd = Path.cwd()
            os.chdir(courses_dir / course_name)
            
            cmd = [
                'gh', 'repo', 'create',
                '--clone', '--public',
                '--template', 'https://github.com/berkeley-cdss/course-site-myst',
                repo_name
            ]
            run_command(cmd)
            
            # Change back to original directory for now
            os.chdir(original_cwd)
    
    # Change to the semester directory for file operations
    if not args.dry_run:
        if semester_dir.exists():
            os.chdir(semester_dir)
        else:
            print(f"Error: Expected directory {semester_dir} does not exist")
            sys.exit(1)
    
    # Check if landing page repository exists locally
    landing_page_path = courses_dir / course_name / f"berkeley-{course_name}.github.io"
    
    if not landing_page_path.exists():
        print(f"Warning: Landing page repository not found at {landing_page_path}")
        print("Please ensure the landing page repository is cloned in the expected location.")
        print("Continuing with default values...")
        course_title = course_name
        course_description = "Course website"
        course_authors = "Instructor Name"
    else:
        print("Found landing page repository. Extracting course information...")
        course_title, course_description, course_authors = extract_course_info(landing_page_path)
        
        # Use defaults if extraction failed
        if not course_title:
            course_title = course_name
        if not course_description:
            course_description = "Course website"
        if not course_authors:
            course_authors = "Instructor Name"
        
        print("Extracted course information:")
        print(f"  Title: {course_title}")
        print(f"  Description: {course_description}")
    
    # Format semester for display
    semester_display = format_semester_display(semester)
    
    # Update files
    if args.dry_run:
        print("\nDRY RUN: Showing what would be updated...")
        print(f"Files would be updated in: {semester_dir}")
        # For dry run, we need to simulate being in the semester directory
        original_cwd = Path.cwd()
        if semester_dir.exists():
            os.chdir(semester_dir)
            update_myst_yml(course_name, semester, course_title, course_description, course_authors, dry_run=True)
            update_index_md(course_title, semester_display, course_name, dry_run=True)
            os.chdir(original_cwd)
        else:
            print(f"Cannot show dry run - directory {semester_dir} does not exist")
    else:
        print("Updating myst.yml...")
        update_myst_yml(course_name, semester, course_title, course_description, course_authors)
        
        print("Updating index.md...")
        update_index_md(course_title, semester_display, course_name)
    
    print("\n✅ Course instance setup complete!")
    print("\nNext steps:")
    print("1. Review and customize the generated myst.yml file")
    print("2. Update index.md with actual instructor/GSI information")
    print("3. Customize schedule.yml with your course schedule")
    print("4. Update syllabus.md, calendar.md, and other content files")
    print("5. Commit and push your changes:")
    print("   git add .")
    print(f"   git commit -m 'Initial course setup for {semester}'")
    print("   git push origin main")
    print(f"\nYour course site will be available at: https://{course_name}.berkeley.edu/{semester}")


if __name__ == "__main__":
    main()
