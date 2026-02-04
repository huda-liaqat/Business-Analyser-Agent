"""
Quick run script for the Business Analyst AI Agent
"""
import os
import sys
import subprocess


def check_venv():
    """Check if running in virtual environment."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import crewai
        import streamlit
        import yfinance
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        return False


def check_api_keys():
    """Check if API keys are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    google_key = os.getenv("GOOGLE_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    if not google_key:
        print("⚠️  GOOGLE_API_KEY is not set")
        print("   Get your free key at: https://aistudio.google.com/apikey")
        return False
    
    if not serper_key:
        print("⚠️  SERPER_API_KEY is not set")
        print("   Get your free key at: https://serper.dev/")
        return False
    
    return True


def main():
    """Main entry point."""
    print("🚀 AI Business Analyst Agent")
    print("=" * 40)
    
    # Check virtual environment
    if not check_venv():
        print("⚠️  Not running in virtual environment")
        print("   Recommended: python -m venv venv && venv\\Scripts\\activate")
    else:
        print("✅ Virtual environment active")
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Install dependencies with: pip install -r requirements.txt")
        return
    print("✅ Dependencies installed")
    
    # Check API keys
    if not check_api_keys():
        print("\n🔑 Create a .env file with your API keys")
        return
    print("✅ API keys configured")
    
    print("\n" + "=" * 40)
    print("🌐 Starting Streamlit server...")
    print("   Open: http://localhost:8501")
    print("=" * 40 + "\n")
    
    # Run Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])


if __name__ == "__main__":
    main()

