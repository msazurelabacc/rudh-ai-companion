# setup_phase32.py
"""
Phase 3.2 Setup Script - Portfolio Management & Risk Analytics
Complete setup for advanced portfolio management system
"""

import subprocess
import sys
import os
import logging
from datetime import datetime

def install_packages():
    """Install required Python packages"""
    packages = [
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "yfinance>=0.2.0",
        "sqlite3",  # Built-in, but checking
        "aiohttp>=3.8.0",
        "requests>=2.31.0"
    ]
    
    print("📦 Installing portfolio management dependencies...")
    
    for package in packages:
        try:
            if package == "sqlite3":
                # sqlite3 is built-in, just check if it's available
                import sqlite3
                print(f"✅ {package} (built-in)")
                continue
            
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
        except ImportError:
            print(f"❌ sqlite3 not available")
            return False
    
    return True

def test_dependencies():
    """Test all dependencies are working"""
    print("\n🧪 Testing dependencies...")
    
    try:
        import numpy as np
        print("✅ NumPy:", np.__version__)
        
        import pandas as pd
        print("✅ Pandas:", pd.__version__)
        
        import scipy
        print("✅ SciPy:", scipy.__version__)
        
        import yfinance as yf
        print("✅ yFinance: Available")
        
        import sqlite3
        print("✅ SQLite3: Available")
        
        import aiohttp
        print("✅ aiohttp:", aiohttp.__version__)
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependency test failed: {e}")
        return False

def create_sample_portfolio():
    """Create a sample portfolio for testing"""
    print("\n📊 Creating sample portfolio for testing...")
    
    try:
        from portfolio_database import PortfolioDatabase
        
        # Initialize database
        db = PortfolioDatabase()
        
        # Check if sample portfolio already exists
        portfolios = db.get_all_portfolios()
        sample_exists = any(p['name'] == 'Rudh Sample Portfolio' for p in portfolios)
        
        if sample_exists:
            print("✅ Sample portfolio already exists")
            return True
        
        # Create sample portfolio
        portfolio_id = db.create_portfolio(
            name="Rudh Sample Portfolio",
            initial_cash=1000000.0,  # ₹10 lakhs
            risk_profile="Moderate",
            investment_goals=["Long-term Growth", "Diversification", "Dividend Income"]
        )
        
        print(f"✅ Sample portfolio created: {portfolio_id}")
        
        # Add sample holdings (Indian blue-chip stocks)
        sample_holdings = [
            ("RELIANCE.NS", 50, 2850.0),    # Reliance Industries
            ("TCS.NS", 30, 4100.0),         # Tata Consultancy Services
            ("HDFCBANK.NS", 40, 1650.0),    # HDFC Bank
            ("INFY.NS", 25, 1750.0),        # Infosys
            ("ICICIBANK.NS", 60, 950.0),    # ICICI Bank
            ("ITC.NS", 100, 450.0),         # ITC Limited
            ("KOTAKBANK.NS", 35, 1800.0),   # Kotak Mahindra Bank
            ("LT.NS", 20, 3200.0),          # Larsen & Toubro
        ]
        
        print("📈 Adding sample holdings...")
        
        for symbol, quantity, price in sample_holdings:
            try:
                holding_id = db.add_holding(portfolio_id, symbol, quantity, price)
                print(f"   ✅ {symbol}: {quantity} shares @ ₹{price}")
            except Exception as e:
                print(f"   ⚠️ Failed to add {symbol}: {e}")
        
        # Update current prices
        print("🔄 Updating current market prices...")
        updated_prices = db.update_prices(portfolio_id)
        
        if updated_prices:
            print(f"✅ Updated prices for {len(updated_prices)} stocks")
        
        # Get portfolio summary
        summary = db.get_portfolio_summary(portfolio_id)
        if 'error' not in summary:
            print(f"✅ Sample portfolio value: ₹{summary['total_value']:,.2f}")
            print(f"   Return: ₹{summary['total_return']:,.2f} ({summary['total_return_percent']:+.2f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample portfolio creation failed: {e}")
        return False

def test_risk_analytics():
    """Test risk analytics functionality"""
    print("\n⚠️ Testing risk analytics...")
    
    try:
        from risk_analytics import RiskAnalyticsEngine
        from portfolio_database import PortfolioDatabase
        
        # Get sample portfolio
        db = PortfolioDatabase()
        portfolios = db.get_all_portfolios()
        
        if not portfolios:
            print("❌ No portfolios found for testing")
            return False
        
        portfolio_id = portfolios[0]['portfolio_id']
        
        # Initialize risk engine
        risk_engine = RiskAnalyticsEngine()
        
        # Test risk calculation
        print("   🎯 Testing risk metrics calculation...")
        risk_metrics = risk_engine.calculate_portfolio_risk(portfolio_id)
        
        print(f"   ✅ Risk Score: {risk_metrics.risk_score}/100")
        print(f"   ✅ Sharpe Ratio: {risk_metrics.sharpe_ratio:.2f}")
        print(f"   ✅ Portfolio Beta: {risk_metrics.portfolio_beta:.2f}")
        
        # Test optimization
        print("   🎯 Testing portfolio optimization...")
        optimization = risk_engine.optimize_portfolio(portfolio_id)
        
        print(f"   ✅ Expected Return: {optimization.expected_return:.1%}")
        print(f"   ✅ Expected Volatility: {optimization.expected_volatility:.1%}")
        print(f"   ✅ Rebalancing Actions: {len(optimization.rebalancing_actions)}")
        
        # Test stress testing
        print("   🎯 Testing stress scenarios...")
        stress_results = risk_engine.stress_test_portfolio(portfolio_id)
        
        if stress_results:
            max_loss = max(stress_results.values())
            print(f"   ✅ Stress Testing: Max loss ₹{max_loss:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Risk analytics test failed: {e}")
        return False

def create_project_structure():
    """Create necessary project directories"""
    print("\n📁 Creating project structure...")
    
    directories = [
        "data",
        "reports",
        "backups"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create {directory}: {e}")

def main():
    """Main setup function"""
    print("🚀 RUDH PORTFOLIO MANAGER V3.2 SETUP")
    print("================================================================================")
    print("Setting up advanced portfolio management with risk analytics...")
    print("This will install dependencies and create sample data for testing.")
    print()
    
    # Step 1: Install packages
    if not install_packages():
        print("❌ Package installation failed. Please check your internet connection.")
        return False
    
    # Step 2: Test dependencies
    if not test_dependencies():
        print("❌ Dependency testing failed. Please check package installations.")
        return False
    
    # Step 3: Create project structure
    create_project_structure()
    
    # Step 4: Test database functionality
    print("\n🗄️ Testing database functionality...")
    try:
        from portfolio_database import PortfolioDatabase
        db = PortfolioDatabase()
        print("✅ Portfolio database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    # Step 5: Create sample portfolio
    if not create_sample_portfolio():
        print("❌ Sample portfolio creation failed")
        return False
    
    # Step 6: Test risk analytics
    if not test_risk_analytics():
        print("❌ Risk analytics testing failed")
        return False
    
    # Success message
    print("\n🎉 PHASE 3.2 SETUP COMPLETE!")
    print("================================================================================")
    print("✅ Portfolio database operational")
    print("✅ Risk analytics engine ready")
    print("✅ Sample portfolio created with 8 Indian blue-chip stocks")
    print("✅ All dependencies installed and tested")
    print()
    print("🚀 READY TO LAUNCH:")
    print("   python rudh_portfolio_manager_v32.py")
    print()
    print("💡 FEATURES AVAILABLE:")
    print("   • Portfolio tracking with real-time prices")
    print("   • Advanced risk analytics (VaR, Beta, Sharpe)")
    print("   • Portfolio optimization using Modern Portfolio Theory")
    print("   • Stress testing and correlation analysis")
    print("   • Voice-enabled portfolio commands")
    print("   • AI-powered investment advice")
    print()
    print("🌟 You now have one of the most advanced personal portfolio")
    print("   management systems available! Ready for real investment decisions.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n📅 Setup completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n❌ Setup failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)