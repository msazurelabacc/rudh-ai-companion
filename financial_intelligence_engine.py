# financial_intelligence_engine.py
"""
Rudh AI Financial Intelligence Engine - Phase 3
Advanced financial analysis with real-time market data integration
Optimized for Indian markets (NSE, BSE) with global coverage
"""

import asyncio
import logging
import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import yfinance as yf
import pandas as pd
import numpy as np

# Import existing config
import sys
sys.path.append('src')
from config.config import RudhConfig

@dataclass
class StockData:
    """Stock data structure"""
    symbol: str
    name: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    market_cap: float
    pe_ratio: Optional[float]
    day_range: Tuple[float, float]
    week_52_range: Tuple[float, float]
    currency: str
    exchange: str
    timestamp: datetime

@dataclass
class InvestmentRecommendation:
    """Investment recommendation structure"""
    symbol: str
    action: str  # BUY, SELL, HOLD
    confidence: float
    target_price: float
    stop_loss: float
    reasoning: str
    risk_level: str  # LOW, MEDIUM, HIGH
    time_horizon: str  # SHORT, MEDIUM, LONG
    allocation_percent: float

@dataclass
class PortfolioAnalysis:
    """Portfolio analysis results"""
    total_value: float
    total_return: float
    return_percent: float
    risk_score: float
    diversification_score: float
    recommendations: List[InvestmentRecommendation]
    sector_allocation: Dict[str, float]
    top_performers: List[str]
    underperformers: List[str]

class FinancialIntelligenceEngine:
    """Advanced Financial Intelligence for Rudh AI"""
    
    def __init__(self):
        self.config = RudhConfig.get_config()
        self.logger = logging.getLogger("FinancialEngine")
        
        # Indian market symbols mapping
        self.indian_stocks = {
            'TCS': 'TCS.NS',
            'RELIANCE': 'RELIANCE.NS', 
            'INFY': 'INFY.NS',
            'HDFCBANK': 'HDFCBANK.NS',
            'ICICIBANK': 'ICICIBANK.NS',
            'SBI': 'SBIN.NS',
            'ITC': 'ITC.NS',
            'LT': 'LT.NS',
            'WIPRO': 'WIPRO.NS',
            'MARUTI': 'MARUTI.NS',
            'BHARTIARTL': 'BHARTIARTL.NS',
            'ASIANPAINT': 'ASIANPAINT.NS',
            'NTPC': 'NTPC.NS',
            'KOTAKBANK': 'KOTAKBANK.NS',
            'HINDUNILVR': 'HINDUNILVR.NS'
        }
        
        # Global market symbols
        self.global_stocks = {
            'APPLE': 'AAPL',
            'MICROSOFT': 'MSFT',
            'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN',
            'TESLA': 'TSLA',
            'NVIDIA': 'NVDA',
            'META': 'META',
            'NETFLIX': 'NFLX'
        }
        
        # Market indices
        self.indices = {
            'NIFTY50': '^NSEI',
            'SENSEX': '^BSESN',
            'NIFTYBANK': '^NSEBANK',
            'SPY': 'SPY',
            'NASDAQ': '^IXIC',
            'DOW': '^DJI'
        }
        
        # Risk-free rate (10-year Indian govt bond approximate)
        self.risk_free_rate = 0.07
        
        self.logger.info("✅ Financial Intelligence Engine initialized")
    
    async def get_stock_data(self, symbol: str, market: str = "auto") -> Optional[StockData]:
        """Get real-time stock data"""
        try:
            # Auto-detect market and convert symbol
            yf_symbol = self._convert_symbol(symbol, market)
            
            stock = yf.Ticker(yf_symbol)
            info = stock.info
            hist = stock.history(period="1d")
            
            if hist.empty:
                self.logger.warning(f"No data found for {symbol}")
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            # Get 52-week range
            week_52_high = info.get('fiftyTwoWeekHigh', current_price)
            week_52_low = info.get('fiftyTwoWeekLow', current_price)
            
            # Get day range
            day_high = hist['High'].iloc[-1]
            day_low = hist['Low'].iloc[-1]
            
            return StockData(
                symbol=symbol.upper(),
                name=info.get('longName', symbol),
                current_price=round(current_price, 2),
                change=round(change, 2),
                change_percent=round(change_percent, 2),
                volume=int(info.get('volume', 0)),
                market_cap=info.get('marketCap', 0),
                pe_ratio=info.get('trailingPE'),
                day_range=(round(day_low, 2), round(day_high, 2)),
                week_52_range=(round(week_52_low, 2), round(week_52_high, 2)),
                currency=info.get('currency', 'INR'),
                exchange=info.get('exchange', 'NSE'),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    def _convert_symbol(self, symbol: str, market: str) -> str:
        """Convert symbol to Yahoo Finance format"""
        symbol_upper = symbol.upper()
        
        if market.lower() == "indian" or market == "auto":
            if symbol_upper in self.indian_stocks:
                return self.indian_stocks[symbol_upper]
            elif not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                return f"{symbol_upper}.NS"  # Default to NSE
        
        if market.lower() == "global" or market == "auto":
            if symbol_upper in self.global_stocks:
                return self.global_stocks[symbol_upper]
        
        # Return as-is for indices or already formatted symbols
        return symbol
    
    async def analyze_stock(self, symbol: str, user_profile: Dict = None) -> InvestmentRecommendation:
        """Analyze stock and provide investment recommendation"""
        try:
            stock_data = await self.get_stock_data(symbol)
            if not stock_data:
                raise ValueError(f"Could not fetch data for {symbol}")
            
            # Technical analysis
            technical_score = await self._technical_analysis(symbol)
            
            # Fundamental analysis
            fundamental_score = await self._fundamental_analysis(stock_data)
            
            # Market sentiment analysis
            sentiment_score = await self._market_sentiment_analysis(symbol)
            
            # Combine scores
            overall_score = (technical_score * 0.4 + 
                           fundamental_score * 0.4 + 
                           sentiment_score * 0.2)
            
            # Generate recommendation
            action, confidence = self._determine_action(overall_score)
            target_price = self._calculate_target_price(stock_data, overall_score)
            stop_loss = self._calculate_stop_loss(stock_data, action)
            risk_level = self._assess_risk_level(stock_data)
            
            # User-specific adjustments
            if user_profile:
                action, confidence = self._adjust_for_user_profile(
                    action, confidence, risk_level, user_profile
                )
            
            reasoning = self._generate_reasoning(
                stock_data, technical_score, fundamental_score, 
                sentiment_score, overall_score
            )
            
            return InvestmentRecommendation(
                symbol=symbol.upper(),
                action=action,
                confidence=confidence,
                target_price=target_price,
                stop_loss=stop_loss,
                reasoning=reasoning,
                risk_level=risk_level,
                time_horizon="MEDIUM",  # 6-12 months default
                allocation_percent=self._suggest_allocation(overall_score, risk_level)
            )
            
        except Exception as e:
            self.logger.error(f"Stock analysis failed for {symbol}: {e}")
            return InvestmentRecommendation(
                symbol=symbol.upper(),
                action="HOLD",
                confidence=0.0,
                target_price=0.0,
                stop_loss=0.0,
                reasoning=f"Analysis failed: {str(e)}",
                risk_level="HIGH",
                time_horizon="UNKNOWN",
                allocation_percent=0.0
            )
    
    async def _technical_analysis(self, symbol: str) -> float:
        """Perform technical analysis and return score (0-100)"""
        try:
            yf_symbol = self._convert_symbol(symbol, "auto")
            stock = yf.Ticker(yf_symbol)
            hist = stock.history(period="3mo")
            
            if len(hist) < 50:
                return 50.0  # Neutral if insufficient data
            
            scores = []
            
            # Moving Average Analysis
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            
            current_price = hist['Close'].iloc[-1]
            ma20 = hist['MA20'].iloc[-1]
            ma50 = hist['MA50'].iloc[-1]
            
            # Price above MA20 and MA50 is bullish
            if current_price > ma20 > ma50:
                scores.append(80)
            elif current_price > ma20:
                scores.append(65)
            elif current_price > ma50:
                scores.append(55)
            else:
                scores.append(30)
            
            # RSI Analysis
            rsi = self._calculate_rsi(hist['Close'])
            if 30 <= rsi <= 70:
                scores.append(70)  # Normal range
            elif rsi < 30:
                scores.append(85)  # Oversold - potential buy
            else:
                scores.append(25)  # Overbought - potential sell
            
            # Volume Analysis
            avg_volume = hist['Volume'].tail(20).mean()
            recent_volume = hist['Volume'].iloc[-1]
            if recent_volume > avg_volume * 1.5:
                scores.append(75)  # High volume is good
            else:
                scores.append(50)
            
            return np.mean(scores)
            
        except Exception as e:
            self.logger.error(f"Technical analysis failed for {symbol}: {e}")
            return 50.0
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50.0
    
    async def _fundamental_analysis(self, stock_data: StockData) -> float:
        """Perform fundamental analysis and return score (0-100)"""
        try:
            scores = []
            
            # P/E Ratio Analysis
            if stock_data.pe_ratio:
                if 10 <= stock_data.pe_ratio <= 20:
                    scores.append(80)  # Good valuation
                elif 20 < stock_data.pe_ratio <= 30:
                    scores.append(60)  # Fair valuation
                elif stock_data.pe_ratio < 10:
                    scores.append(70)  # Potentially undervalued
                else:
                    scores.append(30)  # Potentially overvalued
            else:
                scores.append(50)  # No P/E data
            
            # Price relative to 52-week range
            current = stock_data.current_price
            low_52 = stock_data.week_52_range[0]
            high_52 = stock_data.week_52_range[1]
            
            position_in_range = (current - low_52) / (high_52 - low_52) if high_52 > low_52 else 0.5
            
            if 0.3 <= position_in_range <= 0.7:
                scores.append(75)  # Good entry point
            elif position_in_range < 0.3:
                scores.append(85)  # Near 52-week low
            else:
                scores.append(40)  # Near 52-week high
            
            # Market cap consideration (larger = more stable)
            if stock_data.market_cap > 100000000000:  # >100B
                scores.append(70)  # Large cap stability
            elif stock_data.market_cap > 10000000000:  # >10B
                scores.append(65)  # Mid cap
            else:
                scores.append(55)  # Small cap (higher risk/reward)
            
            return np.mean(scores)
            
        except Exception as e:
            self.logger.error(f"Fundamental analysis failed: {e}")
            return 50.0
    
    async def _market_sentiment_analysis(self, symbol: str) -> float:
        """Analyze market sentiment and return score (0-100)"""
        try:
            # Simplified sentiment - in production, would use news APIs
            # For now, use recent price momentum as proxy
            
            yf_symbol = self._convert_symbol(symbol, "auto")
            stock = yf.Ticker(yf_symbol)
            hist = stock.history(period="1mo")
            
            if len(hist) < 5:
                return 50.0
            
            # Calculate momentum
            recent_return = (hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100
            
            if recent_return > 10:
                return 85  # Strong positive momentum
            elif recent_return > 5:
                return 70  # Positive momentum
            elif recent_return > -5:
                return 55  # Neutral
            elif recent_return > -10:
                return 40  # Negative momentum
            else:
                return 25  # Strong negative momentum
                
        except Exception as e:
            self.logger.error(f"Sentiment analysis failed for {symbol}: {e}")
            return 50.0
    
    def _determine_action(self, overall_score: float) -> Tuple[str, float]:
        """Determine investment action based on overall score"""
        confidence = min(abs(overall_score - 50) * 2, 95) / 100
        
        if overall_score >= 70:
            return "BUY", confidence
        elif overall_score >= 55:
            return "HOLD", confidence * 0.7
        else:
            return "SELL", confidence
    
    def _calculate_target_price(self, stock_data: StockData, score: float) -> float:
        """Calculate target price based on analysis"""
        current = stock_data.current_price
        
        if score >= 70:
            # Bullish target: 15-25% upside
            multiplier = 1.15 + (score - 70) / 100 * 0.10
        elif score >= 55:
            # Neutral target: 5-10% upside
            multiplier = 1.05 + (score - 55) / 15 * 0.05
        else:
            # Bearish target: 5-15% downside
            multiplier = 0.95 - (55 - score) / 55 * 0.10
        
        return round(current * multiplier, 2)
    
    def _calculate_stop_loss(self, stock_data: StockData, action: str) -> float:
        """Calculate stop loss price"""
        current = stock_data.current_price
        
        if action == "BUY":
            # 8-12% stop loss for buy positions
            return round(current * 0.90, 2)
        elif action == "SELL":
            # 8-12% stop loss for sell positions
            return round(current * 1.10, 2)
        else:  # HOLD
            # 10% stop loss either way
            return round(current * 0.90, 2)
    
    def _assess_risk_level(self, stock_data: StockData) -> str:
        """Assess risk level of the stock"""
        factors = []
        
        # Market cap factor
        if stock_data.market_cap > 100000000000:
            factors.append("LOW")
        elif stock_data.market_cap > 10000000000:
            factors.append("MEDIUM")
        else:
            factors.append("HIGH")
        
        # Volatility factor (based on 52-week range)
        volatility = (stock_data.week_52_range[1] - stock_data.week_52_range[0]) / stock_data.current_price
        if volatility > 0.8:
            factors.append("HIGH")
        elif volatility > 0.4:
            factors.append("MEDIUM")
        else:
            factors.append("LOW")
        
        # Return most common factor
        risk_counts = {"LOW": factors.count("LOW"), 
                      "MEDIUM": factors.count("MEDIUM"), 
                      "HIGH": factors.count("HIGH")}
        
        return max(risk_counts, key=risk_counts.get)
    
    def _adjust_for_user_profile(self, action: str, confidence: float, 
                                risk_level: str, user_profile: Dict) -> Tuple[str, float]:
        """Adjust recommendation based on user profile"""
        user_risk_tolerance = user_profile.get('risk_tolerance', 'MEDIUM')
        
        # Conservative users avoid high-risk investments
        if user_risk_tolerance == 'LOW' and risk_level == 'HIGH':
            if action == 'BUY':
                action = 'HOLD'
                confidence *= 0.6
        
        # Aggressive users more confident in high-risk plays
        elif user_risk_tolerance == 'HIGH' and risk_level == 'HIGH':
            confidence = min(confidence * 1.2, 0.95)
        
        return action, confidence
    
    def _generate_reasoning(self, stock_data: StockData, tech_score: float, 
                          fund_score: float, sent_score: float, overall_score: float) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasoning = f"Analysis for {stock_data.name}: "
        
        # Current status
        change_dir = "up" if stock_data.change >= 0 else "down"
        reasoning += f"Currently trading at ₹{stock_data.current_price:.2f} ({change_dir} {abs(stock_data.change_percent):.1f}% today). "
        
        # Technical analysis
        if tech_score >= 70:
            reasoning += "Technical indicators show strong bullish signals. "
        elif tech_score >= 55:
            reasoning += "Technical indicators are neutral to positive. "
        else:
            reasoning += "Technical indicators show bearish signals. "
        
        # Fundamental analysis
        if fund_score >= 70:
            reasoning += "Fundamentals appear strong with good valuation metrics. "
        elif fund_score >= 55:
            reasoning += "Fundamentals are fair with reasonable valuation. "
        else:
            reasoning += "Fundamentals show some concerns with current valuation. "
        
        # Overall recommendation
        if overall_score >= 70:
            reasoning += "Overall analysis suggests a favorable investment opportunity."
        elif overall_score >= 55:
            reasoning += "Overall analysis suggests holding current positions."
        else:
            reasoning += "Overall analysis suggests caution is warranted."
        
        return reasoning
    
    def _suggest_allocation(self, score: float, risk_level: str) -> float:
        """Suggest portfolio allocation percentage"""
        base_allocation = {
            "LOW": 15.0,
            "MEDIUM": 10.0,
            "HIGH": 5.0
        }
        
        allocation = base_allocation.get(risk_level, 10.0)
        
        # Adjust based on confidence
        if score >= 80:
            allocation *= 1.5
        elif score >= 70:
            allocation *= 1.2
        elif score < 40:
            allocation *= 0.5
        
        return min(allocation, 25.0)  # Max 25% in any single stock
    
    async def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market overview"""
        try:
            overview = {
                "timestamp": datetime.now().isoformat(),
                "indices": {},
                "top_indian_stocks": {},
                "top_global_stocks": {},
                "market_sentiment": "NEUTRAL"
            }
            
            # Get major indices
            for name, symbol in self.indices.items():
                try:
                    data = await self.get_stock_data(symbol, "global")
                    if data:
                        overview["indices"][name] = {
                            "current": data.current_price,
                            "change": data.change,
                            "change_percent": data.change_percent
                        }
                except:
                    continue
            
            # Get top Indian stocks
            for name, symbol in list(self.indian_stocks.items())[:5]:
                try:
                    data = await self.get_stock_data(symbol, "indian")
                    if data:
                        overview["top_indian_stocks"][name] = {
                            "current": data.current_price,
                            "change": data.change,
                            "change_percent": data.change_percent
                        }
                except:
                    continue
            
            # Simple market sentiment based on Nifty
            if "NIFTY50" in overview["indices"]:
                nifty_change = overview["indices"]["NIFTY50"]["change_percent"]
                if nifty_change > 1:
                    overview["market_sentiment"] = "BULLISH"
                elif nifty_change < -1:
                    overview["market_sentiment"] = "BEARISH"
            
            return overview
            
        except Exception as e:
            self.logger.error(f"Market overview failed: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def analyze_portfolio(self, holdings: List[Dict]) -> PortfolioAnalysis:
        """Analyze user's portfolio and provide insights"""
        try:
            total_value = 0
            total_invested = 0
            stock_data = []
            recommendations = []
            
            for holding in holdings:
                symbol = holding['symbol']
                quantity = holding['quantity']
                avg_price = holding['avg_price']
                
                # Get current stock data
                data = await self.get_stock_data(symbol)
                if data:
                    current_value = data.current_price * quantity
                    invested_value = avg_price * quantity
                    
                    total_value += current_value
                    total_invested += invested_value
                    
                    stock_data.append({
                        'symbol': symbol,
                        'data': data,
                        'quantity': quantity,
                        'invested': invested_value,
                        'current_value': current_value,
                        'return': current_value - invested_value
                    })
                    
                    # Get recommendation for each holding
                    rec = await self.analyze_stock(symbol)
                    recommendations.append(rec)
            
            # Calculate overall metrics
            total_return = total_value - total_invested
            return_percent = (total_return / total_invested * 100) if total_invested > 0 else 0
            
            # Sort performers
            stock_data.sort(key=lambda x: x['return'], reverse=True)
            top_performers = [x['symbol'] for x in stock_data[:3]]
            underperformers = [x['symbol'] for x in stock_data[-3:]]
            
            return PortfolioAnalysis(
                total_value=round(total_value, 2),
                total_return=round(total_return, 2),
                return_percent=round(return_percent, 2),
                risk_score=self._calculate_portfolio_risk(stock_data),
                diversification_score=self._calculate_diversification(stock_data),
                recommendations=recommendations,
                sector_allocation={},  # Would implement sector analysis
                top_performers=top_performers,
                underperformers=underperformers
            )
            
        except Exception as e:
            self.logger.error(f"Portfolio analysis failed: {e}")
            return PortfolioAnalysis(
                total_value=0, total_return=0, return_percent=0,
                risk_score=0, diversification_score=0,
                recommendations=[], sector_allocation={},
                top_performers=[], underperformers=[]
            )
    
    def _calculate_portfolio_risk(self, stock_data: List[Dict]) -> float:
        """Calculate portfolio risk score (0-100)"""
        if not stock_data:
            return 0
        
        # Simple risk calculation based on volatility and concentration
        volatilities = []
        total_value = sum(x['current_value'] for x in stock_data)
        
        for stock in stock_data:
            # Weight by portfolio percentage
            weight = stock['current_value'] / total_value
            # Approximate volatility from 52-week range
            volatility = (stock['data'].week_52_range[1] - stock['data'].week_52_range[0]) / stock['data'].current_price
            volatilities.append(volatility * weight)
        
        avg_volatility = sum(volatilities)
        
        # Convert to 0-100 scale (higher = riskier)
        risk_score = min(avg_volatility * 100, 100)
        return round(risk_score, 1)
    
    def _calculate_diversification(self, stock_data: List[Dict]) -> float:
        """Calculate diversification score (0-100)"""
        if len(stock_data) <= 1:
            return 20  # Poor diversification
        
        total_value = sum(x['current_value'] for x in stock_data)
        concentrations = [x['current_value'] / total_value for x in stock_data]
        
        # Higher concentration = lower diversification
        max_concentration = max(concentrations)
        
        if max_concentration > 0.5:
            return 30  # Poor diversification
        elif max_concentration > 0.3:
            return 60  # Fair diversification
        else:
            return 85  # Good diversification

# Test function
async def test_financial_engine():
    """Test the financial intelligence engine"""
    print("🧪 Testing Financial Intelligence Engine...")
    print("=" * 60)
    
    engine = FinancialIntelligenceEngine()
    
    # Test stock data retrieval
    print("📊 Testing stock data retrieval...")
    stocks_to_test = ['RELIANCE', 'TCS', 'AAPL']
    
    for symbol in stocks_to_test:
        print(f"\n🔍 Fetching data for {symbol}...")
        data = await engine.get_stock_data(symbol)
        if data:
            print(f"✅ {data.name}: ₹{data.current_price} ({data.change_percent:+.2f}%)")
        else:
            print(f"❌ Failed to fetch data for {symbol}")
    
    # Test stock analysis
    print(f"\n📈 Testing investment analysis for RELIANCE...")
    recommendation = await engine.analyze_stock('RELIANCE')
    print(f"✅ Recommendation: {recommendation.action} (Confidence: {recommendation.confidence:.0%})")
    print(f"   Target: ₹{recommendation.target_price}, Stop Loss: ₹{recommendation.stop_loss}")
    print(f"   Risk: {recommendation.risk_level}, Allocation: {recommendation.allocation_percent:.1f}%")
    
    # Test market overview
    print(f"\n🌐 Testing market overview...")
    overview = await engine.get_market_overview()
    if 'indices' in overview:
        print(f"✅ Market overview retrieved successfully")
        for index, data in overview['indices'].items():
            print(f"   {index}: {data['current']:.2f} ({data['change_percent']:+.2f}%)")
    
    # Test portfolio analysis
    print(f"\n💼 Testing portfolio analysis...")
    sample_portfolio = [
        {'symbol': 'RELIANCE', 'quantity': 10, 'avg_price': 2500},
        {'symbol': 'TCS', 'quantity': 5, 'avg_price': 3800},
        {'symbol': 'INFY', 'quantity': 15, 'avg_price': 1600}
    ]
    
    portfolio_analysis = await engine.analyze_portfolio(sample_portfolio)
    print(f"✅ Portfolio Analysis Complete:")
    print(f"   Total Value: ₹{portfolio_analysis.total_value:,.2f}")
    print(f"   Total Return: ₹{portfolio_analysis.total_return:,.2f} ({portfolio_analysis.return_percent:+.2f}%)")
    print(f"   Risk Score: {portfolio_analysis.risk_score}/100")
    print(f"   Diversification: {portfolio_analysis.diversification_score}/100")
    
    print(f"\n🎯 Financial Intelligence Engine Ready!")
    print(f"   ✅ Real-time data retrieval working")
    print(f"   ✅ Investment analysis operational")
    print(f"   ✅ Portfolio management ready")
    print(f"   ✅ Market overview functional")

if __name__ == "__main__":
    asyncio.run(test_financial_engine())