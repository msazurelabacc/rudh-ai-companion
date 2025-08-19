# risk_analytics.py
"""
Rudh Risk Analytics & Portfolio Optimization Engine - Phase 3.2
Advanced risk management using modern portfolio theory
"""

import numpy as np
import pandas as pd
import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import sqlite3
from scipy import optimize
import warnings
warnings.filterwarnings('ignore')

@dataclass
class RiskMetrics:
    """Risk analysis results"""
    portfolio_id: str
    total_value: float
    daily_var_95: float  # Value at Risk (95% confidence)
    daily_var_99: float  # Value at Risk (99% confidence)
    portfolio_beta: float
    sharpe_ratio: float
    volatility: float  # Annual volatility
    max_drawdown: float
    correlation_risk: float
    concentration_risk: float
    risk_score: int  # 1-100 scale
    recommendation: str

@dataclass
class OptimizationResult:
    """Portfolio optimization results"""
    recommended_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    rebalancing_actions: List[Dict]
    potential_improvement: str

class RiskAnalyticsEngine:
    """Advanced portfolio risk analytics and optimization"""
    
    def __init__(self, db_path: str = "rudh_portfolio.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("RiskAnalytics")
        
        # Risk-free rate (Indian 10-year government bond ~7%)
        self.risk_free_rate = 0.07
        
        # Market benchmark (NIFTY 50)
        self.benchmark_symbol = "^NSEI"
    
    def calculate_portfolio_risk(self, portfolio_id: str, lookback_days: int = 252) -> RiskMetrics:
        """Calculate comprehensive risk metrics for portfolio"""
        try:
            # Get portfolio holdings
            holdings = self._get_portfolio_holdings(portfolio_id)
            if not holdings:
                raise ValueError("No holdings found in portfolio")
            
            # Get historical data
            symbols = list(holdings.keys())
            weights = np.array(list(holdings.values()))
            
            price_data = self._get_historical_data(symbols, lookback_days)
            returns_data = price_data.pct_change().dropna()
            
            # Get benchmark data
            benchmark_data = self._get_benchmark_data(lookback_days)
            benchmark_returns = benchmark_data.pct_change().dropna()
            
            # Portfolio returns
            portfolio_returns = (returns_data * weights).sum(axis=1)
            
            # Calculate risk metrics
            daily_var_95 = self._calculate_var(portfolio_returns, 0.05)
            daily_var_99 = self._calculate_var(portfolio_returns, 0.01)
            portfolio_beta = self._calculate_beta(portfolio_returns, benchmark_returns)
            sharpe_ratio = self._calculate_sharpe_ratio(portfolio_returns)
            volatility = portfolio_returns.std() * np.sqrt(252)  # Annualized
            max_drawdown = self._calculate_max_drawdown(portfolio_returns)
            
            # Advanced risk metrics
            correlation_risk = self._calculate_correlation_risk(returns_data)
            concentration_risk = self._calculate_concentration_risk(weights)
            
            # Overall risk score (1-100)
            risk_score = self._calculate_risk_score(
                volatility, max_drawdown, correlation_risk, concentration_risk
            )
            
            # Get total portfolio value
            total_value = self._get_portfolio_value(portfolio_id)
            
            # Convert VaR to absolute values
            daily_var_95_abs = abs(daily_var_95 * total_value)
            daily_var_99_abs = abs(daily_var_99 * total_value)
            
            # Risk recommendation
            recommendation = self._get_risk_recommendation(risk_score, concentration_risk)
            
            return RiskMetrics(
                portfolio_id=portfolio_id,
                total_value=total_value,
                daily_var_95=daily_var_95_abs,
                daily_var_99=daily_var_99_abs,
                portfolio_beta=portfolio_beta,
                sharpe_ratio=sharpe_ratio,
                volatility=volatility,
                max_drawdown=max_drawdown,
                correlation_risk=correlation_risk,
                concentration_risk=concentration_risk,
                risk_score=risk_score,
                recommendation=recommendation
            )
            
        except Exception as e:
            self.logger.error(f"❌ Risk calculation failed: {e}")
            raise
    
    def optimize_portfolio(self, portfolio_id: str, target_return: float = None) -> OptimizationResult:
        """Optimize portfolio using modern portfolio theory"""
        try:
            # Get portfolio holdings
            holdings = self._get_portfolio_holdings(portfolio_id)
            symbols = list(holdings.keys())
            current_weights = np.array(list(holdings.values()))
            
            # Get historical data for optimization
            price_data = self._get_historical_data(symbols, 252)
            returns_data = price_data.pct_change().dropna()
            
            # Calculate expected returns and covariance matrix
            expected_returns = returns_data.mean() * 252  # Annualized
            cov_matrix = returns_data.cov() * 252  # Annualized
            
            # Portfolio optimization
            if target_return is None:
                # Maximize Sharpe ratio
                optimal_weights = self._maximize_sharpe_ratio(expected_returns, cov_matrix)
            else:
                # Minimize risk for target return
                optimal_weights = self._minimize_risk_for_return(
                    expected_returns, cov_matrix, target_return
                )
            
            # Calculate optimized portfolio metrics
            opt_return = np.sum(optimal_weights * expected_returns)
            opt_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
            opt_sharpe = (opt_return - self.risk_free_rate) / opt_volatility
            
            # Create weight dictionary
            recommended_weights = dict(zip(symbols, optimal_weights))
            
            # Generate rebalancing actions
            rebalancing_actions = self._generate_rebalancing_actions(
                symbols, current_weights, optimal_weights, portfolio_id
            )
            
            # Potential improvement analysis
            current_return = np.sum(current_weights * expected_returns)
            current_volatility = np.sqrt(np.dot(current_weights.T, np.dot(cov_matrix, current_weights)))
            current_sharpe = (current_return - self.risk_free_rate) / current_volatility
            
            improvement = f"Sharpe ratio: {current_sharpe:.3f} → {opt_sharpe:.3f} " \
                         f"(+{((opt_sharpe - current_sharpe) / current_sharpe * 100):+.1f}%)"
            
            return OptimizationResult(
                recommended_weights=recommended_weights,
                expected_return=opt_return,
                expected_volatility=opt_volatility,
                sharpe_ratio=opt_sharpe,
                rebalancing_actions=rebalancing_actions,
                potential_improvement=improvement
            )
            
        except Exception as e:
            self.logger.error(f"❌ Portfolio optimization failed: {e}")
            raise
    
    def calculate_correlation_matrix(self, portfolio_id: str) -> pd.DataFrame:
        """Calculate correlation matrix for portfolio holdings"""
        try:
            holdings = self._get_portfolio_holdings(portfolio_id)
            symbols = list(holdings.keys())
            
            price_data = self._get_historical_data(symbols, 252)
            returns_data = price_data.pct_change().dropna()
            
            correlation_matrix = returns_data.corr()
            return correlation_matrix
            
        except Exception as e:
            self.logger.error(f"❌ Correlation calculation failed: {e}")
            return pd.DataFrame()
    
    def stress_test_portfolio(self, portfolio_id: str) -> Dict[str, float]:
        """Perform stress testing on portfolio"""
        try:
            holdings = self._get_portfolio_holdings(portfolio_id)
            symbols = list(holdings.keys())
            weights = np.array(list(holdings.values()))
            
            price_data = self._get_historical_data(symbols, 252)
            returns_data = price_data.pct_change().dropna()
            
            portfolio_returns = (returns_data * weights).sum(axis=1)
            total_value = self._get_portfolio_value(portfolio_id)
            
            # Stress test scenarios
            scenarios = {
                "Market Crash (-20%)": -0.20,
                "Black Monday (-22.6%)": -0.226,
                "COVID-19 Crash (-34%)": -0.34,
                "2008 Financial Crisis (-37%)": -0.37,
                "Worst Historical Day": portfolio_returns.min()
            }
            
            stress_results = {}
            for scenario, shock in scenarios.items():
                portfolio_loss = total_value * abs(shock)
                stress_results[scenario] = portfolio_loss
            
            return stress_results
            
        except Exception as e:
            self.logger.error(f"❌ Stress testing failed: {e}")
            return {}
    
    def _get_portfolio_holdings(self, portfolio_id: str) -> Dict[str, float]:
        """Get portfolio holdings as weights"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query("""
                SELECT symbol, quantity, current_price 
                FROM holdings WHERE portfolio_id = ?
                """, conn, params=(portfolio_id,))
            
            if df.empty:
                return {}
            
            # Calculate position values
            df['position_value'] = df['quantity'] * df['current_price']
            total_value = df['position_value'].sum()
            
            # Calculate weights
            holdings = {}
            for _, row in df.iterrows():
                weight = row['position_value'] / total_value
                holdings[row['symbol']] = weight
            
            return holdings
            
        except Exception as e:
            self.logger.error(f"❌ Get holdings failed: {e}")
            return {}
    
    def _get_historical_data(self, symbols: List[str], days: int) -> pd.DataFrame:
        """Get historical price data for symbols"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)  # Extra buffer
            
            data = {}
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(start=start_date, end=end_date)
                    if not hist.empty:
                        data[symbol] = hist['Close']
                except Exception as e:
                    self.logger.warning(f"Failed to get data for {symbol}: {e}")
                    continue
            
            if not data:
                raise ValueError("No historical data available")
            
            df = pd.DataFrame(data)
            return df.dropna().tail(days)
            
        except Exception as e:
            self.logger.error(f"❌ Historical data fetch failed: {e}")
            raise
    
    def _get_benchmark_data(self, days: int) -> pd.Series:
        """Get benchmark (NIFTY 50) data"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days + 30)
            
            ticker = yf.Ticker(self.benchmark_symbol)
            hist = ticker.history(start=start_date, end=end_date)
            
            return hist['Close'].dropna().tail(days)
            
        except Exception as e:
            self.logger.warning(f"Benchmark data failed: {e}")
            # Return dummy data if benchmark fails
            return pd.Series([100] * days)
    
    def _calculate_var(self, returns: pd.Series, confidence_level: float) -> float:
        """Calculate Value at Risk"""
        return np.percentile(returns, confidence_level * 100)
    
    def _calculate_beta(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """Calculate portfolio beta"""
        try:
            # Align the series
            aligned_data = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
            if len(aligned_data) < 30:
                return 1.0  # Default beta
            
            portfolio_aligned = aligned_data.iloc[:, 0]
            benchmark_aligned = aligned_data.iloc[:, 1]
            
            covariance = np.cov(portfolio_aligned, benchmark_aligned)[0, 1]
            benchmark_variance = np.var(benchmark_aligned)
            
            if benchmark_variance == 0:
                return 1.0
            
            beta = covariance / benchmark_variance
            return beta
            
        except Exception as e:
            self.logger.warning(f"Beta calculation failed: {e}")
            return 1.0
    
    def _calculate_sharpe_ratio(self, returns: pd.Series) -> float:
        """Calculate Sharpe ratio"""
        try:
            excess_returns = returns.mean() - (self.risk_free_rate / 252)  # Daily risk-free rate
            volatility = returns.std()
            
            if volatility == 0:
                return 0.0
            
            sharpe = (excess_returns / volatility) * np.sqrt(252)  # Annualized
            return sharpe
            
        except Exception as e:
            self.logger.warning(f"Sharpe ratio calculation failed: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown"""
        try:
            cumulative_returns = (1 + returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdowns = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdowns.min()
            return abs(max_drawdown)
            
        except Exception as e:
            self.logger.warning(f"Max drawdown calculation failed: {e}")
            return 0.0
    
    def _calculate_correlation_risk(self, returns_data: pd.DataFrame) -> float:
        """Calculate correlation risk (average correlation)"""
        try:
            corr_matrix = returns_data.corr()
            # Remove diagonal (self-correlations)
            mask = ~np.eye(corr_matrix.shape[0], dtype=bool)
            correlations = corr_matrix.values[mask]
            
            avg_correlation = np.mean(np.abs(correlations))
            return avg_correlation
            
        except Exception as e:
            self.logger.warning(f"Correlation risk calculation failed: {e}")
            return 0.5
    
    def _calculate_concentration_risk(self, weights: np.ndarray) -> float:
        """Calculate concentration risk using Herfindahl index"""
        try:
            # Herfindahl-Hirschman Index
            hhi = np.sum(weights ** 2)
            # Convert to 0-1 scale (1 = maximum concentration)
            return hhi
            
        except Exception as e:
            self.logger.warning(f"Concentration risk calculation failed: {e}")
            return 0.5
    
    def _calculate_risk_score(self, volatility: float, max_drawdown: float, 
                             correlation_risk: float, concentration_risk: float) -> int:
        """Calculate overall risk score (1-100)"""
        try:
            # Normalize metrics to 0-1 scale
            vol_score = min(volatility / 0.5, 1.0)  # 50% vol = max score
            dd_score = min(max_drawdown / 0.5, 1.0)  # 50% drawdown = max score
            corr_score = correlation_risk  # Already 0-1
            conc_score = concentration_risk  # Already 0-1
            
            # Weighted average (volatility and drawdown more important)
            risk_score = (vol_score * 0.3 + dd_score * 0.3 + 
                         corr_score * 0.2 + conc_score * 0.2)
            
            # Convert to 1-100 scale
            return int(risk_score * 100)
            
        except Exception as e:
            self.logger.warning(f"Risk score calculation failed: {e}")
            return 50
    
    def _get_risk_recommendation(self, risk_score: int, concentration_risk: float) -> str:
        """Generate risk recommendation"""
        if risk_score < 30:
            return "LOW RISK: Portfolio is well-diversified with conservative risk profile"
        elif risk_score < 60:
            return "MODERATE RISK: Balanced portfolio with acceptable risk levels"
        elif risk_score < 80:
            return "HIGH RISK: Consider diversification and risk reduction strategies"
        else:
            return "VERY HIGH RISK: Immediate action required to reduce portfolio risk"
    
    def _get_portfolio_value(self, portfolio_id: str) -> float:
        """Get total portfolio value"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT SUM(quantity * current_price) as total_holdings,
                       (SELECT cash_balance FROM portfolios WHERE portfolio_id = ?) as cash
                FROM holdings WHERE portfolio_id = ?
                """, (portfolio_id, portfolio_id))
                
                result = cursor.fetchone()
                holdings_value = result[0] if result[0] else 0.0
                cash_balance = result[1] if result[1] else 0.0
                
                return holdings_value + cash_balance
                
        except Exception as e:
            self.logger.error(f"❌ Portfolio value calculation failed: {e}")
            return 0.0
    
    def _maximize_sharpe_ratio(self, expected_returns: pd.Series, cov_matrix: pd.DataFrame) -> np.ndarray:
        """Optimize portfolio to maximize Sharpe ratio"""
        try:
            n_assets = len(expected_returns)
            
            def negative_sharpe(weights):
                portfolio_return = np.sum(weights * expected_returns)
                portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                if portfolio_volatility == 0:
                    return -np.inf
                sharpe = (portfolio_return - self.risk_free_rate) / portfolio_volatility
                return -sharpe  # Negative because we want to maximize
            
            # Constraints: weights sum to 1, all weights >= 0
            constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            bounds = tuple((0, 0.4) for _ in range(n_assets))  # Max 40% in any asset
            
            # Initial guess: equal weights
            initial_guess = np.array([1/n_assets] * n_assets)
            
            result = optimize.minimize(
                negative_sharpe, 
                initial_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                return result.x
            else:
                self.logger.warning("Optimization failed, using equal weights")
                return initial_guess
                
        except Exception as e:
            self.logger.error(f"❌ Sharpe maximization failed: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    def _minimize_risk_for_return(self, expected_returns: pd.Series, 
                                 cov_matrix: pd.DataFrame, target_return: float) -> np.ndarray:
        """Minimize risk for target return"""
        try:
            n_assets = len(expected_returns)
            
            def portfolio_volatility(weights):
                return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            # Constraints
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights sum to 1
                {'type': 'eq', 'fun': lambda x: np.sum(x * expected_returns) - target_return}  # Target return
            ]
            bounds = tuple((0, 0.4) for _ in range(n_assets))
            
            initial_guess = np.array([1/n_assets] * n_assets)
            
            result = optimize.minimize(
                portfolio_volatility,
                initial_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                return result.x
            else:
                self.logger.warning("Risk minimization failed, using equal weights")
                return initial_guess
                
        except Exception as e:
            self.logger.error(f"❌ Risk minimization failed: {e}")
            return np.array([1/len(expected_returns)] * len(expected_returns))
    
    def _generate_rebalancing_actions(self, symbols: List[str], current_weights: np.ndarray,
                                     optimal_weights: np.ndarray, portfolio_id: str) -> List[Dict]:
        """Generate specific rebalancing actions"""
        try:
            total_value = self._get_portfolio_value(portfolio_id)
            actions = []
            
            for i, symbol in enumerate(symbols):
                current_weight = current_weights[i]
                optimal_weight = optimal_weights[i]
                weight_diff = optimal_weight - current_weight
                
                if abs(weight_diff) > 0.05:  # Only significant changes (>5%)
                    value_change = weight_diff * total_value
                    
                    if weight_diff > 0:
                        action = "BUY"
                        amount = abs(value_change)
                    else:
                        action = "SELL"
                        amount = abs(value_change)
                    
                    actions.append({
                        'symbol': symbol,
                        'action': action,
                        'amount': amount,
                        'current_weight': current_weight * 100,
                        'target_weight': optimal_weight * 100,
                        'weight_change': weight_diff * 100
                    })
            
            return actions
            
        except Exception as e:
            self.logger.error(f"❌ Rebalancing actions generation failed: {e}")
            return []

# Test the risk analytics engine
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testing Risk Analytics Engine...")
    
    # Initialize risk analytics
    risk_engine = RiskAnalyticsEngine()
    
    # Test with existing portfolio (you'll need to have created one first)
    try:
        from portfolio_database import PortfolioDatabase
        
        # Create test portfolio if needed
        db = PortfolioDatabase()
        portfolios = db.get_all_portfolios()
        
        if portfolios:
            portfolio_id = portfolios[0]['portfolio_id']
            print(f"\n📊 Analyzing portfolio: {portfolios[0]['name']}")
            
            # Risk analysis
            print("\n🎯 Calculating risk metrics...")
            risk_metrics = risk_engine.calculate_portfolio_risk(portfolio_id)
            
            print(f"💰 Portfolio Value: ₹{risk_metrics.total_value:,.2f}")
            print(f"📉 Daily VaR (95%): ₹{risk_metrics.daily_var_95:,.2f}")
            print(f"📉 Daily VaR (99%): ₹{risk_metrics.daily_var_99:,.2f}")
            print(f"📈 Portfolio Beta: {risk_metrics.portfolio_beta:.2f}")
            print(f"⚡ Sharpe Ratio: {risk_metrics.sharpe_ratio:.2f}")
            print(f"📊 Annual Volatility: {risk_metrics.volatility:.1%}")
            print(f"📉 Max Drawdown: {risk_metrics.max_drawdown:.1%}")
            print(f"🔗 Correlation Risk: {risk_metrics.correlation_risk:.1%}")
            print(f"🎯 Concentration Risk: {risk_metrics.concentration_risk:.1%}")
            print(f"⚠️ Risk Score: {risk_metrics.risk_score}/100")
            print(f"💡 Recommendation: {risk_metrics.recommendation}")
            
            # Portfolio optimization
            print("\n🎯 Optimizing portfolio...")
            optimization = risk_engine.optimize_portfolio(portfolio_id)
            
            print(f"📈 Expected Return: {optimization.expected_return:.1%}")
            print(f"📊 Expected Volatility: {optimization.expected_volatility:.1%}")
            print(f"⚡ Optimized Sharpe: {optimization.sharpe_ratio:.2f}")
            print(f"💡 Improvement: {optimization.potential_improvement}")
            
            print("\n🔄 Recommended Rebalancing:")
            for action in optimization.rebalancing_actions:
                print(f"   {action['action']} ₹{action['amount']:,.0f} of {action['symbol']} "
                      f"({action['current_weight']:.1f}% → {action['target_weight']:.1f}%)")
            
            # Stress testing
            print("\n⚠️ Stress Testing Results:")
            stress_results = risk_engine.stress_test_portfolio(portfolio_id)
            for scenario, loss in stress_results.items():
                print(f"   {scenario}: ₹{loss:,.0f} potential loss")
            
        else:
            print("❌ No portfolios found. Create a portfolio first using portfolio_database.py")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n🎉 Risk analytics engine ready!")