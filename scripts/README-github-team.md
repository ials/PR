# GitHub Team Setup Script

This script automates the creation of GitHub teams and repository access for course instances. The script is **idempotent** - it can be run multiple times safely and will only make changes when needed.

## Prerequisites

1. GitHub CLI (`gh`) must be installed and authenticated
2. You must have admin permissions on the target organization
3. The repository must already exist

## Usage

### Basic Usage

```bash
# Create team and add to repository (safe to run multiple times)
python setup-github-team.py stat158 spring-2025

# With specific users
python setup-github-team.py stat158 spring-2025 --users andrewpbray,instructor2,ta1

# Dry run to see what would happen
python setup-github-team.py stat158 spring-2025 --users andrewpbray --dry-run

# Force update permissions/roles even if already set
python setup-github-team.py stat158 spring-2025 --users andrewpbray --force
```

### Options

- `--users`: Comma-separated list of GitHub usernames to add to the team
- `--role`: Role for users (`member` or `maintainer`, default: `member`)
- `--permission`: Repository permission level (`pull`, `triage`, `push`, `maintain`, `admin`, default: `maintain`)
- `--dry-run`: Show what would be done without executing commands
- `--force`: Force operations even if resources already exist (useful for updating permissions/roles)

## Idempotent Behavior

The script checks for existing resources before attempting to create them:

- ✅ **Organization exists**: Validates organization access before proceeding
- ✅ **Repository exists**: Confirms repository exists and is accessible
- ✅ **Team exists**: Skips team creation if team already exists
- ✅ **Team has repo access**: Skips adding team to repo if already has access
- ✅ **User in team**: Skips adding user if already a team member

### Force Mode

Use `--force` to update existing configurations:
- Update team repository permissions
- Update user roles in teams
- Useful for changing permission levels or roles after initial setup

## What the script does

1. **Validates prerequisites** - Checks that organization and repository exist
2. **Creates a team** in the organization `berkeley-{course}` with name `instructors-{semester}` (if not exists)
3. **Adds team to repository** `berkeley-{course}/{semester}` with maintain permissions (if not already added)
4. **Adds users to team** (if specified) with member role (if not already members)

## Examples

For course `stat158` and semester `spring-2025`:
- Organization: `berkeley-stat158`
- Team: `instructors-spring-2025`
- Repository: `berkeley-stat158/spring-2025`

### Example Output

```bash
$ python setup-github-team.py stat158 spring-2025 --users andrewpbray

Course setup for: stat158 spring-2025
Organization: berkeley-stat158
Team: instructors-spring-2025
Repository: berkeley-stat158/spring-2025

✓ Organization 'berkeley-stat158' is accessible
✓ Repository 'berkeley-stat158/spring-2025' is accessible

✓ Team 'instructors-spring-2025' already exists in organization 'berkeley-stat158'
✓ Team 'instructors-spring-2025' already has access to repository 'berkeley-stat158/spring-2025'
Adding user 'andrewpbray' to team 'instructors-spring-2025' as 'member'...
✓ User 'andrewpbray' added to team as member

✓ GitHub team setup completed successfully!
```

### Example Commands Generated

```bash
# Create team
gh api --method POST /orgs/berkeley-stat158/teams \
  -f name="instructors-spring-2025" -f privacy="closed"

# Add team to repo
gh api --method PUT \
  -H "Accept: application/vnd.github.v3+json" \
  /orgs/berkeley-stat158/teams/instructors-spring-2025/repos/berkeley-stat158/spring-2025 \
  -f permission="maintain"

# Add user to team
gh api --method PUT -H "Accept: application/vnd.github.v3+json" \
  /orgs/berkeley-stat158/teams/instructors-spring-2025/memberships/andrewpbray \
  -f role="member"
```

## Error Handling

The script will stop on the first error and display the GitHub API error message. Common issues:

- Team already exists
- User doesn't have permission on the organization
- Repository doesn't exist
- User being added doesn't exist or isn't a member of the organization

## Dependencies

- Python 3.6+
- GitHub CLI (`gh`) installed and authenticated
- `subprocess` and `json` modules (included with Python)
