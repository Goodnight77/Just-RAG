#!/usr/bin/env python3
"""Setup script for the RAG Chatbot."""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a command and return True if successful."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        return False

def setup_environment():
    """Setup the development environment."""
    print("🚀 Setting up RAG Chatbot environment...")
    
    # Create data directory
    data_dir = Path("data")
    if not data_dir.exists():
        print("📁 Creating data directory...")
        data_dir.mkdir()
        print("✅ Data directory created")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        example_env = Path(".env.example")
        if example_env.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created from template")
        else:
            with open(".env", "w") as f:
                f.write("# Add your Gemini API key here\\n")
                f.write("GEMINI_API_KEY=your_api_key_here\\n")
            print("✅ .env file created")
    
    # Install requirements
    print("📦 Installing Python dependencies...")
    if run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("✅ Dependencies installed successfully")
    else:
        print("❌ Failed to install dependencies")
        return False
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Consider using a virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   python setup.py")
    
    return True

def main():
    """Main setup function."""
    print("RAG Chatbot Setup")
    print("=" * 50)
    
    if not setup_environment():
        print("\\n❌ Setup failed!")
        sys.exit(1)
    
    print("\\n🎉 Setup completed successfully!")
    print("\\nNext steps:")
    print("1. Add your Gemini API key to the .env file")
    print("2. Place your document in the data/ directory")
    print("3. Run: python main.py --document data/your_document.pdf")
    print("\\nFor help: python main.py --help")

if __name__ == "__main__":
    main()