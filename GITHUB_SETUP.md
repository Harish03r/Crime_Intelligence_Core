# GitHub Repository Setup Guide

## Option 1: Create New Repository on GitHub

1. Go to GitHub.com and log in
2. Click "New Repository" (green button)
3. Name your repository: `crime-intelligence-core`
4. Add description: "AI-powered crime intelligence system with multi-agent architecture"
5. Keep it Public (or Private if you prefer)
6. Don't initialize with README (we already have one)
7. Click "Create Repository"

## Option 2: Connect to Existing Repository

If you already have a repository, get the URL from GitHub (should look like):
`https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git`

## Push to GitHub

Once you have the repository URL, run these commands:

```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git

# Verify remote was added
git remote -v

# Push to GitHub (first time)
git push -u origin master

# For future pushes, just use:
git push
```

## Example with Sample Username

If your GitHub username is `johndoe` and repository is `crime-intelligence-core`:

```bash
git remote add origin https://github.com/johndoe/crime-intelligence-core.git
git push -u origin master
```

## Authentication

If you haven't set up GitHub authentication:

### Using Personal Access Token (Recommended):
1. Go to GitHub Settings > Developer Settings > Personal Access Tokens
2. Generate new token with `repo` scope
3. Use token as password when prompted

### Using SSH (Alternative):
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to SSH agent: `ssh-add ~/.ssh/id_ed25519`
3. Add public key to GitHub Settings > SSH Keys
4. Use SSH URL: `git@github.com:USERNAME/REPOSITORY_NAME.git`

## Repository Features to Enable

After pushing, consider enabling:

1. **GitHub Pages** (for documentation)
2. **Issues** (for bug tracking)
3. **Wiki** (for detailed docs)
4. **Discussions** (for community)
5. **Actions** (for CI/CD)

## Next Steps After Push

1. Add repository topics/tags: `crime-intelligence`, `ai`, `crewai`, `streamlit`
2. Create release tags for versions
3. Set up branch protection rules
4. Add collaborators if needed
5. Configure webhooks if required