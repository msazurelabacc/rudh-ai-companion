# rudh_financial_advisor_minimal.py
"""
Minimal Working Financial Advisor - All features in one file
"""

import asyncio
import logging
import sys
from datetime import datetime

# Import existing modules
sys.path.append('src')
from config.config import RudhConfig
from financial_intelligence_engine import FinancialIntelligenceEngine

# Import existing services
try:
    from azure_speech_service import AzureSpeechService
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    from azure_openai_service import AzureOpenAIService
    AZURE_AI_AVAILABLE = True
except ImportError:
    AZURE_AI_AVAILABLE = False

class SimpleFinancialAdvisor:
    """Simple but complete financial advisor"""
    
    def __init__(self):
        self.financial_engine = FinancialIntelligenceEngine()
        
        # Initialize services
        if AZURE_AI_AVAILABLE:
            self.ai_service = AzureOpenAIService()
            self.ai_available = True
        else:
            self.ai_available = False
            
        if VOICE_AVAILABLE:
            self.voice_service = AzureSpeechService()
            self.voice_available = self.voice_service.is_available
        else:
            self.voice_available = False
        
        self.voice_enabled = True
        self.session_start = datetime.now()
        self.query_count = 0
        
        print("✅ Simple Financial Advisor initialized")
    
    async def speak(self, text):
        """Speak text if voice is available and enabled"""
        if self.voice_available and self.voice_enabled:
            print("🎵 Speaking response...")
            await self.voice_service.speak_text(text, "neutral")
    
    async def run(self):
        """Main advisor loop"""
        print("=" * 80)
        print("🤖 RUDH FINANCIAL ADVISOR - SIMPLE VERSION")
        print("   Voice-Enhanced Financial Intelligence for Chennai Markets")
        print("=" * 80)
        
        print(f"🧠 STATUS:")
        print(f"   📈 Market Data: ✅ Live NSE/BSE/Global")
        print(f"   🗣️ Voice: {'✅ Enabled' if self.voice_available else '📝 Text Only'}")
        print(f"   🤖 AI: {'✅ GPT-4o Connected' if self.ai_available else '🔧 Basic Mode'}")
        
        welcome = "Welcome to your Chennai financial advisor! I can analyze stocks, show market overview, review portfolios, and recommend investments."
        print(f"\n💬 {welcome}")
        await self.speak(welcome)
        
        print(f"\n📋 COMMANDS:")
        print(f"   analyze SYMBOL    - Stock analysis (e.g., 'analyze RELIANCE')")
        print(f"   market           - Market overview")
        print(f"   portfolio        - Portfolio review")
        print(f"   recommend        - Stock recommendations")
        print(f"   /voice           - Toggle voice on/off")
        print(f"   /quit            - Exit")
        print("-" * 80)
        
        while True:
            try:
                self.query_count += 1
                user_input = input(f"\n[{self.query_count}] 💰 Your question: ").strip().lower()
                
                if not user_input:
                    continue
                
                start_time = datetime.now()
                
                if user_input == "/quit":
                    await self.handle_quit()
                    break
                elif user_input == "/voice":
                    await self.toggle_voice()
                elif user_input.startswith("analyze "):
                    symbol = user_input.replace("analyze ", "").upper()
                    await self.analyze_stock(symbol)
                elif user_input in ["market", "market overview"]:
                    await self.market_overview()
                elif user_input in ["portfolio", "portfolio review"]:
                    await self.portfolio_review()
                elif user_input in ["recommend", "recommend stocks", "recommendations"]:
                    await self.recommend_stocks()
                else:
                    await self.general_response(user_input)
                
                # Show timing
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"   ⚡ Response time: {elapsed:.2f}s")
                
            except KeyboardInterrupt:
                await self.handle_quit()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def analyze_stock(self, symbol):
        """Analyze a stock"""
        print(f"🧠 Analyzing {symbol}...")
        
        try:
            # Get stock data
            stock_data = await self.financial_engine.get_stock_data(symbol)
            if not stock_data:
                response = f"❌ Could not find data for {symbol}"
                print(response)
                await self.speak(response)
                return
            
            # Get recommendation
            rec = await self.financial_engine.analyze_stock(symbol)
            
            # Format response
            response = f"""📊 ANALYSIS FOR {stock_data.name} ({symbol})

💰 Current Price: ₹{stock_data.current_price:,.2f} ({stock_data.change_percent:+.2f}% today)
📈 Day Range: ₹{stock_data.day_range[0]:,.2f} - ₹{stock_data.day_range[1]:,.2f}
📅 52-Week: ₹{stock_data.week_52_range[0]:,.2f} - ₹{stock_data.week_52_range[1]:,.2f}"""

            if stock_data.pe_ratio:
                response += f"\n📊 P/E Ratio: {stock_data.pe_ratio:.2f}"
            
            action_emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(rec.action, "⚪")
            response += f"""

{action_emoji} RECOMMENDATION: {rec.action} (Confidence: {rec.confidence:.0%})
🎯 Target: ₹{rec.target_price:,.2f} | Stop Loss: ₹{rec.stop_loss:,.2f}
⚠️ Risk: {rec.risk_level} | Allocation: {rec.allocation_percent:.1f}%

💡 {rec.reasoning}"""
            
            print(response)
            
            # Voice summary
            voice_text = f"Analysis for {stock_data.name}. Currently {stock_data.current_price:.0f} rupees, {abs(stock_data.change_percent):.1f} percent {'up' if stock_data.change_percent >= 0 else 'down'} today. My recommendation is {rec.action.lower()} with {rec.confidence:.0f} percent confidence."
            await self.speak(voice_text)
            
        except Exception as e:
            error = f"Analysis failed for {symbol}: {e}"
            print(f"❌ {error}")
            await self.speak(f"Analysis failed for {symbol}")
    
    async def market_overview(self):
        """Show market overview"""
        print("🧠 Getting market overview...")
        
        try:
            overview = await self.financial_engine.get_market_overview()
            
            response = "🌐 MARKET OVERVIEW\n"
            
            # Indices
            if "indices" in overview:
                response += "\n📊 MAJOR INDICES:\n"
                for index, data in overview["indices"].items():
                    direction = "🟢" if data["change_percent"] >= 0 else "🔴"
                    response += f"{direction} {index}: {data['current']:.2f} ({data['change_percent']:+.2f}%)\n"
            
            # Indian stocks
            if "top_indian_stocks" in overview:
                response += "\n🇮🇳 TOP INDIAN STOCKS:\n"
                for stock, data in overview["top_indian_stocks"].items():
                    direction = "🟢" if data["change_percent"] >= 0 else "🔴"
                    response += f"{direction} {stock}: ₹{data['current']:.2f} ({data['change_percent']:+.2f}%)\n"
            
            sentiment = overview.get("market_sentiment", "NEUTRAL")
            response += f"\n⚖️ Market Sentiment: {sentiment}"
            
            print(response)
            
            # Voice summary
            nifty_text = ""
            if "indices" in overview and "NIFTY50" in overview["indices"]:
                nifty = overview["indices"]["NIFTY50"]
                direction = "up" if nifty["change_percent"] >= 0 else "down"
                nifty_text = f"Nifty is {direction} {abs(nifty['change_percent']):.1f} percent. "
            
            voice_text = f"Market overview: {nifty_text}Overall sentiment is {sentiment.lower()}."
            await self.speak(voice_text)
            
        except Exception as e:
            error = f"Market overview failed: {e}"
            print(f"❌ {error}")
            await self.speak("Market overview failed")
    
    async def portfolio_review(self):
        """Review sample portfolio"""
        print("🧠 Analyzing portfolio...")
        
        # Demo portfolio
        portfolio = [
            {'symbol': 'RELIANCE', 'quantity': 10, 'avg_price': 2500},
            {'symbol': 'TCS', 'quantity': 5, 'avg_price': 3800},
            {'symbol': 'INFY', 'quantity': 15, 'avg_price': 1600},
            {'symbol': 'HDFCBANK', 'quantity': 8, 'avg_price': 1700}
        ]
        
        try:
            analysis = await self.financial_engine.analyze_portfolio(portfolio)
            
            response = f"""💼 PORTFOLIO ANALYSIS (DEMO)

💰 Total Value: ₹{analysis.total_value:,.2f}
📈 Total Return: ₹{analysis.total_return:,.2f} ({analysis.return_percent:+.2f}%)
⚠️ Risk Score: {analysis.risk_score:.1f}/100
🎯 Diversification: {analysis.diversification_score:.1f}/100"""

            if analysis.top_performers:
                response += f"\n🏆 Top Performers: {', '.join(analysis.top_performers[:3])}"
            
            response += "\n\n💡 This is a demo portfolio for testing purposes."
            
            print(response)
            
            # Voice summary
            return_status = "positive" if analysis.return_percent >= 0 else "negative"
            voice_text = f"Portfolio analysis complete. Total value {analysis.total_value:.0f} rupees with {return_status} return of {abs(analysis.return_percent):.1f} percent. Risk score {analysis.risk_score:.0f} out of 100."
            await self.speak(voice_text)
            
        except Exception as e:
            error = f"Portfolio analysis failed: {e}"
            print(f"❌ {error}")
            await self.speak("Portfolio analysis failed")
    
    async def recommend_stocks(self):
        """Recommend stocks"""
        print("🧠 Generating stock recommendations...")
        
        stocks = ["RELIANCE", "TCS", "HDFCBANK"]
        
        response = "🎯 STOCK RECOMMENDATIONS\n\nBased on current market analysis:\n"
        buy_recommendations = []
        
        try:
            for symbol in stocks:
                rec = await self.financial_engine.analyze_stock(symbol)
                action_emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(rec.action, "⚪")
                
                response += f"\n{action_emoji} {symbol}: {rec.action} (Confidence: {rec.confidence:.0%})"
                response += f"\n   Target: ₹{rec.target_price:,.2f} | Risk: {rec.risk_level}"
                
                if rec.action == "BUY":
                    buy_recommendations.append(f"{symbol} with {rec.confidence:.0f} percent confidence")
            
            response += "\n\n💡 Always do your own research before investing!"
            
            print(response)
            
            # Voice summary
            if buy_recommendations:
                voice_text = f"Stock recommendations: {', '.join(buy_recommendations[:2])}. Remember to do your own research."
            else:
                voice_text = "Current recommendations are mostly hold positions. Market conditions suggest caution."
            await self.speak(voice_text)
            
        except Exception as e:
            error = f"Recommendations failed: {e}"
            print(f"❌ {error}")
            await self.speak("Recommendation generation failed")
    
    async def general_response(self, query):
        """Handle general queries"""
        response = f"I understand you asked: '{query}'. Try these commands:\n- analyze RELIANCE\n- market\n- portfolio\n- recommend"
        print(response)
        await self.speak("Try commands like analyze, market overview, portfolio review, or recommend stocks")
    
    async def toggle_voice(self):
        """Toggle voice on/off"""
        if not self.voice_available:
            print("🔧 Voice not available")
            return
        
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        print(f"🎵 Voice {status}")
        
        if self.voice_enabled:
            await self.speak("Voice output enabled")
    
    async def handle_quit(self):
        """Handle exit"""
        session_time = (datetime.now() - self.session_start).total_seconds()
        
        farewell = f"""
👋 Thank you for using Rudh Financial Advisor!

📊 Session Summary:
   • Queries: {self.query_count - 1}
   • Duration: {session_time:.1f} seconds

🚀 May your investments grow and prosper!
        """
        
        print(farewell)
        await self.speak("Thank you for using Rudh Financial Advisor. May your investments prosper!")

async def main():
    """Run the simple financial advisor"""
    try:
        advisor = SimpleFinancialAdvisor()
        await advisor.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())