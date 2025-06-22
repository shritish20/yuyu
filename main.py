import streamlit as st
import pandas as pd
import numpy as np
import httpx
import plotly.express as px
import plotly.graph_objects as go
import json
import websockets
import asyncio
import threading
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = "https://golu-8xwd.onrender.com"  # Replace with your actual API URL
st.set_page_config(page_title="VoluGuard: Options Trading Dashboard", layout="wide", page_icon="📈")

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css');
    
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #00C4B4;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        border: none;
    }
    .stButton>button:hover {
        background-color: #009688;
    }
    .stTextInput>div>input {
        background-color: #2E2E2E;
        color: #FFFFFF;
        border: 1px solid #00C4B4;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00C4B4;
        border-bottom: 2px solid #00C4B4;
    }
    .metric-card {
        background-color: #2E2E2E;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .metric-label {
        font-size: 14px;
        color: #B0B0B0;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .flag-warning {
        color: #FF5252;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'ws_data' not in st.session_state:
    st.session_state.ws_data = []

# Helper Functions
async def fetch_api(endpoint, method="GET", data=None, params=None):
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"} if st.session_state.access_token else {}
    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(f"{API_BASE_URL}{endpoint}", json=data, headers=headers, params=params)
            else:
                response = await client.get(f"{API_BASE_URL}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            st.error(f"API Error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None

async def websocket_listener():
    try:
        ws_url_response = await fetch_api("/authorize-market-feed", params={"access_token": st.session_state.access_token})
        if not ws_url_response or not ws_url_response.get("socket_url"):
            st.error("Failed to get WebSocket URL")
            return
        ws_url = ws_url_response["socket_url"]
        
        async with websockets.connect(ws_url) as ws:
            while True:
                message = await ws.recv()
                st.session_state.ws_data.append({"timestamp": datetime.now().strftime("%H:%M:%S"), "data": message})
                if len(st.session_state.ws_data) > 50:  # Limit to last 50 messages
                    st.session_state.ws_data = st.session_state.ws_data[-50:]
    except Exception as e:
        st.error(f"WebSocket Error: {str(e)}")

def start_websocket():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_listener())

# Login Page
if not st.session_state.access_token:
    st.title("VoluGuard: Login")
    st.markdown("Enter your Upstox API access token to access the trading dashboard.")
    with st.form("login_form"):
        token = st.text_input("Upstox Access Token", type="password")
        if st.form_submit_button("Login"):
            if token:
                st.session_state.access_token = token
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Please enter a valid access token.")
else:
    # Main App
    st.title("VoluGuard: Options Trading Dashboard")
    st.markdown(f"Welcome to VoluGuard! Your institutional-grade options trading platform. <i class='fas fa-sign-out-alt'></i> [Logout](#)", unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.access_token = None
        st.session_state.ws_data = []
        st.rerun()

    # Tabs for navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Strategies", "Risk", "Option Chain", "Trade & Journal"])

    # Tab 1: Dashboard
    with tab1:
        st.header("Market Overview")
        dashboard_data = asyncio.run(fetch_api("/option-seller-dashboard", params={"access_token": st.session_state.access_token}))
        
        if dashboard_data:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Nifty Spot</div>
                        <div class="metric-value">{dashboard_data['nifty_spot']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">India VIX</div>
                        <div class="metric-value">{dashboard_data['india_vix']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">ATM IV</div>
                        <div class="metric-value">{dashboard_data['avg_iv']}%</div>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Straddle Price</div>
                        <div class="metric-value">{dashboard_data['straddle_price']}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.subheader("Volatility Metrics")
            vol_data = asyncio.run(fetch_api("/predict/volatility", params={"access_token": st.session_state.access_token}))
            if vol_data:
                vol_df = pd.DataFrame({
                    "Metric": ["Historical Vol (7d)", "GARCH Vol (7d)", "XGBoost Vol", "IVP", "IV-RV Spread"],
                    "Value": [
                        vol_data["volatility"]["hv_7"],
                        vol_data["volatility"]["garch_7d"],
                        vol_data["volatility"]["xgb_vol"],
                        vol_data["volatility"]["ivp"],
                        vol_data["volatility"]["iv_rv_spread"]
                    ]
                })
                fig_vol = px.bar(vol_df, x="Metric", y="Value", title="Volatility Metrics", color="Metric")
                st.plotly_chart(fig_vol, use_container_width=True)

            st.subheader("Market Regime")
            regime_data = asyncio.run(fetch_api("/calculate/regime", params={"access_token": st.session_state.access_token}))
            if regime_data:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Current Regime</div>
                        <div class="metric-value">{regime_data['regime']}</div>
                        <div style="font-size: 14px; color: #B0B0B0;">Score: {regime_data['score']} | {regime_data['note']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.write(regime_data['explanation'])

        # Start WebSocket for real-time data
        if st.button("Start Live Market Feed"):
            ws_thread = threading.Thread(target=start_websocket, daemon=True)
            ws_thread.start()
            st.success("WebSocket feed started!")

        if st.session_state.ws_data:
            st.subheader("Live Market Data Feed")
            ws_df = pd.DataFrame(st.session_state.ws_data)
            st.dataframe(ws_df, use_container_width=True)

    # Tab 2: Strategies
    with tab2:
        st.header("Strategy Suggestions")
        strategy_data = asyncio.run(fetch_api("/suggest/strategy", params={"access_token": st.session_state.access_token}))
        
        if strategy_data:
            st.write(f"**Suggested Strategies**: {', '.join(strategy_data['strategies'])}")
            st.write(f"**Rationale**: {strategy_data['rationale']}")
            if strategy_data.get("event_warning"):
                st.warning(strategy_data["event_warning"])

            st.subheader("Strategy Details")
            strategy_name = st.selectbox("Select Strategy", strategy_data['strategies'])
            lots = st.number_input("Number of Lots", min_value=1, value=1)
            
            if st.button("Get Strategy Details"):
                strategy_details = asyncio.run(fetch_api("/strategy/details", method="POST", data={"strategy": strategy_name, "lots": lots}, params={"access_token": st.session_state.access_token}))
                if strategy_details:
                    st.write(f"**Premium**: ₹{strategy_details['premium_total']:.2f} | **Max Profit**: ₹{strategy_details['max_profit']:.2f} | **Max Loss**: {'Unlimited' if strategy_details['max_loss'] == float('inf') else f'₹{strategy_details['max_loss']:.2f}'}")
                    orders_df = pd.DataFrame(strategy_details['orders'])
                    st.dataframe(orders_df, use_container_width=True)
                    
                    if st.button("Place Strategy Orders"):
                        order_response = asyncio.run(fetch_api("/execute/order", method="POST", data=strategy_details['orders'], params={"access_token": st.session_state.access_token}))
                        if order_response:
                            st.success("Orders placed successfully!")
                            st.json(order_response)

    # Tab 3: Risk
    with tab3:
        st.header("Portfolio Risk Evaluation")
        st.write("Upload active trades JSON or fetch from Upstox to evaluate risk.")
        
        uploaded_file = st.file_uploader("Upload Active Trades JSON", type="json")
        if uploaded_file:
            active_trades = json.load(uploaded_file)
            risk_data = asyncio.run(fetch_api("/evaluate/risk", method="POST", data={"active_trades": active_trades}, params={"access_token": st.session_state.access_token}))
            
            if risk_data:
                st.subheader("Portfolio Summary")
                portfolio_df = pd.DataFrame([risk_data['portfolio']])
                st.dataframe(portfolio_df, use_container_width=True)
                
                st.subheader("Strategy Risk")
                strategy_df = pd.DataFrame(risk_data['summary'])
                st.dataframe(strategy_df, use_container_width=True)
                
                st.subheader("Risk Flags")
                for flag in risk_data['portfolio']['Flags']:
                    st.markdown(f"<div class='flag-warning'>{flag}</div>", unsafe_allow_html=True)

    # Tab 4: Option Chain
    with tab4:
        st.header("Option Chain Analysis")
        chain_data = asyncio.run(fetch_api("/full-chain-table", params={"access_token": st.session_state.access_token}))
        
        if chain_data:
            chain_df = pd.DataFrame(chain_data['data'])
            st.dataframe(chain_df, use_container_width=True)
            
            st.subheader("IV Skew Visualization")
            fig_skew = px.line(chain_df, x="Strike", y="IV Skew", title="IV Skew Across Strikes")
            st.plotly_chart(fig_skew, use_container_width=True)

    # Tab 5: Trade & Journal
    with tab5:
        st.header("Trade and Journal Logging")
        
        st.subheader("Log a Trade")
        with st.form("trade_form"):
            strategy = st.text_input("Strategy")
            instrument_token = st.text_input("Instrument Token")
            entry_price = st.number_input("Entry Price", min_value=0.0)
            quantity = st.number_input("Quantity", min_value=0.0)
            realized_pnl = st.number_input("Realized P&L", value=0.0)
            unrealized_pnl = st.number_input("Unrealized P&L", value=0.0)
            notes = st.text_area("Notes")
            capital_used = st.number_input("Capital Used", min_value=0.0)
            potential_loss = st.number_input("Potential Loss", min_value=0.0)
            sl_hit = st.checkbox("Stop-Loss Hit")
            vega = st.number_input("Vega", value=0.0)
            status = st.selectbox("Status", ["open", "closed"])
            
            if st.form_submit_button("Log Trade"):
                trade_data = {
                    "strategy": strategy,
                    "instrument_token": instrument_token,
                    "entry_price": entry_price,
                    "quantity": quantity,
                    "realized_pnl": realized_pnl,
                    "unrealized_pnl": unrealized_pnl,
                    "notes": notes,
                    "capital_used": capital_used,
                    "potential_loss": potential_loss,
                    "sl_hit": sl_hit,
                    "vega": vega,
                    "status": status
                }
                trade_response = asyncio.run(fetch_api("/log/trade", method="POST", data=trade_data))
                if trade_response:
                    st.success("Trade logged successfully!")

        st.subheader("Log a Journal")
        with st.form("journal_form"):
            title = st.text_input("Title")
            content = st.text_area("Content")
            mood = st.selectbox("Mood", ["Positive", "Neutral", "Negative"])
            tags = st.text_input("Tags (comma-separated)")
            
            if st.form_submit_button("Log Journal"):
                journal_data = {
                    "title": title,
                    "content": content,
                    "mood": mood,
                    "tags": tags
                }
                journal_response = asyncio.run(fetch_api("/log/journal", method="POST", data=journal_data))
                if journal_response:
                    st.success("Journal logged successfully!")

        st.subheader("View Logs")
        trades = asyncio.run(fetch_api("/fetch/trades", params={"status": "closed"}))
        if trades:
            st.write("**Closed Trades**")
            trades_df = pd.DataFrame(trades['trades'])
            st.dataframe(trades_df, use_container_width=True)
        
        journals = asyncio.run(fetch_api("/fetch/journals"))
        if journals:
            st.write("**Journals**")
            journals_df = pd.DataFrame(journals['journals'])
            st.dataframe(journals_df, use_container_width=True)
