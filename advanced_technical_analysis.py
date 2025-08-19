# advanced_technical_analysis.py
"""
Advanced Technical Analysis Engine for Rudh Financial Intelligence
Adds RSI, MACD, Bollinger Bands, and Chennai market insights
"""
import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio

logger = logging.getLogger(__name__)

class AdvancedTechnicalAnalysis:
    """Advanced technical analysis engine with Chennai market intelligence"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Chennai market symbols for regional analysis
        self.chennai_stocks = {
            'TVS': 'TVSMOTOR.NS',
            'ASHOKLEY': 'ASHOKLEY.NS',
            'TIINDIA': 'TIINDIA.NS',
            'MOTHERSON': 'MOTHERSON.NS',
            'APOLLO': 'APOLLOTYRE.NS',
            'TNPL': 'TNPL.NS'
        }
        
        # Sector classifications for analysis
        self.sectors = {
            'IT': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS'],
            'Banking': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS'],
            'Auto': ['TVSMOTOR.NS', 'ASHOKLEY.NS', 'MARUTI.NS', 'M&M.NS'],
            'Energy': ['RELIANCE.NS', 'ONGC.NS', 'IOC.NS', 'BPCL.NS']
        }
        
        logger.info("✅ Advanced Technical Analysis Engine initialized")
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series()
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD indicator"""
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'histogram': histogram.iloc[-1],
                'crossover': 'bullish' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'bearish'
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {}
    
    def calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            current_price = prices.iloc[-1]
            current_sma = sma.iloc[-1]
            current_upper = upper_band.iloc[-1]
            current_lower = lower_band.iloc[-1]
            
            # Band position analysis
            band_position = (current_price - current_lower) / (current_upper - current_lower) * 100
            
            signal = 'neutral'
            if current_price > current_upper:
                signal = 'overbought'
            elif current_price < current_lower:
                signal = 'oversold'
            elif band_position > 80:
                signal = 'approaching_overbought'
            elif band_position < 20:
                signal = 'approaching_oversold'
            
            return {
                'upper_band': current_upper,
                'middle_band': current_sma,
                'lower_band': current_lower,
                'position': band_position,
                'signal': signal
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {}
    
    def calculate_support_resistance(self, prices: pd.Series, volume: pd.Series = None) -> Dict:
        """Calculate dynamic support and resistance levels"""
        try:
            # Find local peaks and troughs
            high_prices = prices.rolling(window=5, center=True).max()
            low_prices = prices.rolling(window=5, center=True).min()
            
            resistance_levels = []
            support_levels = []
            
            for i in range(len(prices)):
                if prices.iloc[i] == high_prices.iloc[i]:
                    resistance_levels.append(prices.iloc[i])
                if prices.iloc[i] == low_prices.iloc[i]:
                    support_levels.append(prices.iloc[i])
            
            # Get most significant levels
            current_price = prices.iloc[-1]
            
            resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.05)
            support = max([s for s in support_levels if s < current_price], default=current_price * 0.95)
            
            return {
                'resistance': resistance,
                'support': support,
                'distance_to_resistance': ((resistance - current_price) / current_price) * 100,
                'distance_to_support': ((current_price - support) / current_price) * 100
            }
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}")
            return {}
    
    async def get_advanced_analysis(self, symbol: str, period: str = "6mo") -> Dict:
        """Get comprehensive technical analysis for a symbol"""
        try:
            # Ensure symbol has correct suffix
            if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                symbol = f"{symbol}.NS"
            
            logger.info(f"🔍 Getting advanced analysis for {symbol}")
            
            # Fetch data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return {'error': f'No data available for {symbol}'}
            
            closes = hist['Close']
            volumes = hist['Volume']
            
            # Calculate all technical indicators
            rsi = self.calculate_rsi(closes)
            macd = self.calculate_macd(closes)
            bollinger = self.calculate_bollinger_bands(closes)
            support_resistance = self.calculate_support_resistance(closes, volumes)
            
            # Price analysis
            current_price = closes.iloc[-1]
            price_change = ((current_price - closes.iloc[-2]) / closes.iloc[-2]) * 100
            
            # Moving averages
            sma_20 = closes.rolling(20).mean().iloc[-1]
            sma_50 = closes.rolling(50).mean().iloc[-1]
            ema_12 = closes.ewm(span=12).mean().iloc[-1]
            
            # Volume analysis
            avg_volume = volumes.rolling(20).mean().iloc[-1]
            current_volume = volumes.iloc[-1]
            volume_ratio = current_volume / avg_volume
            
            # Overall technical signal
            signals = []
            if not rsi.empty and rsi.iloc[-1] < 30:
                signals.append('oversold')
            elif not rsi.empty and rsi.iloc[-1] > 70:
                signals.append('overbought')
            
            if macd.get('crossover') == 'bullish':
                signals.append('macd_bullish')
            elif macd.get('crossover') == 'bearish':
                signals.append('macd_bearish')
            
            if bollinger.get('signal') in ['oversold', 'approaching_oversold']:
                signals.append('bb_buy')
            elif bollinger.get('signal') in ['overbought', 'approaching_overbought']:
                signals.append('bb_sell')
            
            # Generate overall recommendation
            bullish_signals = sum(1 for s in signals if s in ['oversold', 'macd_bullish', 'bb_buy'])
            bearish_signals = sum(1 for s in signals if s in ['overbought', 'macd_bearish', 'bb_sell'])
            
            if bullish_signals > bearish_signals:
                overall_signal = 'BUY'
                confidence = min(90, 60 + (bullish_signals * 10))
            elif bearish_signals > bullish_signals:
                overall_signal = 'SELL'
                confidence = min(90, 60 + (bearish_signals * 10))
            else:
                overall_signal = 'HOLD'
                confidence = 50
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'price_change': price_change,
                'technical_indicators': {
                    'rsi': rsi.iloc[-1] if not rsi.empty else None,
                    'macd': macd,
                    'bollinger_bands': bollinger,
                    'support_resistance': support_resistance
                },
                'moving_averages': {
                    'sma_20': sma_20,
                    'sma_50': sma_50,
                    'ema_12': ema_12
                },
                'volume_analysis': {
                    'current_volume': current_volume,
                    'average_volume': avg_volume,
                    'volume_ratio': volume_ratio
                },
                'signals': signals,
                'recommendation': {
                    'action': overall_signal,
                    'confidence': confidence,
                    'target_price': support_resistance.get('resistance', current_price * 1.05),
                    'stop_loss': support_resistance.get('support', current_price * 0.95)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in advanced analysis for {symbol}: {e}")
            return {'error': str(e)}
    
    async def get_sector_analysis(self, sector: str) -> Dict:
        """Analyze an entire sector performance"""
        try:
            if sector.upper() not in self.sectors:
                return {'error': f'Sector {sector} not recognized. Available: {list(self.sectors.keys())}'}
            
            sector_stocks = self.sectors[sector.upper()]
            sector_data = []
            
            logger.info(f"📊 Analyzing {sector.upper()} sector ({len(sector_stocks)} stocks)")
            
            for symbol in sector_stocks:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period="1d")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        change_pct = ((current_price - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1]) * 100
                        
                        sector_data.append({
                            'symbol': symbol,
                            'name': info.get('shortName', symbol),
                            'price': current_price,
                            'change_pct': change_pct,
                            'market_cap': info.get('marketCap', 0)
                        })
                except Exception as e:
                    logger.warning(f"Failed to get data for {symbol}: {e}")
                    continue
            
            if not sector_data:
                return {'error': f'No data available for {sector} sector'}
            
            # Calculate sector metrics
            avg_change = sum(stock['change_pct'] for stock in sector_data) / len(sector_data)
            best_performer = max(sector_data, key=lambda x: x['change_pct'])
            worst_performer = min(sector_data, key=lambda x: x['change_pct'])
            
            # Sector sentiment
            positive_stocks = sum(1 for stock in sector_data if stock['change_pct'] > 0)
            sentiment_score = (positive_stocks / len(sector_data)) * 100
            
            if sentiment_score > 70:
                sentiment = 'VERY_POSITIVE'
            elif sentiment_score > 50:
                sentiment = 'POSITIVE'
            elif sentiment_score > 30:
                sentiment = 'NEUTRAL'
            else:
                sentiment = 'NEGATIVE'
            
            return {
                'sector': sector.upper(),
                'average_change': avg_change,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'best_performer': best_performer,
                'worst_performer': worst_performer,
                'total_stocks': len(sector_data),
                'positive_stocks': positive_stocks,
                'stocks': sector_data
            }
            
        except Exception as e:
            logger.error(f"Error in sector analysis: {e}")
            return {'error': str(e)}
    
    async def get_chennai_market_intelligence(self) -> Dict:
        """Get Chennai-specific market insights"""
        try:
            logger.info("🏛️ Analyzing Chennai market intelligence")
            
            chennai_data = []
            for name, symbol in self.chennai_stocks.items():
                try:
                    analysis = await self.get_advanced_analysis(symbol)
                    if 'error' not in analysis:
                        chennai_data.append({
                            'name': name,
                            'symbol': symbol,
                            'price': analysis['current_price'],
                            'change': analysis['price_change'],
                            'recommendation': analysis['recommendation']['action'],
                            'confidence': analysis['recommendation']['confidence'],
                            'rsi': analysis['technical_indicators']['rsi']
                        })
                except Exception as e:
                    logger.warning(f"Failed to analyze {name}: {e}")
                    continue
            
            if not chennai_data:
                return {'error': 'No Chennai market data available'}
            
            # Chennai market metrics
            avg_change = sum(stock['change'] for stock in chennai_data) / len(chennai_data)
            buy_recommendations = sum(1 for stock in chennai_data if stock['recommendation'] == 'BUY')
            
            chennai_sentiment = 'POSITIVE' if avg_change > 0 else 'NEGATIVE'
            if abs(avg_change) < 0.5:
                chennai_sentiment = 'NEUTRAL'
            
            # Top picks from Chennai
            top_pick = max(chennai_data, key=lambda x: x['confidence']) if chennai_data else None
            
            return {
                'chennai_market_summary': {
                    'average_change': avg_change,
                    'sentiment': chennai_sentiment,
                    'buy_recommendations': buy_recommendations,
                    'total_stocks': len(chennai_data),
                    'top_chennai_pick': top_pick
                },
                'chennai_stocks': chennai_data
            }
            
        except Exception as e:
            logger.error(f"Error in Chennai market analysis: {e}")
            return {'error': str(e)}

# Test the advanced technical analysis
if __name__ == "__main__":
    async def test_advanced_analysis():
        analyzer = AdvancedTechnicalAnalysis()
        
        print("🧪 Testing Advanced Technical Analysis...")
        
        # Test individual stock analysis
        print("\n📊 Testing RELIANCE analysis...")
        reliance_analysis = await analyzer.get_advanced_analysis("RELIANCE")
        if 'error' not in reliance_analysis:
            print(f"✅ RELIANCE: ₹{reliance_analysis['current_price']:.2f}")
            print(f"   RSI: {reliance_analysis['technical_indicators']['rsi']:.1f}")
            print(f"   MACD: {reliance_analysis['technical_indicators']['macd']['crossover']}")
            print(f"   Recommendation: {reliance_analysis['recommendation']['action']} ({reliance_analysis['recommendation']['confidence']}%)")
        
        # Test sector analysis
        print("\n🏦 Testing IT sector analysis...")
        it_analysis = await analyzer.get_sector_analysis("IT")
        if 'error' not in it_analysis:
            print(f"✅ IT Sector: {it_analysis['average_change']:.2f}% average change")
            print(f"   Sentiment: {it_analysis['sentiment']} ({it_analysis['sentiment_score']:.1f}%)")
            print(f"   Best: {it_analysis['best_performer']['name']} (+{it_analysis['best_performer']['change_pct']:.2f}%)")
        
        # Test Chennai market intelligence
        print("\n🏛️ Testing Chennai market intelligence...")
        chennai_analysis = await analyzer.get_chennai_market_intelligence()
        if 'error' not in chennai_analysis:
            summary = chennai_analysis['chennai_market_summary']
            print(f"✅ Chennai Market: {summary['average_change']:.2f}% average change")
            print(f"   Sentiment: {summary['sentiment']}")
            if summary['top_chennai_pick']:
                top = summary['top_chennai_pick']
                print(f"   Top Pick: {top['name']} - {top['recommendation']} ({top['confidence']}%)")
        
        print("\n🎯 Advanced Technical Analysis Engine Ready!")
    
    # Run the test
    asyncio.run(test_advanced_analysis())