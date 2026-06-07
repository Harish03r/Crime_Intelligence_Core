"""Setup script for Crime Intelligence Core."""

import os
import sys
from pathlib import Path
import subprocess
import shutil

def print_banner():
    """Print setup banner."""
    print("="*60)
    print("🚔 CRIME INTELLIGENCE CORE - SETUP")
    print("="*60)
    print("AI-Powered Crime Intelligence with Multi-Agent Architecture")
    print("")

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['data', 'logs', 'config', 'agents', 'scripts']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def setup_environment():
    """Set up environment variables."""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your:")
        print("   - Google Gemini API key")
        print("   - Neo4j database credentials")
        return True
    else:
        print("❌ .env.example not found")
        return False

def check_neo4j():
    """Check if Neo4j is available."""
    print("🔍 Checking Neo4j availability...")
    
    # Check if Docker is available
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
        print("✅ Docker is available")
        
        # Ask user if they want to start Neo4j with Docker
        response = input("🐳 Start Neo4j with Docker Compose? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            try:
                subprocess.run(['docker-compose', 'up', '-d', 'neo4j'], check=True)
                print("✅ Neo4j started with Docker")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to start Neo4j with Docker")
                return False
        
    except subprocess.CalledProcessError:
        print("⚠️  Docker not available")
        print("   You can:")
        print("   1. Install Docker and use docker-compose.yml")
        print("   2. Install Neo4j manually")
        print("   3. Use Neo4j Aura (cloud)")
        
    return False

def validate_setup():
    """Validate the setup."""
    print("🔍 Validating setup...")
    
    # Check if all required files exist
    required_files = [
        'app.py', 'requirements.txt', '.env',
        'agents/base_agent.py', 'agents/investigator_agent.py',
        'config/database.py', 'scripts/generate_dummy_data.py'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    return True

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Set up environment
    if not setup_environment():
        print("⚠️  Environment setup incomplete")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Check Neo4j
    check_neo4j()
    
    # Validate setup
    if validate_setup():
        print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys and database credentials")
        print("2. Ensure Neo4j is running")
        print("3. Run: python run_app.py")
        print("\nOr use Docker:")
        print("docker-compose up --build")
    else:
        print("❌ Setup validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()