# portfolio_database.py - FIXED VERSION
"""
Rudh Portfolio Database & Tracking System - Phase 3.2 FIXED
Advanced portfolio management with SQLite database for holdings tracking
"""

import sqlite3
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import yfinance as yf
import time
import uuid

@dataclass
class Portfolio:
    """Portfolio data structure"""
    portfolio_id: str
    name: str
    created_date: str
    total_investment: float
    current_value: float
    cash_balance: float
    risk_profile: str  # Conservative, Moderate, Aggressive
    investment_goals: List[str]
    target_allocation: Dict[str, float]  # Sector allocations

@dataclass
class Holding:
    """Individual stock holding data structure"""
    holding_id: str
    portfolio_id: str
    symbol: str
    company_name: str
    quantity: int
    avg_cost: float
    current_price: float
    sector: str
    purchase_date: str
    last_updated: str
    dividend_yield: float = 0.0
    
    @property
    def total_cost(self) -> float:
        return self.quantity * self.avg_cost
    
    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price
    
    @property
    def profit_loss(self) -> float:
        return self.current_value - self.total_cost
    
    @property
    def profit_loss_percent(self) -> float:
        if self.total_cost == 0:
            return 0.0
        return (self.profit_loss / self.total_cost) * 100

@dataclass
class Transaction:
    """Transaction record"""
    transaction_id: str
    portfolio_id: str
    symbol: str
    transaction_type: str  # BUY, SELL, DIVIDEND
    quantity: int
    price: float
    transaction_date: str
    fees: float = 0.0
    notes: str = ""

class PortfolioDatabase:
    """Portfolio database management system"""
    
    def __init__(self, db_path: str = "rudh_portfolio.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("PortfolioDatabase")
        self.init_database()
    
    def _generate_unique_id(self, prefix: str) -> str:
        """Generate unique ID with timestamp and UUID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_suffix = str(uuid.uuid4())[:8]
        return f"{prefix}_{timestamp}_{unique_suffix}"
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Portfolios table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS portfolios (
                    portfolio_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    total_investment REAL NOT NULL,
                    current_value REAL NOT NULL,
                    cash_balance REAL NOT NULL,
                    risk_profile TEXT NOT NULL,
                    investment_goals TEXT NOT NULL,
                    target_allocation TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
                """)
                
                # Holdings table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS holdings (
                    holding_id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    avg_cost REAL NOT NULL,
                    current_price REAL NOT NULL,
                    sector TEXT NOT NULL,
                    purchase_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    dividend_yield REAL DEFAULT 0.0,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id)
                )
                """)
                
                # Transactions table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    transaction_date TEXT NOT NULL,
                    fees REAL DEFAULT 0.0,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id)
                )
                """)
                
                # Performance tracking table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    snapshot_date TEXT NOT NULL,
                    total_value REAL NOT NULL,
                    total_investment REAL NOT NULL,
                    cash_balance REAL NOT NULL,
                    sector_allocation TEXT NOT NULL,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id)
                )
                """)
                
                conn.commit()
                self.logger.info("✅ Portfolio database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    def create_portfolio(self, name: str, initial_cash: float = 100000.0, 
                        risk_profile: str = "Moderate", 
                        investment_goals: List[str] = None) -> str:
        """Create a new portfolio"""
        try:
            portfolio_id = self._generate_unique_id("portfolio")
            
            if investment_goals is None:
                investment_goals = ["Long-term Growth", "Diversification"]
            
            # Default target allocation for Indian markets
            target_allocation = {
                "IT": 25.0,
                "Banking": 20.0,
                "Auto": 15.0,
                "Pharma": 10.0,
                "Energy": 10.0,
                "FMCG": 10.0,
                "Others": 10.0
            }
            
            portfolio = Portfolio(
                portfolio_id=portfolio_id,
                name=name,
                created_date=datetime.now().isoformat(),
                total_investment=0.0,
                current_value=initial_cash,
                cash_balance=initial_cash,
                risk_profile=risk_profile,
                investment_goals=investment_goals,
                target_allocation=target_allocation
            )
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO portfolios VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    portfolio.portfolio_id,
                    portfolio.name,
                    portfolio.created_date,
                    portfolio.total_investment,
                    portfolio.current_value,
                    portfolio.cash_balance,
                    portfolio.risk_profile,
                    json.dumps(portfolio.investment_goals),
                    json.dumps(portfolio.target_allocation),
                    datetime.now().isoformat()
                ))
                conn.commit()
            
            self.logger.info(f"✅ Portfolio created: {name} (ID: {portfolio_id})")
            return portfolio_id
            
        except Exception as e:
            self.logger.error(f"❌ Portfolio creation failed: {e}")
            raise
    
    def add_holding(self, portfolio_id: str, symbol: str, quantity: int, 
                   purchase_price: float, purchase_date: str = None) -> str:
        """Add a stock holding to portfolio"""
        try:
            if purchase_date is None:
                purchase_date = datetime.now().isoformat()
            
            # Get stock info with error handling
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                company_name = info.get('longName', symbol)
                current_price = info.get('currentPrice', purchase_price)
                sector = info.get('sector', 'Unknown')
                dividend_yield = info.get('dividendYield', 0.0) or 0.0
            except Exception as e:
                self.logger.warning(f"Failed to get stock info for {symbol}: {e}")
                company_name = symbol
                current_price = purchase_price
                sector = 'Unknown'
                dividend_yield = 0.0
            
            holding_id = self._generate_unique_id(f"holding_{symbol}")
            
            holding = Holding(
                holding_id=holding_id,
                portfolio_id=portfolio_id,
                symbol=symbol,
                company_name=company_name,
                quantity=quantity,
                avg_cost=purchase_price,
                current_price=current_price,
                sector=sector,
                purchase_date=purchase_date,
                last_updated=datetime.now().isoformat(),
                dividend_yield=dividend_yield
            )
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO holdings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    holding.holding_id,
                    holding.portfolio_id,
                    holding.symbol,
                    holding.company_name,
                    holding.quantity,
                    holding.avg_cost,
                    holding.current_price,
                    holding.sector,
                    holding.purchase_date,
                    holding.last_updated,
                    holding.dividend_yield
                ))
                
                # Record transaction with unique ID
                transaction_id = self._generate_unique_id(f"txn_{symbol}")
                cursor.execute("""
                INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    transaction_id,
                    portfolio_id,
                    symbol,
                    "BUY",
                    quantity,
                    purchase_price,
                    purchase_date,
                    0.0,
                    f"Initial purchase of {quantity} shares"
                ))
                
                # Update portfolio cash balance
                total_cost = quantity * purchase_price
                cursor.execute("""
                UPDATE portfolios 
                SET cash_balance = cash_balance - ?,
                    total_investment = total_investment + ?,
                    last_updated = ?
                WHERE portfolio_id = ?
                """, (total_cost, total_cost, datetime.now().isoformat(), portfolio_id))
                
                conn.commit()
            
            self.logger.info(f"✅ Holding added: {symbol} x{quantity} @ ₹{purchase_price}")
            return holding_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add holding: {e}")
            raise
    
    def update_prices(self, portfolio_id: str) -> Dict[str, float]:
        """Update current prices for all holdings in portfolio"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query("""
                SELECT symbol, holding_id FROM holdings WHERE portfolio_id = ?
                """, conn, params=(portfolio_id,))
            
            updated_prices = {}
            
            for _, row in df.iterrows():
                try:
                    stock = yf.Ticker(row['symbol'])
                    info = stock.info
                    current_price = info.get('currentPrice', 0)
                    
                    if current_price > 0:
                        with sqlite3.connect(self.db_path) as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                            UPDATE holdings 
                            SET current_price = ?, last_updated = ?
                            WHERE holding_id = ?
                            """, (current_price, datetime.now().isoformat(), row['holding_id']))
                            conn.commit()
                        
                        updated_prices[row['symbol']] = current_price
                        
                except Exception as e:
                    self.logger.warning(f"Failed to update {row['symbol']}: {e}")
                    # Add a small delay to avoid rate limiting
                    time.sleep(0.1)
                    continue
            
            # Update portfolio current value
            self._update_portfolio_value(portfolio_id)
            
            self.logger.info(f"✅ Updated {len(updated_prices)} stock prices")
            return updated_prices
            
        except Exception as e:
            self.logger.error(f"❌ Price update failed: {e}")
            return {}
    
    def _update_portfolio_value(self, portfolio_id: str):
        """Update portfolio's current value"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate total holdings value
                cursor.execute("""
                SELECT SUM(quantity * current_price) as total_holdings
                FROM holdings WHERE portfolio_id = ?
                """, (portfolio_id,))
                
                result = cursor.fetchone()
                total_holdings = result[0] if result[0] else 0.0
                
                # Get cash balance
                cursor.execute("""
                SELECT cash_balance FROM portfolios WHERE portfolio_id = ?
                """, (portfolio_id,))
                
                cash_balance = cursor.fetchone()[0]
                total_value = total_holdings + cash_balance
                
                # Update portfolio
                cursor.execute("""
                UPDATE portfolios 
                SET current_value = ?, last_updated = ?
                WHERE portfolio_id = ?
                """, (total_value, datetime.now().isoformat(), portfolio_id))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"❌ Portfolio value update failed: {e}")
    
    def get_portfolio_summary(self, portfolio_id: str) -> Dict:
        """Get comprehensive portfolio summary"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Portfolio info
                portfolio_df = pd.read_sql_query("""
                SELECT * FROM portfolios WHERE portfolio_id = ?
                """, conn, params=(portfolio_id,))
                
                if portfolio_df.empty:
                    return {"error": "Portfolio not found"}
                
                portfolio_data = portfolio_df.iloc[0].to_dict()
                
                # Holdings info
                holdings_df = pd.read_sql_query("""
                SELECT * FROM holdings WHERE portfolio_id = ?
                """, conn, params=(portfolio_id,))
                
                holdings = []
                total_current_value = 0.0
                total_investment = 0.0
                sector_allocation = {}
                
                for _, holding in holdings_df.iterrows():
                    current_value = holding['quantity'] * holding['current_price']
                    investment = holding['quantity'] * holding['avg_cost']
                    profit_loss = current_value - investment
                    profit_loss_pct = (profit_loss / investment * 100) if investment > 0 else 0
                    
                    holdings.append({
                        'symbol': holding['symbol'],
                        'company_name': holding['company_name'],
                        'quantity': holding['quantity'],
                        'avg_cost': holding['avg_cost'],
                        'current_price': holding['current_price'],
                        'current_value': current_value,
                        'investment': investment,
                        'profit_loss': profit_loss,
                        'profit_loss_percent': profit_loss_pct,
                        'sector': holding['sector'],
                        'weight': 0.0  # Will calculate after total
                    })
                    
                    total_current_value += current_value
                    total_investment += investment
                    
                    # Sector allocation
                    sector = holding['sector']
                    if sector in sector_allocation:
                        sector_allocation[sector] += current_value
                    else:
                        sector_allocation[sector] = current_value
                
                # Calculate weights
                for holding in holdings:
                    if total_current_value > 0:
                        holding['weight'] = (holding['current_value'] / total_current_value) * 100
                
                # Sector percentages
                for sector in sector_allocation:
                    if total_current_value > 0:
                        sector_allocation[sector] = (sector_allocation[sector] / total_current_value) * 100
                
                # Portfolio performance
                total_portfolio_value = total_current_value + portfolio_data['cash_balance']
                total_return = total_current_value - total_investment
                total_return_pct = (total_return / total_investment * 100) if total_investment > 0 else 0
                
                return {
                    'portfolio_id': portfolio_id,
                    'name': portfolio_data['name'],
                    'created_date': portfolio_data['created_date'],
                    'risk_profile': portfolio_data['risk_profile'],
                    'total_value': total_portfolio_value,
                    'cash_balance': portfolio_data['cash_balance'],
                    'holdings_value': total_current_value,
                    'total_investment': total_investment,
                    'total_return': total_return,
                    'total_return_percent': total_return_pct,
                    'holdings_count': len(holdings),
                    'holdings': holdings,
                    'sector_allocation': sector_allocation,
                    'target_allocation': json.loads(portfolio_data['target_allocation']),
                    'investment_goals': json.loads(portfolio_data['investment_goals']),
                    'last_updated': portfolio_data['last_updated']
                }
                
        except Exception as e:
            self.logger.error(f"❌ Portfolio summary failed: {e}")
            return {"error": str(e)}
    
    def get_all_portfolios(self) -> List[Dict]:
        """Get all portfolios summary"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query("SELECT * FROM portfolios", conn)
                
                portfolios = []
                for _, row in df.iterrows():
                    portfolios.append({
                        'portfolio_id': row['portfolio_id'],
                        'name': row['name'],
                        'current_value': row['current_value'],
                        'total_investment': row['total_investment'],
                        'return_percent': ((row['current_value'] - row['total_investment']) / row['total_investment'] * 100) if row['total_investment'] > 0 else 0,
                        'risk_profile': row['risk_profile'],
                        'created_date': row['created_date']
                    })
                
                return portfolios
                
        except Exception as e:
            self.logger.error(f"❌ Get portfolios failed: {e}")
            return []

# Test the portfolio database
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testing Portfolio Database System...")
    
    # Initialize database
    db = PortfolioDatabase()
    
    # Create sample portfolio
    print("\n📝 Creating sample portfolio...")
    portfolio_id = db.create_portfolio(
        name="Rudh Test Portfolio",
        initial_cash=500000.0,
        risk_profile="Moderate",
        investment_goals=["Long-term Growth", "Dividend Income"]
    )
    
    # Add sample holdings with delays to avoid duplicate transaction IDs
    print("\n📈 Adding sample holdings...")
    holdings = [
        ("RELIANCE.NS", 50, 2850.0),
        ("TCS.NS", 30, 4100.0),
        ("HDFCBANK.NS", 40, 1650.0),
        ("INFY.NS", 25, 1750.0)
    ]
    
    for i, (symbol, quantity, price) in enumerate(holdings):
        try:
            # Add small delay to ensure unique timestamps
            if i > 0:
                time.sleep(1)
            holding_id = db.add_holding(portfolio_id, symbol, quantity, price)
            print(f"✅ Added {symbol}: {quantity} shares @ ₹{price}")
        except Exception as e:
            print(f"❌ Failed to add {symbol}: {e}")
    
    # Update prices
    print("\n🔄 Updating current prices...")
    updated_prices = db.update_prices(portfolio_id)
    for symbol, price in updated_prices.items():
        print(f"✅ {symbol}: ₹{price:.2f}")
    
    # Get portfolio summary
    print("\n📊 Portfolio Summary:")
    summary = db.get_portfolio_summary(portfolio_id)
    
    if 'error' not in summary:
        print(f"💰 Total Value: ₹{summary['total_value']:,.2f}")
        print(f"📈 Total Return: ₹{summary['total_return']:,.2f} ({summary['total_return_percent']:+.2f}%)")
        print(f"🏢 Holdings: {summary['holdings_count']} stocks")
        print(f"💵 Cash: ₹{summary['cash_balance']:,.2f}")
        
        print("\n🏢 Sector Allocation:")
        for sector, percentage in summary['sector_allocation'].items():
            print(f"   {sector}: {percentage:.1f}%")
    else:
        print(f"❌ Error: {summary['error']}")
    
    print("\n🎉 Portfolio database system ready!")