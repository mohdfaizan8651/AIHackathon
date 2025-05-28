from langchain_anthropic import ChatAnthropic
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from typing import List
import os
from cloudemodel import llm
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

def access_inventory_data():
    return "📦 Inventory: 1200 units in stock."

def access_logistics_data():
    return "🚚 Logistics: 3 shipments in transit."

def access_forecasting_data():
    return "📈 Forecast: Demand expected to rise 15% next quarter."

def access_margin_reports():
    return "💰 Margin: Gross margin is 38%."

def access_cost_breakdown():
    return "📊 Costs: Materials 45%, Labor 35%, Other 20%."

def access_pnl_report():
    return "📉 P&L: Q1 Net profit = $200K."

# STEP 3: Register tools
ALL_TOOLS = {
    "inventory": Tool(name="InventoryTool", func=access_inventory_data, description="Check inventory levels."),
    "logistics": Tool(name="LogisticsTool", func=access_logistics_data, description="Check shipping details."),
    "forecasting": Tool(name="ForecastTool", func=access_forecasting_data, description="Check future demand."),
    "margin": Tool(name="MarginTool", func=access_margin_reports, description="See margin reports."),
    "cost": Tool(name="CostTool", func=access_cost_breakdown, description="See cost breakdown."),
    "pnl": Tool(name="PnLTool", func=access_pnl_report, description="View profit and loss statement.")
}

# STEP 4: Define role-based access
ROLE_ACCESS = {
    "planning": ["inventory", "logistics", "forecasting"],
    "finance": ["margin", "cost", "pnl"],
    "admin": list(ALL_TOOLS.keys())
}

def get_tools_for_role(role: str) -> List[Tool]:
    allowed = ROLE_ACCESS.get(role.lower(), [])
    return [ALL_TOOLS[tool_key] for tool_key in allowed]

# STEP 5: Create agent with Claude 3.5 Sonnet
def create_agent_for_role(user_role: str):
    tools = get_tools_for_role(user_role)
    if not tools:
        raise PermissionError(f"❌ No tools authorized for role: {user_role}")

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    print(tools, "-----------------------Faizan-----------------",'---------------',agent)
    return agent

# STEP 6: Usage
def agent(query):
    user_role = input("Enter your role (planning, finance, admin): ").strip().lower()

    try:
        agent = create_agent_for_role(user_role)

        print(f"\n✅ Agent ready for '{user_role}' role.")
        # query = input("Ask something: ")
        result = agent.run(query)
        print("\n🤖 Claude's Response:\n", result)
        return result
    except PermissionError as e:
        print(str(e))
print(agent())