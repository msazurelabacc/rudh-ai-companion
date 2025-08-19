# setup_financial_intelligence.py
"""
Setup script for Rudh Financial Intelligence Module - Phase 3
Installs dependencies and configures financial services
"""

import subprocess
import sys
import os
from pathlib import Path

def install_financial_dependencies():
    """Install required packages for financial intelligence"""
    print("📦 Installing Financial Intelligence Dependencies...")
    print("=" * 60)
    
    # Required packages for financial intelligence
    packages = [
        "yfinance>=0.2.18",      # Yahoo Finance API
        "pandas>=1.5.0",         # Data manipulation
        "numpy>=1.24.0",         # Numerical computations
        "requests>=2.28.0",      # HTTP requests for APIs
        "python-dotenv>=0.19.0", # Environment variables
        "aiohttp>=3.8.0",        # Async HTTP client
        "beautifulsoup4>=4.11.0", # Web scraping for news
        "lxml>=4.9.0",           # XML/HTML parser
        "matplotlib>=3.6.0",     # Plotting (optional)
        "seaborn>=0.11.0",       # Statistical plotting (optional)
    ]
    
    print("📋 Packages to install:")
    for package in packages:
        print(f"   • {package}")
    
    print(f"\n🔧 Installing packages...")
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            return False
    
    print(f"\n✅ All financial dependencies installed successfully!")
    return True

def create_financial_config():
    """Create financial intelligence configuration"""
    print(f"\n⚙️ Setting up Financial Intelligence Configuration...")
    print("=" * 60)
    
    # Check if .env file exists and add financial settings
    env_file = Path(".env")
    
    financial_config = """
# Financial Intelligence Configuration
FINANCIAL_ENGINE_ENABLED=true
DEFAULT_CURRENCY=INR
DEFAULT_MARKET=indian
RISK_FREE_RATE=0.07

# Market Data Sources
YAHOO_FINANCE_ENABLED=true
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here

# Financial Analysis Settings
MAX_PORTFOLIO_STOCKS=50
DEFAULT_ANALYSIS_PERIOD=1y
TECHNICAL_ANALYSIS_ENABLED=true
FUNDAMENTAL_ANALYSIS_ENABLED=true

# Risk Management
MAX_SINGLE_STOCK_ALLOCATION=25.0
DEFAULT_STOP_LOSS_PERCENT=8.0
DEFAULT_TARGET_GAIN_PERCENT=20.0

# Indian Market Settings
NSE_MARKET_HOURS_START=09:15
NSE_MARKET_HOURS_END=15:30
BSE_MARKET_HOURS_START=09:15
BSE_MARKET_HOURS_END=15:30

# Logging
FINANCIAL_LOG_LEVEL=INFO
ENABLE_TRADE_LOGGING=true
"""
    
    try:
        with open(env_file, "a", encoding="utf-8") as f:
            f.write(financial_config)
        print("✅ Financial configuration added to .env file")
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        return False
    
    return True

def create_sample_portfolio():
    """Create sample portfolio file for testing"""
    print(f"\n📁 Creating Sample Portfolio for Testing...")
    print("=" * 60)
    
    sample_portfolio = {
        "portfolio_name": "Sample Chennai Tech Portfolio",
        "created_date": "2025-08-19",
        "currency": "INR",
        "risk_tolerance": "MEDIUM",
        "holdings": [
            {
                "symbol": "TCS",
                "name": "Tata Consultancy Services",
                "quantity": 10,
                "avg_purchase_price": 3800.00,
                "purchase_date": "2024-12-01",
                "sector": "IT Services"
            },
            {
                "symbol": "RELIANCE",
                "name": "Reliance Industries",
                "quantity": 5,
                "avg_purchase_price": 2500.00,
                "purchase_date": "2024-11-15",
                "sector": "Oil & Gas"
            },
            {
                "symbol": "INFY",
                "name": "Infosys Limited",
                "quantity": 15,
                "avg_purchase_price": 1600.00,
                "purchase_date": "2024-10-20",
                "sector": "IT Services"
            },
            {
                "symbol": "HDFCBANK",
                "name": "HDFC Bank",
                "quantity": 8,
                "avg_purchase_price": 1700.00,
                "purchase_date": "2024-09-10",
                "sector": "Banking"
            }
        ],
        "watchlist": [
            "ICICIBANK", "SBI", "ITC", "LT", "WIPRO", 
            "MARUTI", "BHARTIARTL", "ASIANPAINT"
        ]
    }
    
    try:
        import json
        with open("sample_portfolio.json", "w", encoding="utf-8") as f:
            json.dump(sample_portfolio, f, indent=2, ensure_ascii=False)
        print("✅ Sample portfolio created: sample_portfolio.json")
        print("💡 This portfolio is worth approximately ₹1,45,000 at purchase prices")
    except Exception as e:
        print(f"❌ Failed to create sample portfolio: {e}")
        return False
    
    return True

def create_requirements_financial():
    """Create requirements file for financial intelligence"""
    print(f"\n📝 Creating Financial Requirements File...")
    print("=" * 60)
    
    requirements = """# Financial Intelligence Requirements - Phase 3
# Core financial data and analysis packages

# Market Data APIs
yfinance>=0.2.18
requests>=2.28.0
aiohttp>=3.8.0

# Data Analysis and Manipulation
pandas>=1.5.0
numpy>=1.24.0

# Web Scraping for News/Sentiment
beautifulsoup4>=4.11.0
lxml>=4.9.0

# Visualization (Optional but Recommended)
matplotlib>=3.6.0
seaborn>=0.11.0
plotly>=5.11.0

# Configuration and Environment
python-dotenv>=0.19.0

# Enhanced HTTP and API handling
httpx>=0.24.0
urllib3>=1.26.12

# Date and Time handling
python-dateutil>=2.8.2

# Async support
asyncio>=3.4.3

# Optional: Advanced Financial Analysis
scipy>=1.9.0
scikit-learn>=1.1.0
statsmodels>=0.13.0

# Optional: Database support for portfolio storage
sqlite3>=2.6.0

# Already installed with existing Rudh:
# azure-cognitiveservices-speech
# azure-ai-language
# openai
# pygame
"""
    
    try:
        with open("requirements_financial.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        print("✅ Financial requirements file created: requirements_financial.txt")
    except Exception as e:
        print(f"❌ Failed to create requirements file: {e}")
        return False
    
    return True

def test_financial_setup():
    """Test financial intelligence setup"""
    print(f"\n🧪 Testing Financial Intelligence Setup...")
    print("=" * 60)
    
    print("📋 Testing package imports...")
    
    # Test core packages
    test_packages = [
        ("yfinance", "yf"),
        ("pandas", "pd"),
        ("numpy", "np"),
        ("requests", "requests"),
        ("aiohttp", "aiohttp"),
    ]
    
    all_passed = True
    
    for package_name, import_name in test_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name} - OK")
        except ImportError as e:
            print(f"   ❌ {package_name} - FAILED: {e}")
            all_passed = False
    
    # Test Yahoo Finance API
    print(f"\n📊 Testing Yahoo Finance API connection...")
    try:
        import yfinance as yf
        # Test with a simple Indian stock
        ticker = yf.Ticker("RELIANCE.NS")
        info = ticker.info
        if info and 'longName' in info:
            print(f"   ✅ API Connection - OK (Retrieved: {info['longName']})")
        else:
            print(f"   ⚠️ API Connection - Limited (No company name retrieved)")
    except Exception as e:
        print(f"   ❌ API Connection - FAILED: {e}")
        all_passed = False
    
    # Test financial engine import
    print(f"\n🧠 Testing Financial Engine...")
    try:
        # This will test our financial_intelligence_engine.py
        print(f"   📁 Checking financial_intelligence_engine.py exists...")
        if os.path.exists("financial_intelligence_engine.py"):
            print(f"   ✅ Financial Engine File - Found")
        else:
            print(f"   ❌ Financial Engine File - Missing")
            all_passed = False
    except Exception as e:
        print(f"   ❌ Financial Engine Test - FAILED: {e}")
        all_passed = False
    
    print(f"\n{'✅ SETUP SUCCESSFUL!' if all_passed else '❌ SETUP INCOMPLETE'}")
    
    if all_passed:
        print(f"""
🎉 FINANCIAL INTELLIGENCE IS READY!

🚀 Quick Start Commands:
   python financial_intelligence_engine.py  # Test the engine
   python rudh_financial_advisor.py         # Start the advisor

💡 Sample Queries to Try:
   • "analyze RELIANCE"
   • "market overview" 
   • "portfolio review"
   • "recommend stocks"

📊 Your Chennai-focused AI financial advisor is ready!
        """)
    else:
        print(f"""
🔧 SETUP NEEDS ATTENTION:
   • Check failed package installations
   • Ensure internet connection for API tests
   • Verify all required files are present
        """)
    
    return all_passed

def main():
    """Main setup function"""
    print("🚀 RUDH FINANCIAL INTELLIGENCE SETUP - PHASE 3")
    print("=" * 80)
    print("Setting up your Chennai-focused AI Financial Advisor...")
    print("This will install market data APIs, analysis tools, and portfolio management")
    print("=" * 80)
    
    # Step 1: Install dependencies
    if not install_financial_dependencies():
        print("❌ Dependency installation failed. Exiting.")
        return False
    
    # Step 2: Create configuration
    if not create_financial_config():
        print("❌ Configuration setup failed. Continuing...")
    
    # Step 3: Create sample portfolio
    if not create_sample_portfolio():
        print("❌ Sample portfolio creation failed. Continuing...")
    
    # Step 4: Create requirements file
    if not create_requirements_financial():
        print("❌ Requirements file creation failed. Continuing...")
    
    # Step 5: Test setup
    success = test_financial_setup()
    
    if success:
        print(f"\n🎉 CONGRATULATIONS!")
        print(f"Rudh Financial Intelligence is ready for Chennai markets!")
        print(f"\nNext step: python rudh_financial_advisor.py")
    else:
        print(f"\n🔧 Setup completed with some issues.")
        print(f"Check the error messages above and retry.")
    
    return success

if __name__ == "__main__":
    main()