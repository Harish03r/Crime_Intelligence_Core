"""Entry point to run the Crime Intelligence Core application."""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import crewai
        import neo4j
        import google.generativeai
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are set up."""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found. Copy .env.example to .env and configure:")
        print("   - GOOGLE_API_KEY: Your Gemini API key")
        print("   - NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD: Neo4j connection details")
        return False
    
    print("✅ Environment file found")
    return True

def setup_database():
    """Set up the Neo4j database with dummy data."""
    print("🔄 Setting up database with dummy data...")
    try:
        from scripts.generate_dummy_data import main as generate_data
        generate_data()
        print("✅ Database setup completed")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("Make sure Neo4j is running and credentials are correct")
        return False

def main():
    """Main function to run the application."""
    print("🚔 Crime Intelligence Core - Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Ask user if they want to set up database
    setup_db = input("\n🗄️  Set up database with dummy data? (y/n): ").lower().strip()
    if setup_db in ['y', 'yes']:
        if not setup_database():
            print("⚠️  Database setup failed, but you can still run the app")
    
    # Run Streamlit app
    print("\n🚀 Starting Streamlit application...")
    print("📍 Application will open at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()