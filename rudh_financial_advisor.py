# rudh_financial_advisor.py - COMPLETE FIXED VERSION
"""
Rudh AI Financial Advisor - Phase 3 - FIXED VERSION
Voice-enabled personal financial advisor with real-time market data
Combines emotional intelligence with financial expertise
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys

# Import existing Rudh modules
sys.path.append('src')
from config.config import RudhConfig

# Import our new financial engine
from financial_intelligence_engine import FinancialIntelligenceEngine, StockData, InvestmentRecommendation

# Import existing voice capabilities
try:
    from azure_speech_service import AzureSpeechService
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    AzureSpeechService = None

# Import existing Azure OpenAI
try:
    from azure_openai_service import AzureOpenAIService
    AZURE_AI_AVAILABLE = True
except ImportError:
    AZURE_AI_AVAILABLE = False
    AzureOpenAIService = None

class RudhFinancialAdvisor:
    """Voice-enabled financial advisor combining AI and real-time market data"""
    
    def __init__(self):
        self.config = RudhConfig.get_config()
        self.logger = logging.getLogger("RudhFinancialAdvisor")
        
        # Initialize core services
        self.financial_engine = FinancialIntelligenceEngine()
        
        # Initialize AI services if available
        if AZURE_AI_AVAILABLE:
            self.ai_service = AzureOpenAIService()
            self.ai_available = True
        else:
            self.ai_service = None
            self.ai_available = False
        
        # Initialize voice services if available
        if VOICE_AVAILABLE:
            self.voice_service = AzureSpeechService()
            self.voice_available = self.voice_service.is_available
        else:
            self.voice_service = None
            self.voice_available = False
        
        # Session tracking
        self.session_stats = {
            "queries": 0,
            "recommendations_given": 0,
            "total_response_time": 0,
            "voice_interactions": 0,
            "start_time": datetime.now()
        }
        
        # User profile (would be loaded from database in production)
        self.user_profile = {
            "name": "User",
            "risk_tolerance": "MEDIUM",  # LOW, MEDIUM, HIGH
            "investment_experience": "INTERMEDIATE",  # BEGINNER, INTERMEDIATE, ADVANCED
            "investment_goals": ["LONG_TERM_GROWTH", "INCOME"],
            "preferred_sectors": ["TECHNOLOGY", "BANKING"],
            "location": "Chennai",
            "currency_preference": "INR",
            "voice_enabled": True
        }
        
        self.logger.info("✅ Rudh Financial Advisor initialized")
    
    async def start_advisor_session(self):
        """Start interactive financial advisor session"""
        print("=" * 80)
        print("🤖 RUDH AI FINANCIAL ADVISOR - VOICE ENHANCED")
        print("   Your Personal Investment Assistant for Chennai & Global Markets")
        print("=" * 80)
        
        # Check service availability
        print("🧠 CORE FINANCIAL ENGINES:")
        print(f"   📈 Real-time Market Data: ✅ OPERATIONAL")
        print(f"   🤖 Azure OpenAI (GPT-4o): {'✅ CONNECTED' if self.ai_available else '🔧 FALLBACK'}")
        print(f"   🗣️ Voice Synthesis: {'✅ ENABLED' if self.voice_available else '🔧 TEXT ONLY'}")
        print(f"   💰 Investment Analysis: ✅ READY")
        print(f"   🌐 Market Coverage: ✅ NSE/BSE + Global")
        
        # Welcome message
        welcome_msg = (
            f"🌟 Welcome to your personal financial advisor! "
            f"I can help you with stock analysis, portfolio optimization, "
            f"market insights, and investment recommendations tailored for Chennai markets. "
            f"I understand both Indian and global markets."
        )
        
        if self.voice_available:
            await self.voice_service.speak_text(welcome_msg, "excited")
        
        print(f"\n💬 {welcome_msg}")
        
        print(f"\n📋 FINANCIAL COMMANDS:")
        print(f"   'analyze SYMBOL' - Get detailed stock analysis")
        print(f"   'market overview' - Current market snapshot")
        print(f"   'portfolio review' - Analyze your holdings")
        print(f"   'recommend stocks' - Get AI investment suggestions")
        print(f"   'news SYMBOL' - Latest financial news")
        print(f"   '/voice' - Toggle voice output")
        print(f"   '/profile' - View/update investor profile")
        print(f"   '/help' - Show all commands")
        print(f"   '/quit' - Exit advisor")
        
        print(f"\n💡 Try: 'analyze RELIANCE' or 'market overview'")
        print("-" * 80)
        
        # Main interaction loop
        while True:
            try:
                user_input = input(f"\n[{self.session_stats['queries'] + 1}] 💰 Your question: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == '/quit':
                    await self._handle_quit()
                    break
                elif user_input.lower() == '/help':
                    await self._show_help()
                elif user_input.lower() == '/voice':
                    await self._toggle_voice()
                elif user_input.lower() == '/profile':
                    await self._show_profile()
                elif user_input.lower() == '/stats':
                    await self._show_stats()
                else:
                    # Process financial query
                    await self._process_financial_query(user_input)
                
                self.session_stats["queries"] += 1
                
            except KeyboardInterrupt:
                await self._handle_quit()
                break
            except Exception as e:
                self.logger.error(f"Session error: {e}")
                print(f"❌ I encountered an issue: {e}")
    
    async def _process_financial_query(self, query: str):
        """Process financial queries with AI and market data"""
        start_time = datetime.now()
        
        try:
            print(f"🧠 Analyzing your financial query...")
            
            # Determine query type and extract parameters
            query_type, params = self._parse_financial_query(query)
            
            response = ""
            voice_text = ""
            
            if query_type == "stock_analysis":
                symbol = params.get("symbol", "").upper()
                if symbol:
                    response, voice_text = await self._handle_stock_analysis(symbol)
                else:
                    response = "Please specify a stock symbol (e.g., 'analyze RELIANCE')"
                    voice_text = response
            
            elif query_type == "market_overview":
                response, voice_text = await self._handle_market_overview()
            
            elif query_type == "portfolio_review":
                response, voice_text = await self._handle_portfolio_review()
            
            elif query_type == "stock_recommendation":
                response, voice_text = await self._handle_stock_recommendations()
            
            elif query_type == "general_financial":
                response, voice_text = await self._handle_general_financial_query(query)
            
            else:
                # Fallback to AI-powered response
                response, voice_text = await self._handle_ai_financial_response(query)
            
            # Display response
            print(f"🤖 Rudh: {response}")
            
            # Voice output if enabled
            if self.voice_available and self.user_profile.get("voice_enabled", True):
                print(f"🎵 Speaking response...")
                await self.voice_service.speak_text(voice_text, "neutral")
            
            # Performance tracking
            processing_time = (datetime.now() - start_time).total_seconds()
            self.session_stats["total_response_time"] += processing_time
            
            print(f"\n📊 ANALYSIS METRICS:")
            print(f"   ⚡ Processing Time: {processing_time:.3f}s")
            print(f"   🎯 Query Type: {query_type}")
            print(f"   🗣️ Voice Output: {'✅' if self.voice_available else '📝 Text Only'}")
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            error_msg = f"I apologize, but I encountered an issue processing your request: {str(e)}"
            print(f"❌ {error_msg}")
            
            if self.voice_available:
                await self.voice_service.speak_text("I apologize, but I encountered a technical issue.", "neutral")
    
def _parse_financial_query(self, query: str) -> tuple:
    """Parse financial query to determine type and extract parameters"""
    query_lower = query.lower()
    
    # Recommendation patterns - CHECK THIS FIRST!
    if any(phrase in query_lower for phrase in ["recommend stocks", "suggest stocks", "stock recommendations", "recommendations"]):
        return "stock_recommendation", {}
    
    # Stock analysis patterns
    elif any(word in query_lower for word in ["analyze", "analysis", "stock", "price"]) and not any(word in query_lower for word in ["recommend", "suggest"]):
        # Extract symbol
        words = query.split()
        symbol = None
        for word in words:
            if word.upper() in ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "AAPL", "MSFT", "GOOGL"]:
                symbol = word.upper()
                break
            elif len(word) <= 6 and word.isalpha() and word.upper() not in ["ANALYZE", "STOCK", "PRICE"]:
                symbol = word.upper()
        
        return "stock_analysis", {"symbol": symbol}
    
    # Market overview patterns
    elif any(word in query_lower for word in ["market", "overview", "indices", "nifty", "sensex"]):
        return "market_overview", {}
    
    # Portfolio patterns
    elif any(word in query_lower for word in ["portfolio", "holdings", "my stocks"]):
        return "portfolio_review", {}
    
    # General financial patterns
    elif any(word in query_lower for word in ["financial", "investment", "money", "wealth"]):
        return "general_financial", {"query": query}
    
    else:
        return "general_query", {"query": query}
    
    async def _handle_stock_analysis(self, symbol: str) -> tuple:
        """Handle stock analysis requests"""
        try:
            # Get stock data
            stock_data = await self.financial_engine.get_stock_data(symbol)
            if not stock_data:
                return f"❌ Could not find data for {symbol}. Please check the symbol.", f"Could not find data for {symbol}"
            
            # Get investment recommendation
            recommendation = await self.financial_engine.analyze_stock(symbol, self.user_profile)
            
            # Format detailed response
            response = f"📊 ANALYSIS FOR {stock_data.name} ({symbol})\n\n"
            response += f"💰 Current Price: ₹{stock_data.current_price:,.2f} "
            response += f"({stock_data.change_percent:+.2f}% today)\n"
            response += f"📈 Day Range: ₹{stock_data.day_range[0]:,.2f} - ₹{stock_data.day_range[1]:,.2f}\n"
            response += f"📅 52-Week Range: ₹{stock_data.week_52_range[0]:,.2f} - ₹{stock_data.week_52_range[1]:,.2f}\n"
            
            if stock_data.pe_ratio:
                response += f"📊 P/E Ratio: {stock_data.pe_ratio:.2f}\n"
            
            response += f"📊 Volume: {stock_data.volume:,}\n\n"
            
            # Investment recommendation
            action_emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(recommendation.action, "⚪")
            response += f"🎯 INVESTMENT RECOMMENDATION\n"
            response += f"{action_emoji} Action: {recommendation.action} (Confidence: {recommendation.confidence:.0%})\n"
            response += f"🎯 Target Price: ₹{recommendation.target_price:,.2f}\n"
            response += f"🛡️ Stop Loss: ₹{recommendation.stop_loss:,.2f}\n"
            response += f"⚠️ Risk Level: {recommendation.risk_level}\n"
            response += f"💼 Suggested Allocation: {recommendation.allocation_percent:.1f}%\n\n"
            response += f"💡 REASONING:\n{recommendation.reasoning}"
            
            # Voice summary
            voice_text = f"Analysis for {stock_data.name}. Currently trading at {stock_data.current_price:.0f} rupees, "
            voice_text += f"{abs(stock_data.change_percent):.1f} percent {'up' if stock_data.change_percent >= 0 else 'down'} today. "
            voice_text += f"My recommendation is {recommendation.action.lower()} with {recommendation.confidence:.0f} percent confidence. "
            voice_text += f"Target price is {recommendation.target_price:.0f} rupees."
            
            self.session_stats["recommendations_given"] += 1
            
            return response, voice_text
            
        except Exception as e:
            error_msg = f"Analysis failed for {symbol}: {str(e)}"
            return f"❌ {error_msg}", error_msg
    
    async def _handle_market_overview(self) -> tuple:
        """Handle market overview requests"""
        try:
            overview = await self.financial_engine.get_market_overview()
            
            response = "🌐 MARKET OVERVIEW\n\n"
            
            # Indices
            if "indices" in overview:
                response += "📊 MAJOR INDICES:\n"
                for index, data in overview["indices"].items():
                    direction = "🟢" if data["change_percent"] >= 0 else "🔴"
                    response += f"{direction} {index}: {data['current']:.2f} ({data['change_percent']:+.2f}%)\n"
                response += "\n"
            
            # Top Indian stocks
            if "top_indian_stocks" in overview:
                response += "🇮🇳 TOP INDIAN STOCKS:\n"
                for stock, data in overview["top_indian_stocks"].items():
                    direction = "🟢" if data["change_percent"] >= 0 else "🔴"
                    response += f"{direction} {stock}: ₹{data['current']:.2f} ({data['change_percent']:+.2f}%)\n"
                response += "\n"
            
            # Market sentiment
            sentiment = overview.get("market_sentiment", "NEUTRAL")
            sentiment_emoji = {"BULLISH": "🚀", "BEARISH": "📉", "NEUTRAL": "⚖️"}.get(sentiment, "⚖️")
            response += f"{sentiment_emoji} Market Sentiment: {sentiment}\n"
            response += f"🕒 Updated: {datetime.now().strftime('%H:%M IST')}"
            
            # Voice summary
            nifty_change = ""
            if "indices" in overview and "NIFTY50" in overview["indices"]:
                nifty_data = overview["indices"]["NIFTY50"]
                nifty_change = f"Nifty is {'up' if nifty_data['change_percent'] >= 0 else 'down'} {abs(nifty_data['change_percent']):.1f} percent. "
            
            voice_text = f"Market overview: {nifty_change}Overall sentiment is {sentiment.lower()}. "
            voice_text += f"Indian markets are showing mixed performance today."
            
            return response, voice_text
            
        except Exception as e:
            error_msg = f"Market overview failed: {str(e)}"
            return f"❌ {error_msg}", error_msg
    
    async def _handle_portfolio_review(self) -> tuple:
        """Handle portfolio review (demo with sample portfolio)"""
        # Sample portfolio for demonstration
        sample_portfolio = [
            {'symbol': 'RELIANCE', 'quantity': 10, 'avg_price': 2500},
            {'symbol': 'TCS', 'quantity': 5, 'avg_price': 3800},
            {'symbol': 'INFY', 'quantity': 15, 'avg_price': 1600},
            {'symbol': 'HDFCBANK', 'quantity': 8, 'avg_price': 1700}
        ]
        
        try:
            analysis = await self.financial_engine.analyze_portfolio(sample_portfolio)
            
            response = "💼 PORTFOLIO ANALYSIS (DEMO)\n\n"
            response += f"💰 Total Value: ₹{analysis.total_value:,.2f}\n"
            response += f"📈 Total Return: ₹{analysis.total_return:,.2f} ({analysis.return_percent:+.2f}%)\n"
            response += f"⚠️ Risk Score: {analysis.risk_score:.1f}/100\n"
            response += f"🎯 Diversification: {analysis.diversification_score:.1f}/100\n\n"
            
            if analysis.top_performers:
                response += f"🏆 Top Performers: {', '.join(analysis.top_performers[:3])}\n"
            
            if analysis.underperformers:
                response += f"📉 Underperformers: {', '.join(analysis.underperformers[:3])}\n"
            
            response += f"\n💡 This is a demo portfolio. Connect your actual holdings for real analysis!"
            
            # Voice summary
            return_status = "positive" if analysis.return_percent >= 0 else "negative"
            voice_text = f"Portfolio analysis complete. Your portfolio value is {analysis.total_value:.0f} rupees "
            voice_text += f"with a {return_status} return of {abs(analysis.return_percent):.1f} percent. "
            voice_text += f"Risk score is {analysis.risk_score:.0f} out of 100."
            
            return response, voice_text
            
        except Exception as e:
            error_msg = f"Portfolio analysis failed: {str(e)}"
            return f"❌ {error_msg}", error_msg
    
    async def _handle_stock_recommendations(self) -> tuple:
        """Handle stock recommendation requests - FIXED VERSION"""
        # Recommend based on current market conditions and user profile
        recommended_stocks = ["RELIANCE", "TCS", "HDFCBANK"]
        
        response = "🎯 STOCK RECOMMENDATIONS FOR YOU\n\n"
        response += "Based on your risk profile and market conditions:\n\n"
        
        voice_parts = []
        
        for symbol in recommended_stocks:
            try:
                rec = await self.financial_engine.analyze_stock(symbol, self.user_profile)
                action_emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(rec.action, "⚪")
                
                response += f"{action_emoji} {symbol}: {rec.action} (Confidence: {rec.confidence:.0%})\n"
                response += f"   Target: ₹{rec.target_price:,.2f} | Risk: {rec.risk_level}\n"
                response += f"   Allocation: {rec.allocation_percent:.1f}%\n\n"
                
                if rec.action == "BUY":
                    voice_parts.append(f"{symbol} is a buy with {rec.confidence:.0f} percent confidence")
                
            except Exception as e:
                response += f"❌ Could not analyze {symbol}: {str(e)}\n\n"
        
        response += "💡 Always do your own research before investing!"
        
        voice_text = "Here are my stock recommendations: " + ". ".join(voice_parts[:2]) + ". Remember to do your own research."
        
        return response, voice_text
    
    async def _handle_general_financial_query(self, query: str) -> tuple:
        """Handle general financial questions"""
        # Use AI if available, otherwise provide generic response
        if self.ai_available:
            return await self._handle_ai_financial_response(query)
        else:
            response = "I can help with stock analysis, market overviews, and portfolio reviews. Try 'analyze RELIANCE' or 'market overview'."
            return response, response
    
    async def _handle_ai_financial_response(self, query: str) -> tuple:
        """Handle AI-powered financial responses - FIXED VERSION"""
        if not self.ai_available:
            response = "AI service unavailable. Try specific commands like 'analyze SYMBOL' or 'market overview'."
            return response, response
        
        try:
            # Enhanced prompt for financial context
            enhanced_prompt = f"""You are Rudh, an expert financial advisor specializing in Indian and global markets. 
            User profile: Risk tolerance: {self.user_profile['risk_tolerance']}, Experience: {self.user_profile['investment_experience']}, Location: Chennai
            
            User question: {query}
            
            Provide a helpful, accurate financial response. Keep it concise but informative. 
            Include specific actionable advice when appropriate."""
            
            # Use the correct method name for Azure OpenAI service
            ai_response = await self.ai_service.get_response(enhanced_prompt)
            
            # Extract text for voice (remove complex formatting)
            voice_text = ai_response.replace("*", "").replace("#", "").replace("\n", " ")
            
            return ai_response, voice_text
            
        except Exception as e:
            error_msg = f"AI response failed: {str(e)}"
            return f"❌ {error_msg}", error_msg
    
    async def _toggle_voice(self):
        """Toggle voice output"""
        if not self.voice_available:
            print("🔧 Voice synthesis not available")
            return
        
        current_state = self.user_profile.get("voice_enabled", True)
        self.user_profile["voice_enabled"] = not current_state
        
        new_state = "enabled" if self.user_profile["voice_enabled"] else "disabled"
        print(f"🎵 Voice output {new_state}")
        
        if self.user_profile["voice_enabled"]:
            await self.voice_service.speak_text("Voice output is now enabled", "neutral")
    
    async def _show_profile(self):
        """Show user investment profile"""
        print(f"\n👤 INVESTOR PROFILE:")
        print(f"   Name: {self.user_profile['name']}")
        print(f"   Risk Tolerance: {self.user_profile['risk_tolerance']}")
        print(f"   Experience: {self.user_profile['investment_experience']}")
        print(f"   Goals: {', '.join(self.user_profile['investment_goals'])}")
        print(f"   Preferred Sectors: {', '.join(self.user_profile['preferred_sectors'])}")
        print(f"   Location: {self.user_profile['location']}")
        print(f"   Voice Enabled: {self.user_profile.get('voice_enabled', True)}")
    
    async def _show_stats(self):
        """Show session statistics"""
        session_time = (datetime.now() - self.session_stats["start_time"]).total_seconds()
        avg_response_time = (self.session_stats["total_response_time"] / max(self.session_stats["queries"], 1))
        
        print(f"\n📊 SESSION STATISTICS:")
        print(f"   Queries Processed: {self.session_stats['queries']}")
        print(f"   Recommendations Given: {self.session_stats['recommendations_given']}")
        print(f"   Session Duration: {session_time:.1f}s")
        print(f"   Average Response Time: {avg_response_time:.3f}s")
        print(f"   Voice Interactions: {self.session_stats['voice_interactions']}")
    
    async def _show_help(self):
        """Show detailed help"""
        help_text = """
🔍 FINANCIAL ANALYSIS COMMANDS:
   • analyze SYMBOL - Detailed stock analysis (e.g., 'analyze RELIANCE')
   • market overview - Current market snapshot with indices
   • portfolio review - Analyze your portfolio performance
   • recommend stocks - Get AI-powered stock suggestions
   
📊 SAMPLE INDIAN STOCKS TO TRY:
   • RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, ITC
   
🌍 GLOBAL STOCKS:
   • AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA
   
⚙️ SYSTEM COMMANDS:
   • /voice - Toggle voice output on/off
   • /profile - View/update your investor profile
   • /stats - View session statistics
   • /help - Show this help message
   • /quit - Exit the advisor
   
💡 NATURAL LANGUAGE:
   You can also ask questions like:
   • "Should I invest in tech stocks?"
   • "What's happening in the market today?"
   • "How risky is Reliance stock?"
        """
        print(help_text)
        
        if self.voice_available:
            voice_summary = "I can help with stock analysis, market overviews, portfolio reviews, and investment recommendations. Try asking about any Indian or global stock."
            await self.voice_service.speak_text(voice_summary, "helpful")
    
    async def _handle_quit(self):
        """Handle graceful exit - FIXED VERSION"""
        session_time = (datetime.now() - self.session_stats["start_time"]).total_seconds()
        
        farewell = f"""
👋 Thank you for using Rudh Financial Advisor!

📊 Your Session Summary:
   • Queries: {self.session_stats['queries']}
   • Recommendations: {self.session_stats['recommendations_given']}
   • Session Time: {session_time:.1f} seconds
   
💡 Your financial insights have been valuable. Remember:
   • Always diversify your portfolio
   • Do your own research before investing
   • Consider your risk tolerance
   
🚀 May your investments grow and prosper!
        """
        
        print(farewell)
        
        if self.voice_available:
            voice_farewell = "Thank you for using Rudh Financial Advisor. May your investments grow and prosper!"
            await self.voice_service.speak_text(voice_farewell, "grateful")

# Main execution
async def main():
    """Main function to run Rudh Financial Advisor"""
    print("🚀 Initializing Rudh Financial Advisor...")
    
    try:
        advisor = RudhFinancialAdvisor()
        await advisor.start_advisor_session()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start advisor: {e}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(main())