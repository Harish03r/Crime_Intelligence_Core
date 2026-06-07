#!/usr/bin/env python3
"""Helper script to push Crime Intelligence Core to GitHub repository."""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Main function to push to GitHub."""
    print("🚔 Crime Intelligence Core - GitHub Push Setup")
    print("=" * 60)
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("❌ Git not initialized. Please run 'git init' first.")
        return
    
    # Get repository URL from user
    print("\n📝 Please provide your GitHub repository details:")
    username = input("GitHub Username: ").strip()
    repo_name = input("Repository Name (default: crime-intelligence-core): ").strip()
    
    if not repo_name:
        repo_name = "crime-intelligence-core"
    
    if not username:
        print("❌ GitHub username is required!")
        return
    
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"\n🔗 Repository URL: {repo_url}")
    
    confirm = input("\nIs this correct? (y/n): ").lower().strip()
    if confirm not in ['y', 'yes']:
        print("❌ Setup cancelled.")
        return
    
    print(f"\n🚀 Setting up repository connection...")
    
    # Check if remote already exists
    check_remote = subprocess.run("git remote", shell=True, capture_output=True, text=True)
    if "origin" in check_remote.stdout:
        print("⚠️  Remote 'origin' already exists.")
        overwrite = input("Remove existing remote and add new one? (y/n): ").lower().strip()
        if overwrite in ['y', 'yes']:
            run_command("git remote remove origin", "Removing existing remote")
        else:
            print("❌ Setup cancelled.")
            return
    
    # Add remote repository
    if not run_command(f"git remote add origin {repo_url}", "Adding remote repository"):
        return
    
    # Verify remote
    if not run_command("git remote -v", "Verifying remote repository"):
        return
    
    # Check current branch
    branch_result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
    current_branch = branch_result.stdout.strip()
    
    if not current_branch:
        current_branch = "master"  # Default for new repos
        print(f"📍 Using default branch: {current_branch}")
    else:
        print(f"📍 Current branch: {current_branch}")
    
    # Push to GitHub
    print(f"\n📤 Pushing to GitHub repository...")
    
    # First push with upstream
    push_command = f"git push -u origin {current_branch}"
    if not run_command(push_command, f"Pushing {current_branch} branch to GitHub"):
        print("\n❌ Push failed. This might be due to:")
        print("   1. Authentication issues (need Personal Access Token)")
        print("   2. Repository doesn't exist on GitHub")
        print("   3. Network connectivity issues")
        print("\n💡 Solutions:")
        print("   1. Create the repository on GitHub first")
        print("   2. Use Personal Access Token for authentication")
        print("   3. Check your internet connection")
        return
    
    print("\n🎉 SUCCESS! Repository pushed to GitHub!")
    print(f"📂 Repository URL: https://github.com/{username}/{repo_name}")
    print(f"🌐 Clone URL: {repo_url}")
    
    # Additional suggestions
    print("\n📋 Next Steps:")
    print("1. Visit your repository on GitHub")
    print("2. Add repository description and topics")
    print("3. Enable GitHub Pages if needed")
    print("4. Set up branch protection rules")
    print("5. Add collaborators if working in a team")
    
    print(f"\n✨ Your Crime Intelligence Core is now on GitHub!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")