#!/usr/bin/env python3
"""
Script to automate GitHub team creation and repository management for course instances.

This script:
1. Creates a team within an organization
2. Adds the team to the repository with maintain permissions
3. Optionally adds users to the team

Usage:
    python setup-github-team.py stat123 fall-2025
    python setup-github-team.py stat123 fall-2025 --users user1,user2,user3
"""

import argparse
import subprocess
import sys
import json
from typing import List, Optional


def run_gh_command(command: List[str], ignore_errors: bool = False) -> dict:
    """
    Run a GitHub CLI command and return the JSON response.
    
    Args:
        command: List of command arguments for gh
        ignore_errors: If True, return empty dict on errors instead of raising
        
    Returns:
        dict: Parsed JSON response from the command
        
    Raises:
        subprocess.CalledProcessError: If the command fails and ignore_errors is False
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Try to parse JSON response if there is output
        if result.stdout.strip():
            return json.loads(result.stdout)
        return {}
        
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            return {}
        print(f"Error running command: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        raise
    except json.JSONDecodeError as e:
        if ignore_errors:
            return {}
        print(f"Error parsing JSON response: {e}")
        print(f"Raw output: {result.stdout}")
        raise


def check_org_exists(org: str) -> bool:
    """
    Check if a GitHub organization exists and is accessible.
    
    Args:
        org: GitHub organization name
        
    Returns:
        bool: True if organization exists and is accessible
    """
    command = ["gh", "api", f"/orgs/{org}"]
    result = run_gh_command(command, ignore_errors=True)
    return bool(result)


def check_repo_exists(repo: str) -> bool:
    """
    Check if a GitHub repository exists and is accessible.
    
    Args:
        repo: Repository name in format "owner/repo"
        
    Returns:
        bool: True if repository exists and is accessible
    """
    command = ["gh", "api", f"/repos/{repo}"]
    result = run_gh_command(command, ignore_errors=True)
    return bool(result)


def check_team_exists(org: str, team_name: str) -> bool:
    """
    Check if a team exists in the organization.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        
    Returns:
        bool: True if team exists
    """
    command = ["gh", "api", f"/orgs/{org}/teams/{team_name}"]
    result = run_gh_command(command, ignore_errors=True)
    return bool(result)


def check_team_has_repo_access(org: str, team_name: str, repo: str) -> bool:
    """
    Check if a team has access to a repository.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        repo: Repository name in format "owner/repo"
        
    Returns:
        bool: True if team has access to the repository
    """
    command = ["gh", "api", f"/orgs/{org}/teams/{team_name}/repos/{repo}"]
    result = run_gh_command(command, ignore_errors=True)
    return bool(result)


def check_user_in_team(org: str, team_name: str, username: str) -> bool:
    """
    Check if a user is a member of a team.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        username: GitHub username
        
    Returns:
        bool: True if user is a member of the team
    """
    command = ["gh", "api", f"/orgs/{org}/teams/{team_name}/memberships/{username}"]
    result = run_gh_command(command, ignore_errors=True)
    return bool(result)


def create_team(org: str, team_name: str) -> dict:
    """
    Create a team in the specified organization.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team to create
        
    Returns:
        dict: Team creation response
    """
    print(f"Creating team '{team_name}' in organization '{org}'...")
    
    command = [
        "gh", "api", "--method", "POST", f"/orgs/{org}/teams",
        "-f", f"name={team_name}",
        "-f", "privacy=closed"
    ]
    
    return run_gh_command(command)


def create_team_if_not_exists(org: str, team_name: str, force: bool = False) -> bool:
    """
    Create a team if it doesn't already exist.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team to create
        force: If True, attempt creation even if team exists (for error handling)
        
    Returns:
        bool: True if team was created, False if it already existed
    """
    if not force and check_team_exists(org, team_name):
        print(f"✓ Team '{team_name}' already exists in organization '{org}'")
        return False
    else:
        if force and check_team_exists(org, team_name):
            print(f"✓ Team '{team_name}' already exists (--force specified)")
            return False
        create_team(org, team_name)
        print(f"✓ Team '{team_name}' created successfully")
        return True


def add_team_to_repo_if_not_exists(org: str, team_name: str, repo: str, permission: str = "maintain", force: bool = False) -> bool:
    """
    Add a team to a repository if it doesn't already have access.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        repo: Repository name (org/repo format)
        permission: Permission level (maintain, admin, push, pull, triage)
        force: If True, update permissions even if team already has access
        
    Returns:
        bool: True if team was added/updated, False if it already had access
    """
    if not force and check_team_has_repo_access(org, team_name, repo):
        print(f"✓ Team '{team_name}' already has access to repository '{repo}'")
        return False
    else:
        add_team_to_repo(org, team_name, repo, permission)
        if force and check_team_has_repo_access(org, team_name, repo):
            print(f"✓ Team '{team_name}' permissions updated for repository '{repo}' ({permission})")
        else:
            print(f"✓ Team '{team_name}' added to repository with {permission} permissions")
        return True


def add_user_to_team_if_not_exists(org: str, team_name: str, username: str, role: str = "member", force: bool = False) -> bool:
    """
    Add a user to a team if they are not already a member.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        username: GitHub username to add
        role: Role for the user (member or maintainer)
        force: If True, update role even if user is already a member
        
    Returns:
        bool: True if user was added/updated, False if they were already a member
    """
    if not force and check_user_in_team(org, team_name, username):
        print(f"✓ User '{username}' is already a member of team '{team_name}'")
        return False
    else:
        add_user_to_team(org, team_name, username, role)
        if force and check_user_in_team(org, team_name, username):
            print(f"✓ User '{username}' role updated in team '{team_name}' ({role})")
        else:
            print(f"✓ User '{username}' added to team as {role}")
        return True


def add_team_to_repo(org: str, team_name: str, repo: str, permission: str = "maintain") -> dict:
    """
    Add a team to a repository with specified permissions.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        repo: Repository name (org/repo format)
        permission: Permission level (maintain, admin, push, pull, triage)
        
    Returns:
        dict: Response from adding team to repo
    """
    print(f"Adding team '{team_name}' to repository '{repo}' with '{permission}' permissions...")
    
    command = [
        "gh", "api", "--method", "PUT",
        "-H", "Accept: application/vnd.github.v3+json",
        f"/orgs/{org}/teams/{team_name}/repos/{repo}",
        "-f", f"permission={permission}"
    ]
    
    return run_gh_command(command)


def add_user_to_team(org: str, team_name: str, username: str, role: str = "member") -> dict:
    """
    Add a user to a team.
    
    Args:
        org: GitHub organization name
        team_name: Name of the team
        username: GitHub username to add
        role: Role for the user (member or maintainer)
        
    Returns:
        dict: Response from adding user to team
    """
    print(f"Adding user '{username}' to team '{team_name}' as '{role}'...")
    
    command = [
        "gh", "api", "--method", "PUT",
        "-H", "Accept: application/vnd.github.v3+json",
        f"/orgs/{org}/teams/{team_name}/memberships/{username}",
        "-f", f"role={role}"
    ]
    
    return run_gh_command(command)


def parse_course_info(course: str, semester: str) -> tuple:
    """
    Parse course and semester information to extract org, team, and repo names.
    
    Args:
        course: Course name (e.g., "stat123")
        semester: Semester (e.g., "fall-2025")
        
    Returns:
        tuple: (org_name, team_name, repo_name)
    """
    # Extract course number from course name
    # Assuming format like "stat123" -> "stat158" becomes "berkeley-stat158"
    org_name = f"berkeley-{course}"
    team_name = f"instructors-{semester}"
    repo_name = f"{org_name}/{semester}"
    
    return org_name, team_name, repo_name


def main():
    parser = argparse.ArgumentParser(
        description="Setup GitHub team and repository access for a course instance"
    )
    parser.add_argument(
        "course",
        help="Course name (e.g., stat123)"
    )
    parser.add_argument(
        "semester", 
        help="Semester (e.g., fall-2025)"
    )
    parser.add_argument(
        "--users",
        help="Comma-separated list of GitHub usernames to add to the team",
        default=""
    )
    parser.add_argument(
        "--role",
        help="Role for users added to the team (member or maintainer)",
        choices=["member", "maintainer"],
        default="member"
    )
    parser.add_argument(
        "--permission",
        help="Permission level for team on repository",
        choices=["pull", "triage", "push", "maintain", "admin"],
        default="maintain"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually executing commands"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force operations even if resources already exist (useful for updating permissions)"
    )
    
    args = parser.parse_args()
    
    # Parse course information
    org_name, team_name, repo_name = parse_course_info(args.course, args.semester)
    
    print(f"Course setup for: {args.course} {args.semester}")
    print(f"Organization: {org_name}")
    print(f"Team: {team_name}")
    print(f"Repository: {repo_name}")
    print()
    
    if args.dry_run:
        print("DRY RUN - No actual changes will be made")
        print()
    
    try:
        # Validation: Check if organization exists
        if not check_org_exists(org_name):
            print(f"❌ Error: Organization '{org_name}' does not exist or is not accessible")
            print("Make sure you have the correct organization name and appropriate permissions")
            sys.exit(1)
        
        # Validation: Check if repository exists
        if not check_repo_exists(repo_name):
            print(f"❌ Error: Repository '{repo_name}' does not exist or is not accessible")
            print("Make sure the repository exists and you have appropriate permissions")
            sys.exit(1)
        
        print(f"✓ Organization '{org_name}' is accessible")
        print(f"✓ Repository '{repo_name}' is accessible")
        print()
        
        # Step 1: Create the team (idempotent)
        if not args.dry_run:
            create_team_if_not_exists(org_name, team_name, args.force)
        else:
            if check_team_exists(org_name, team_name):
                print(f"Would skip creating team '{team_name}' (already exists)")
            else:
                print(f"Would create team: {team_name}")
        
        # Step 2: Add team to repository (idempotent)
        if not args.dry_run:
            add_team_to_repo_if_not_exists(org_name, team_name, repo_name, args.permission, args.force)
        else:
            if check_team_has_repo_access(org_name, team_name, repo_name):
                action = "update permissions for" if args.force else "skip adding team to"
                print(f"Would {action} repo '{repo_name}' ({'already has access' if not args.force else 'force update'})")
            else:
                print(f"Would add team to repo: {repo_name} with {args.permission} permissions")
        
        # Step 3: Add users to team (idempotent)
        if args.users:
            users = [user.strip() for user in args.users.split(",") if user.strip()]
            for user in users:
                if not args.dry_run:
                    add_user_to_team_if_not_exists(org_name, team_name, user, args.role, args.force)
                else:
                    if check_user_in_team(org_name, team_name, user):
                        action = "update role for" if args.force else "skip adding"
                        print(f"Would {action} user '{user}' ({'already a member' if not args.force else 'force update'})")
                    else:
                        print(f"Would add user: {user} as {args.role}")
        
        print()
        print("✓ GitHub team setup completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
