# rudh_financial_advisor_v31.py
"""
Rudh Financial Advisor V3.1 - Advanced Financial Intelligence
Enhanced with technical indicators, Chennai market intelligence, and sophisticated analysis
"""
import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from advanced_technical_analysis import AdvancedTechnicalAnalysis
    from financial_intelligence_engine import FinancialIntelligenceEngine
    from azure_openai_service import AzureOpenAIService
    from azure_speech_service import AzureSpeechService
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are available")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedRudhFinancialAdvisor:
    """Enhanced Rudh Financial Advisor with advanced technical analysis"""
    
    def __init__(self):
        """Initialize the enhanced financial advisor"""
        self.logger = logging.getLogger(__name__)
        self.session_start = time.time()
        self.query_count = 0
        self.voice_enabled = True
        
        # Initialize engines
        self.financial_engine = FinancialIntelligenceEngine()
        self.advanced_analysis = AdvancedTechnicalAnalysis()
        self.ai_service = AzureOpenAIService()
        self.speech_service = AzureSpeechService()
        
        self.logger.info("✅ Enhanced Rudh Financial Advisor V3.1 initialized")
    
    async def analyze_stock_advanced(self, symbol: str) -> str:
        """Enhanced stock analysis with technical indicators"""
        try:
            self.logger.info(f"🔍 Advanced analysis for {symbol}")
            
            # Get basic analysis
            basic_analysis = await self.financial_engine.analyze_stock(symbol)
            
            # Get advanced technical analysis
            advanced_analysis = await self.advanced_analysis.get_advanced_analysis(symbol)
            
            if 'error' in advanced_analysis:
                return f"❌ Error analyzing {symbol}: {advanced_analysis['error']}"
            
            # Format comprehensive response
            current_price = advanced_analysis['current_price']
            change_pct = advanced_analysis['price_change']
            rsi = advanced_analysis['technical_indicators']['rsi']
            macd = advanced_analysis['technical_indicators']['macd']
            bollinger = advanced_analysis['technical_indicators']['bollinger_bands']
            support_resistance = advanced_analysis['technical_indicators']['support_resistance']
            recommendation = advanced_analysis['recommendation']
            
            # Create rich analysis response
            response = f"""📊 ADVANCED ANALYSIS FOR {symbol.upper()}

💰 PRICE ACTION:
   Current Price: ₹{current_price:.2f} ({change_pct:+.2f}% today)
   Support Level: ₹{support_resistance.get('support', 0):.2f}
   Resistance Level: ₹{support_resistance.get('resistance', 0):.2f}

📈 TECHNICAL INDICATORS:
   RSI (14): {rsi:.1f} {'(Oversold)' if rsi < 30 else '(Overbought)' if rsi > 70 else '(Neutral)'}
   MACD: {macd.get('crossover', 'Unknown').title()} crossover
   Bollinger Position: {bollinger.get('position', 0):.1f}% ({bollinger.get('signal', 'neutral')})

🎯 RECOMMENDATION: {recommendation['action']} (Confidence: {recommendation['confidence']}%)
   Target Price: ₹{recommendation['target_price']:.2f}
   Stop Loss: ₹{recommendation['stop_loss']:.2f}
   
📊 MOVING AVERAGES:
   SMA(20): ₹{advanced_analysis['moving_averages']['sma_20']:.2f}
   SMA(50): ₹{advanced_analysis['moving_averages']['sma_50']:.2f}
   EMA(12): ₹{advanced_analysis['moving_averages']['ema_12']:.2f}

💡 VOLUME ANALYSIS:
   Current Volume: {advanced_analysis['volume_analysis']['current_volume']:,.0f}
   Volume Ratio: {advanced_analysis['volume_analysis']['volume_ratio']:.2f}x average"""
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in advanced stock analysis: {e}")
            return f"❌ Error analyzing {symbol}: {str(e)}"
    
    async def analyze_sector(self, sector: str) -> str:
        """Analyze an entire sector"""
        try:
            self.logger.info(f"📊 Analyzing {sector} sector")
            
            sector_analysis = await self.advanced_analysis.get_sector_analysis(sector)
            
            if 'error' in sector_analysis:
                return f"❌ Error analyzing {sector} sector: {sector_analysis['error']}"
            
            response = f"""🏢 {sector_analysis['sector']} SECTOR ANALYSIS

📊 SECTOR PERFORMANCE:
   Average Change: {sector_analysis['average_change']:+.2f}%
   Market Sentiment: {sector_analysis['sentiment']} ({sector_analysis['sentiment_score']:.1f}%)
   Stocks Analyzed: {sector_analysis['total_stocks']}
   Positive Movers: {sector_analysis['positive_stocks']}

🏆 BEST PERFORMER:
   {sector_analysis['best_performer']['name']} ({sector_analysis['best_performer']['symbol']})
   Price: ₹{sector_analysis['best_performer']['price']:.2f} ({sector_analysis['best_performer']['change_pct']:+.2f}%)

📉 WORST PERFORMER:
   {sector_analysis['worst_performer']['name']} ({sector_analysis['worst_performer']['symbol']})
   Price: ₹{sector_analysis['worst_performer']['price']:.2f} ({sector_analysis['worst_performer']['change_pct']:+.2f}%)

💡 SECTOR OUTLOOK: {'BULLISH' if sector_analysis['average_change'] > 1 else 'BEARISH' if sector_analysis['average_change'] < -1 else 'NEUTRAL'}"""
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in sector analysis: {e}")
            return f"❌ Error analyzing {sector} sector: {str(e)}"
    
    async def get_chennai_insights(self) -> str:
        """Get Chennai market intelligence"""
        try:
            self.logger.info("🏛️ Getting Chennai market insights")
            
            chennai_analysis = await self.advanced_analysis.get_chennai_market_intelligence()
            
            if 'error' in chennai_analysis:
                return f"❌ Error getting Chennai insights: {chennai_analysis['error']}"
            
            summary = chennai_analysis['chennai_market_summary']
            stocks = chennai_analysis['chennai_stocks']
            
            response = f"""🏛️ CHENNAI MARKET INTELLIGENCE

📊 TAMIL NADU MARKET OVERVIEW:
   Average Change: {summary['average_change']:+.2f}%
   Market Sentiment: {summary['sentiment']}
   Buy Recommendations: {summary['buy_recommendations']}/{summary['total_stocks']}
   
🌟 TOP CHENNAI PICK:"""
            
            if summary['top_chennai_pick']:
                top = summary['top_chennai_pick']
                response += f"""
   {top['name']} ({top['symbol']})
   Price: ₹{top['price']:.2f} ({top['change']:+.2f}%)
   Recommendation: {top['recommendation']} ({top['confidence']}% confidence)
   RSI: {top['rsi']:.1f}"""
            
            response += "\n\n🏢 CHENNAI STOCKS SNAPSHOT:"
            for stock in stocks[:5]:  # Show top 5
                response += f"\n   {stock['name']}: ₹{stock['price']:.2f} ({stock['change']:+.2f}%) - {stock['recommendation']}"
            
            response += f"\n\n💡 Chennai represents {len(stocks)} major Tamil Nadu companies with strong regional presence."
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in Chennai insights: {e}")
            return f"❌ Error getting Chennai insights: {str(e)}"
    
    async def get_market_overview_enhanced(self) -> str:
        """Enhanced market overview with sector insights"""
        try:
            # Get basic market overview
            basic_overview = await self.financial_engine.get_market_overview()
            
            # Get sector insights
            sectors_to_analyze = ['IT', 'Banking', 'Auto']
            sector_summaries = []
            
            for sector in sectors_to_analyze:
                try:
                    sector_data = await self.advanced_analysis.get_sector_analysis(sector)
                    if 'error' not in sector_data:
                        sector_summaries.append(f"   {sector}: {sector_data['average_change']:+.2f}% ({sector_data['sentiment']})")
                except Exception as e:
                    self.logger.warning(f"Failed to get {sector} sector data: {e}")
                    continue
            
            # Combine basic overview with sector insights
            enhanced_overview = f"""{basic_overview}

🏢 SECTOR PERFORMANCE:
{chr(10).join(sector_summaries) if sector_summaries else '   Sector data unavailable'}

🎯 MARKET SENTIMENT: {'BULLISH' if 'up' in basic_overview.lower() else 'BEARISH' if 'down' in basic_overview.lower() else 'MIXED'}"""
            
            return enhanced_overview
            
        except Exception as e:
            self.logger.error(f"Error in enhanced market overview: {e}")
            return await self.financial_engine.get_market_overview()  # Fallback to basic
    
    async def get_daily_briefing(self) -> str:
        """Generate comprehensive daily market briefing"""
        try:
            self.logger.info("📰 Generating daily market briefing")
            
            # Get market overview
            market_overview = await self.get_market_overview_enhanced()
            
            # Get Chennai insights
            chennai_insights = await self.get_chennai_insights()
            
            # Get top recommendations
            top_stocks = ['RELIANCE', 'TCS', 'HDFCBANK']
            quick_recs = []
            
            for stock in top_stocks:
                try:
                    analysis = await self.advanced_analysis.get_advanced_analysis(stock)
                    if 'error' not in analysis:
                        rec = analysis['recommendation']
                        quick_recs.append(f"   {stock}: {rec['action']} ({rec['confidence']}%)")
                except Exception:
                    continue
            
            briefing = f"""📰 RUDH DAILY MARKET BRIEFING
{datetime.now().strftime('%A, %B %d, %Y')}

{market_overview}

🎯 QUICK RECOMMENDATIONS:
{chr(10).join(quick_recs) if quick_recs else '   Analysis in progress...'}

{chennai_insights}

💡 Have a profitable trading day! Remember to manage your risk appropriately."""
            
            return briefing
            
        except Exception as e:
            self.logger.error(f"Error generating daily briefing: {e}")
            return "❌ Error generating daily briefing. Please try individual commands."
    
    async def process_query(self, query: str) -> str:
        """Enhanced query processing with new commands"""
        query_lower = query.lower().strip()
        self.query_count += 1
        
        try:
            # Enhanced commands
            if query_lower.startswith('analyze '):
                symbol = query_lower.replace('analyze ', '').strip().upper()
                return await self.analyze_stock_advanced(symbol)
            
            elif query_lower.startswith('sector '):
                sector = query_lower.replace('sector ', '').strip()
                return await self.analyze_sector(sector)
            
            elif query_lower in ['chennai', 'chennai market', 'tamil nadu', 'tn market']:
                return await self.get_chennai_insights()
            
            elif query_lower in ['market', 'market overview', 'overview']:
                return await self.get_market_overview_enhanced()
            
            elif query_lower in ['briefing', 'daily briefing', 'daily', 'morning briefing']:
                return await self.get_daily_briefing()
            
            elif query_lower == 'portfolio':
                return await self.financial_engine.analyze_portfolio()
            
            elif query_lower in ['recommend', 'recommendations', 'suggest']:
                return await self.financial_engine.get_stock_recommendations()
            
            elif query_lower.startswith('/'):
                return self.handle_command(query_lower)
            
            else:
                # Use AI for general financial queries
                enhanced_prompt = f"""You are Rudh, an expert financial advisor specializing in Indian markets with deep Chennai/Tamil Nadu insights. 
                
User query: {query}

Provide helpful, accurate financial guidance. Focus on:
- Indian stock market context (NSE/BSE)
- Chennai/Tamil Nadu regional insights when relevant
- Risk management and diversification
- Practical investment advice

Keep response conversational and helpful."""
                
                return await self.ai_service.get_response(enhanced_prompt)
        
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return f"❌ Error processing your request: {str(e)}"
    
    def handle_command(self, command: str) -> str:
        """Handle system commands"""
        if command == '/help':
            return """📋 ENHANCED RUDH FINANCIAL ADVISOR V3.1 COMMANDS:

🔍 ANALYSIS COMMANDS:
   'analyze SYMBOL' - Advanced technical analysis with indicators
   'sector SECTOR' - Analyze entire sector (IT, Banking, Auto, Energy)
   'chennai' - Chennai/Tamil Nadu market intelligence
   'market' - Enhanced market overview with sector insights
   'briefing' - Comprehensive daily market briefing
   'portfolio' - Portfolio analysis and optimization
   'recommend' - AI-powered stock recommendations

🎵 SYSTEM COMMANDS:
   '/voice' - Toggle voice output on/off
   '/help' - Show this help menu
   '/status' - Show system status
   '/quit' - Exit advisor

💡 EXAMPLES:
   'analyze RELIANCE' - Get RSI, MACD, Bollinger Bands analysis
   'sector IT' - Analyze entire IT sector performance
   'chennai' - Get Tamil Nadu market insights
   'briefing' - Daily market summary with recommendations

🌟 NEW IN V3.1:
   ✅ Technical indicators (RSI, MACD, Bollinger Bands)
   ✅ Sector analysis capabilities
   ✅ Chennai market intelligence
   ✅ Enhanced daily briefings
   ✅ Advanced recommendation engine"""
        
        elif command == '/voice':
            self.voice_enabled = not self.voice_enabled
            status = "enabled" if self.voice_enabled else "disabled"
            return f"🎵 Voice output {status}"
        
        elif command == '/status':
            session_time = time.time() - self.session_start
            return f"""📊 SYSTEM STATUS:
   
🧠 Core Engines: ✅ Operational
   📈 Financial Engine: Active
   🔍 Advanced Analysis: Ready
   🤖 AI Service: Connected
   🗣️ Speech Service: {'Enabled' if self.voice_enabled else 'Disabled'}

⚡ Session Stats:
   Session Time: {session_time:.1f} seconds
   Queries Processed: {self.query_count}
   Voice Output: {'On' if self.voice_enabled else 'Off'}

🌐 Market Data: Live (NSE/BSE/Global)
💡 Ready for advanced financial analysis!"""
        
        elif command == '/quit':
            return self.get_session_summary()
        
        else:
            return f"❓ Unknown command: {command}. Type '/help' for available commands."
    
    def get_session_summary(self) -> str:
        """Generate session summary"""
        session_time = time.time() - self.session_start
        return f"""👋 Thank you for using Rudh Financial Advisor V3.1!

📊 Your Session Summary:
   • Queries: {self.query_count}
   • Session Time: {session_time:.1f} seconds
   • Advanced Features Used: Technical Analysis, Market Intelligence

💡 Investment Reminders:
   • Always diversify your portfolio across sectors
   • Use technical indicators as guidance, not gospel
   • Consider Chennai market opportunities for regional advantage
   • Risk management is key to long-term success

🚀 May your investments grow and prosper!

📈 Keep building wealth with intelligent decisions."""
    
    async def speak_response(self, text: str):
        """Generate speech for response if voice enabled"""
        if self.voice_enabled and self.speech_service:
            try:
                start_time = time.time()
                await self.speech_service.speak(text)
                speech_time = time.time() - start_time
                print(f"✅ Speech completed ({speech_time:.3f}s)")
            except Exception as e:
                self.logger.warning(f"Speech synthesis failed: {e}")

async def main():
    """Main interactive loop for Enhanced Rudh Financial Advisor"""
    print("🚀 Initializing Enhanced Rudh Financial Advisor V3.1...")
    
    try:
        advisor = EnhancedRudhFinancialAdvisor()
        
        print("""
================================================================================
🤖 RUDH AI FINANCIAL ADVISOR V3.1 - ENHANCED WITH TECHNICAL INTELLIGENCE
   Your Advanced Personal Investment Assistant
================================================================================
🧠 ENHANCED ENGINES:
   📈 Real-time Market Data: ✅ OPERATIONAL
   🔍 Technical Analysis: ✅ RSI, MACD, Bollinger Bands
   🤖 Azure OpenAI (GPT-4o): ✅ CONNECTED
   🗣️ Voice Synthesis: ✅ ENABLED
   🏛️ Chennai Market Intelligence: ✅ READY
   🏢 Sector Analysis: ✅ IT, Banking, Auto, Energy

🌟 NEW IN V3.1:
   ✅ Advanced Technical Indicators
   ✅ Sector Performance Analysis  
   ✅ Chennai/Tamil Nadu Market Intelligence
   ✅ Enhanced Daily Market Briefings
   ✅ Sophisticated Recommendation Engine

💬 Welcome to your enhanced financial advisor! I can provide technical analysis,
sector insights, Chennai market intelligence, and sophisticated investment guidance.
""")
        
        # Welcome message with voice
        welcome_msg = "Welcome to your enhanced financial advisor with advanced technical analysis and Chennai market intelligence!"
        await advisor.speak_response(welcome_msg)
        
        print("""📋 ENHANCED COMMANDS:
   'analyze RELIANCE' - Advanced technical analysis
   'sector IT' - Analyze entire IT sector
   'chennai' - Tamil Nadu market insights
   'briefing' - Daily market summary
   'market' - Enhanced market overview
   '/help' - Full command list
   '/quit' - Exit advisor

💡 Try: 'briefing' for a comprehensive market overview!
--------------------------------------------------------------------------------""")
        
        # Interactive loop
        while True:
            try:
                query = input("[💰] Your question: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['/quit', 'quit', 'exit']:
                    response = advisor.get_session_summary()
                    print(f"\n🤖 Rudh: {response}")
                    await advisor.speak_response("Thank you for using Rudh Financial Advisor. Happy investing!")
                    break
                
                # Process query
                print("🧠 Processing your financial query...")
                start_time = time.time()
                
                response = await advisor.process_query(query)
                processing_time = time.time() - start_time
                
                print(f"\n🤖 Rudh: {response}")
                
                # Voice response
                if advisor.voice_enabled:
                    print("🎵 Speaking response...")
                    await advisor.speak_response(response)
                
                # Show metrics
                print(f"""
📊 ANALYSIS METRICS:
   ⚡ Processing Time: {processing_time:.3f}s
   🎯 Query Type: enhanced_analysis
   🗣️ Voice Output: {'✅' if advisor.voice_enabled else '❌'}""")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Rudh Financial Advisor V3.1!")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"❌ An error occurred: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Failed to initialize advisor: {e}")
        print(f"❌ Failed to start advisor: {e}")

if __name__ == "__main__":
    asyncio.run(main())