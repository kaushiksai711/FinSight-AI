from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dataclasses import dataclass
from enum import Enum
import json

# Data Models
class TimePeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

@dataclass
class FinancialMetrics:
    net_worth: Optional[float] = None
    cash_flow: Optional[float] = None
    investment_returns: Optional[float] = None
    credit_utilization: Optional[float] = None
    savings_rate: Optional[float] = None
    debt_to_income: Optional[float] = None
    expense_categories: Optional[Dict[str, float]] = None

class AnalyticsAgent:
    def __init__(self, fi_money_agent):
        self.fi_money_agent = fi_money_agent
        self.metrics = FinancialMetrics()
        self._setup_tools()
    
    def _setup_tools(self):
        self.tools = [
            FunctionTool(
                func=self.analyze_spending_patterns
            ),
            FunctionTool(
                name="calculate_investment_performance",
                description="Calculate investment returns and performance metrics",
                func=self.calculate_investment_performance
            ),
            FunctionTool(
                name="assess_financial_health",
                description="Assess overall financial health score",
                func=self.assess_financial_health
            ),
            FunctionTool(
                name="predict_future_wealth",
                description="Predict future net worth based on current trends",
                func=self.predict_future_wealth
            ),
            FunctionTool(
                name="get_credit_insights",
                description="Get insights from credit report data",
                func=self.get_credit_insights
            )
        ]
    
    async def analyze_spending_patterns(self, period: TimePeriod = TimePeriod.MONTHLY) -> Dict:
        """Analyze spending patterns over a specified time period."""
        try:
            # Get transactions from FI Money
            end_date = datetime.now()
            if period == TimePeriod.MONTHLY:
                start_date = end_date - timedelta(days=30)
            elif period == TimePeriod.WEEKLY:
                start_date = end_date - timedelta(weeks=4)
            else:  # Default to 90 days
                start_date = end_date - timedelta(days=90)
            
            # Format dates as strings for the API
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # Get transactions data
            transactions = await self.fi_money_agent.get_transactions(
                start_date=start_str,
                end_date=end_str
            )
            
            # Process transactions (simplified example)
            df = pd.DataFrame(transactions)
            if df.empty:
                return {"status": "No transaction data available", "period": period.value}
            
            # Basic spending analysis
            df['date'] = pd.to_datetime(df['date'])
            df['amount'] = pd.to_numeric(df['amount'])
            
            # Group by category and sum amounts
            spending_by_category = df.groupby('category')['amount'].sum().to_dict()
            
            # Calculate total spending
            total_spent = df[df['amount'] < 0]['amount'].sum() * -1
            
            # Calculate monthly average
            num_months = (end_date - start_date).days / 30
            monthly_avg = total_spent / max(1, num_months)
            
            return {
                "status": "success",
                "period": period.value,
                "total_spent": total_spent,
                "monthly_average": monthly_avg,
                "spending_by_category": spending_by_category,
                "transaction_count": len(df)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def calculate_investment_performance(self) -> Dict:
        """Calculate investment performance metrics."""
        try:
            # Get net worth data which includes investments
            net_worth = await self.fi_money_agent.get_net_worth()
            
            if not net_worth or 'investments' not in net_worth:
                return {"status": "No investment data available"}
            
            investments = net_worth['investments']
            
            # Calculate total investments and returns
            total_invested = sum(inv.get('invested_amount', 0) for inv in investments)
            current_value = sum(inv.get('current_value', 0) for inv in investments)
            total_return = current_value - total_invested
            
            # Calculate XIRR (simplified)
            xirr = self._calculate_xirr(investments) if investments else 0
            
            # Get asset allocation
            asset_allocation = {}
            for inv in investments:
                asset_type = inv.get('asset_type', 'Other')
                asset_allocation[asset_type] = asset_allocation.get(asset_type, 0) + inv.get('current_value', 0)
            
            return {
                "status": "success",
                "total_invested": total_invested,
                "current_value": current_value,
                "total_return": total_return,
                "return_percentage": (total_return / total_invested * 100) if total_invested > 0 else 0,
                "xirr": xirr,
                "asset_allocation": asset_allocation
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _calculate_xirr(self, investments: List[Dict]) -> float:
        """Calculate XIRR for investments (simplified)."""
        # This is a simplified version - real implementation would need actual dates and cash flows
        try:
            # Mock implementation - replace with actual XIRR calculation
            if not investments:
                return 0.0
                
            # Get current date and one year ago
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            # Calculate time-weighted return
            total_invested = sum(inv.get('invested_amount', 0) for inv in investments)
            current_value = sum(inv.get('current_value', 0) for inv in investments)
            
            if total_invested <= 0:
                return 0.0
                
            # Simple annualized return (for demo purposes)
            # In a real implementation, use actual dates and cash flows
            time_period = (end_date - start_date).days / 365
            if time_period <= 0:
                return 0.0
                
            cagr = (current_value / total_invested) ** (1 / time_period) - 1
            return cagr * 100  # Convert to percentage
            
        except Exception:
            return 0.0
    
    async def assess_financial_health(self) -> Dict:
        """Assess overall financial health."""
        try:
            # Get required data
            net_worth_data = await self.fi_money_agent.get_net_worth()
            credit_report = await self.fi_money_agent.get_credit_report()
            
            # Calculate metrics
            score = 0
            metrics = {}
            
            # Net worth analysis
            if net_worth_data:
                assets = net_worth_data.get('total_assets', 0)
                liabilities = net_worth_data.get('total_liabilities', 0)
                net_worth = assets - liabilities
                
                # Score based on net worth to income ratio (simplified)
                # In a real implementation, you'd use actual income data
                if net_worth > 0:
                    score += 25
                metrics['net_worth'] = net_worth
            
            # Credit score analysis
            if credit_report and 'credit_score' in credit_report:
                credit_score = credit_report['credit_score']
                if credit_score >= 750:
                    score += 25
                elif credit_score >= 700:
                    score += 20
                elif credit_score >= 650:
                    score += 15
                metrics['credit_score'] = credit_score
            
            # Debt to income ratio (simplified)
            # In a real implementation, calculate actual debt to income ratio
            if net_worth_data and 'monthly_income' in net_worth_data:
                monthly_income = net_worth_data['monthly_income']
                if monthly_income > 0:
                    debt_to_income = (liabilities / 12) / monthly_income  # Annual liabilities / monthly income
                    if debt_to_income <= 0.35:
                        score += 25
                    elif debt_to_income <= 0.5:
                        score += 15
                    metrics['debt_to_income'] = debt_to_income
            
            # Emergency fund (simplified)
            if net_worth_data and 'liquid_assets' in net_worth_data:
                liquid_assets = net_worth_data['liquid_assets']
                monthly_expenses = net_worth_data.get('monthly_expenses', 1)  # Avoid division by zero
                emergency_months = liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
                
                if emergency_months >= 6:
                    score += 25
                elif emergency_months >= 3:
                    score += 15
                metrics['emergency_fund_months'] = emergency_months
            
            # Cap score at 100
            score = min(100, score)
            
            return {
                "status": "success",
                "financial_health_score": score,
                "metrics": metrics,
                "recommendations": self._generate_recommendations(score, metrics)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _generate_recommendations(self, score: int, metrics: Dict) -> List[str]:
        """Generate personalized financial recommendations."""
        recommendations = []
        
        # Net worth recommendations
        if metrics.get('net_worth', 0) < 0:
            recommendations.append("Focus on reducing debt to improve your net worth.")
        
        # Credit score recommendations
        credit_score = metrics.get('credit_score')
        if credit_score:
            if credit_score < 650:
                recommendations.append("Consider improving your credit score by paying bills on time and reducing credit utilization.")
        
        # Emergency fund recommendations
        emergency_months = metrics.get('emergency_fund_months', 0)
        if emergency_months < 3:
            recommendations.append(f"Build an emergency fund to cover at least 3-6 months of expenses. You currently have {emergency_months:.1f} months covered.")
        
        # Debt to income recommendations
        debt_to_income = metrics.get('debt_to_income')
        if debt_to_income and debt_to_income > 0.35:
            recommendations.append("Consider strategies to reduce your debt-to-income ratio, such as paying down high-interest debt.")
        
        if not recommendations:
            recommendations.append("Your financial health looks good! Continue with your current financial habits.")
        
        return recommendations
    
    async def predict_future_wealth(self, years: int = 5, monthly_contribution: float = 0) -> Dict:
        """Predict future net worth based on current trends."""
        try:
            # Get current financial data
            net_worth_data = await self.fi_money_agent.get_net_worth()
            
            if not net_worth_data:
                return {"status": "No net worth data available"}
            
            current_net_worth = net_worth_data.get('net_worth', 0)
            
            # Make projections (simplified)
            # In a real implementation, use more sophisticated modeling
            projected_net_worth = current_net_worth
            projections = []
            
            # Assume average annual return of 7% (adjust as needed)
            annual_return = 0.07
            
            for year in range(1, years + 1):
                # Add annual contributions and apply returns
                projected_net_worth = (projected_net_worth + (monthly_contribution * 12)) * (1 + annual_return)
                projections.append({
                    "year": year,
                    "projected_net_worth": projected_net_worth,
                    "total_contributions": monthly_contribution * 12 * year
                })
            
            return {
                "status": "success",
                "current_net_worth": current_net_worth,
                "monthly_contribution": monthly_contribution,
                "projected_annual_return": annual_return * 100,  # as percentage
                "projections": projections
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_credit_insights(self) -> Dict:
        """Get insights from credit report data."""
        try:
            credit_report = await self.fi_money_agent.get_credit_report()
            
            if not credit_report:
                return {"status": "No credit report data available"}
            
            insights = {
                "credit_score": credit_report.get('credit_score'),
                "score_range": credit_report.get('score_range', '300-900'),
                "credit_utilization": credit_report.get('credit_utilization'),
                "total_accounts": len(credit_report.get('accounts', [])),
                "credit_age_months": credit_report.get('credit_age_months'),
                "hard_inquiries": len(credit_report.get('inquiries', [])),
                "derogatory_marks": credit_report.get('derogatory_marks', 0)
            }
            
            # Generate insights
            recommendations = []
            
            # Credit utilization
            utilization = insights.get('credit_utilization', 0)
            if utilization > 0.3:  # More than 30% utilization
                recommendations.append("Your credit utilization is high. Try to keep it below 30% for a better credit score.")
            
            # Credit age
            credit_age_years = (insights.get('credit_age_months', 0) or 0) / 12
            if credit_age_years < 2:
                recommendations.append("Your credit history is relatively short. Keep accounts open to build a longer credit history.")
            
            # Hard inquiries
            if insights.get('hard_inquiries', 0) > 3:
                recommendations.append("You have several recent hard inquiries. Try to limit new credit applications.")
            
            # Derogatory marks
            if insights.get('derogatory_marks', 0) > 0:
                recommendations.append("You have derogatory marks on your credit report. Consider addressing these to improve your credit score.")
            
            insights["recommendations"] = recommendations or ["Your credit profile looks good! Keep up the good financial habits."]
            
            return {"status": "success", "insights": insights}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Create the analytics agent instance
analytics_agent = AnalyticsAgent(fi_money_agent=None)  # Will be set when initializing
