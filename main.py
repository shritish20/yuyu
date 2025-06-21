import streamlit as st
import httpx
import asyncio
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration ---
FASTAPI_BASE_URL = "https://golu-8xwd.onrender.com"

# --- Page Configuration ---
st.set_page_config(
    page_title="VoluGuard Pro - Comprehensive Trading & Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for enhanced UI ---
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #4CAF50; /* Green */
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px #aaa;
    }
    .subheader {
        font-size: 1.8em;
        font-weight: semi-bold;
        color: #2E8B57; /* SeaGreen */
        margin-top: 1em;
        margin-bottom: 0.5em;
        border-bottom: 2px solid #eee;
        padding-bottom: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-card-title {
        font-size: 1em;
        color: #555;
        margin-bottom: 5px;
    }
    .metric-card-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.1em;
        border: none;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 8px;
    }
    .info-box {
        background-color: #e6f7ff;
        border-left: 5px solid #2196F3;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        color: #721c24;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

# --- Async HTTP Client (using httpx) ---
@st.cache_resource
def get_http_client():
    """Returns an httpx.AsyncClient instance, cached for efficiency."""
    return httpx.AsyncClient(base_url=FASTAPI_BASE_URL, timeout=60.0) # Increased timeout

client = get_http_client()

# --- Functions to call Backend API Endpoints ---

async def fetch_metrics(access_token: str):
    """Fetches core financial metrics from the backend."""
    try:
        response = await client.get("/metrics", params={"access_token": access_token})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error fetching metrics: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error while fetching metrics: {e}</div>", unsafe_allow_html=True)
        return None

async def fetch_strategy_suggestion(access_token: str):
    """Fetches strategy suggestions from the backend."""
    try:
        response = await client.get("/strategy_suggestion", params={"access_token": access_token})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error fetching strategy suggestions: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error while fetching strategy suggestions: {e}</div>", unsafe_allow_html=True)
        return None

async def create_single_leg_order(access_token: str, order_data: dict):
    """Places a single-leg order via the backend."""
    try:
        response = await client.post("/create_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing order: {e}</div>", unsafe_allow_html=True)
        return None

async def create_multi_leg_order(access_token: str, order_data: dict):
    """Places a multi-leg order via the backend."""
    try:
        response = await client.post("/multi_leg_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing multi-leg order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing multi-leg order: {e}</div>", unsafe_allow_html=True)
        return None

async def create_single_gtt_order(access_token: str, order_data: dict):
    """Places a single-leg GTT order via the backend."""
    try:
        response = await client.post("/create_gtt_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing GTT order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing GTT order: {e}</div>", unsafe_allow_html=True)
        return None

async def create_multi_leg_gtt_order(access_token: str, order_data: dict):
    """Places a multi-leg GTT order via the backend."""
    try:
        response = await client.post("/multi_leg_gtt_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing multi-leg GTT order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing multi-leg GTT order: {e}</div>", unsafe_allow_html=True)
        return None

async def log_trade(access_token: str, trade_data: dict):
    """Logs a trade to the backend."""
    try:
        response = await client.post("/trades", params={"access_token": access_token}, json=trade_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error logging trade: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error logging trade: {e}</div>", unsafe_allow_html=True)
        return None

async def fetch_journal_entries(access_token: str):
    """Fetches trade journal entries from the backend."""
    try:
        response = await client.get("/journal", params={"access_token": access_token})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error fetching journal entries: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error fetching journal entries: {e}</div>", unsafe_allow_html=True)
        return None

# --- UI Components ---

def render_dashboard_tab(access_token):
    st.markdown('<p class="subheader">Current Market Overview</p>', unsafe_allow_html=True)

    if st.button("Refresh Market Data", key="refresh_dashboard_btn"):
        st.session_state['data_fetched'] = False # Force refetch
        st.session_state['metrics_data'] = None
        st.session_state['strategy_data'] = None

    if not st.session_state.get('data_fetched', False):
        with st.spinner("Fetching live market data and calculating insights..."):
            try:
                metrics_data = asyncio.run(fetch_metrics(access_token))
                strategy_data = asyncio.run(fetch_strategy_suggestion(access_token))

                if metrics_data and strategy_data:
                    st.session_state['metrics_data'] = metrics_data
                    st.session_state['strategy_data'] = strategy_data
                    st.session_state['data_fetched'] = True
                    st.markdown("<div class='success-box'>Market data fetched and insights generated successfully!</div>", unsafe_allow_html=True)
                elif metrics_data is None:
                    st.markdown("<div class='error-box'>Failed to fetch market metrics. Please check your Access Token and backend server.</div>", unsafe_allow_html=True)
                elif strategy_data is None:
                    st.markdown("<div class='error-box'>Failed to fetch strategy suggestions. This might indicate an issue with the backend's strategy calculation.</div>", unsafe_allow_html=True)
                else:
                     st.markdown("<div class='warning-box'>No data fetched. Please check Access Token and try again.</div>", unsafe_allow_html=True)


            except Exception as e:
                st.markdown(f"<div class='error-box'>An unexpected error occurred during data fetching: {e}</div>", unsafe_allow_html=True)
                st.session_state['data_fetched'] = False
                st.session_state['metrics_data'] = None
                st.session_state['strategy_data'] = None
    else:
        metrics_data = st.session_state.get('metrics_data')
        strategy_data = st.session_state.get('strategy_data')

    if metrics_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Nifty Spot</p>
                    <p class="metric-card-value">{metrics_data.get('nifty_spot', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">India VIX</p>
                    <p class="metric-card-value">{metrics_data.get('india_vix', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">ATM Strike</p>
                    <p class="metric-card-value">{metrics_data.get('atm_strike', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Days to Expiry</p>
                    <p class="metric-card-value">{metrics_data.get('days_to_expiry', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="subheader">Volatility & Option Metrics</p>', unsafe_allow_html=True)
        metrics_cols_1 = st.columns(4)
        metrics_cols_2 = st.columns(4)

        with metrics_cols_1[0]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Straddle Price</p>
                    <p class="metric-card-value">{metrics_data.get('straddle_price', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_1[1]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Avg IV</p>
                    <p class="metric-card-value">{metrics_data.get('avg_iv', 'N/A'):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_1[2]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Implied Volatility Percentile (IVP)</p>
                    <p class="metric-card-value">{metrics_data.get('ivp', 'N/A'):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_1[3]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">IV-RV Spread</p>
                    <p class="metric-card-value">{metrics_data.get('iv_rv_spread', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)

        with metrics_cols_2[0]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Historical Volatility (7-Day)</p>
                    <p class="metric-card-value">{metrics_data.get('hv_7_day', 'N/A'):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_2[1]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">GARCH Volatility (7-Day)</p>
                    <p class="metric-card-value">{metrics_data.get('garch_7_day', 'N/A'):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_2[2]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Max Pain</p>
                    <p class="metric-card-value">{metrics_data.get('max_pain', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)
        with metrics_cols_2[3]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">PCR</p>
                    <p class="metric-card-value">{metrics_data.get('pcr', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="subheader">Option Greeks</p>', unsafe_allow_html=True)
        greeks_cols = st.columns(5)
        with greeks_cols[0]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Theta</p>
                    <p class="metric-card-value">{metrics_data.get('theta', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with greeks_cols[1]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Vega</p>
                    <p class="metric-card-value">{metrics_data.get('vega', 'N/A'):.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with greeks_cols[2]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Delta</p>
                    <p class="metric-card-value">{metrics_data.get('delta', 'N/A'):.4f}</p>
                </div>
            """, unsafe_allow_html=True)
        with greeks_cols[3]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">Gamma</p>
                    <p class="metric-card-value">{metrics_data.get('gamma', 'N/A'):.6f}</p>
                </div>
            """, unsafe_allow_html=True)
        with greeks_cols[4]:
            st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-card-title">POP</p>
                    <p class="metric-card-value">{metrics_data.get('pop', 'N/A'):.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

    if strategy_data:
        st.markdown('<p class="subheader">Volatility Regime & Strategy Suggestion</p>', unsafe_allow_html=True)
        st.markdown(f"**Current Volatility Regime:** <span style='font-size: 1.2em; font-weight: bold; color: {'#FF4B4B' if 'High Vol' in strategy_data.get('regime_label', '') else '#4CAF50' if 'Low Vol' not in strategy_data.get('regime_label', '') else '#FFD700'};'>{strategy_data.get('regime_label', 'N/A')}</span>", unsafe_allow_html=True)
        st.write(f"**Regime Summary:** {strategy_data.get('regime_summary', 'N/A')}")
        st.write(f"**Regime Implications:** {strategy_data.get('regime_implications', 'N/A')}")
        st.write(f"**Regime Score:** {strategy_data.get('regime_score', 'N/A'):.2f}")

        st.subheader("Suggested Strategies")
        if strategy_data.get('suggested_strategies'):
            for strategy in strategy_data['suggested_strategies']:
                st.markdown(f"- **{strategy}**")
        else:
            st.info("No specific strategies suggested at this moment, or data is insufficient.")

        st.subheader("Strategy Rationale")
        if strategy_data.get('rationale'):
            for item in strategy_data['rationale']:
                st.write(f"- {item}")
        else:
            st.info("No detailed rationale available.")

        if strategy_data.get('event_warning'):
            st.markdown(f"""
                <div class="warning-box">
                    <p style="color: #ffc107;">{strategy_data['event_warning']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_trade_execution_tab(access_token):
    st.markdown('<p class="subheader">Trade Execution</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='warning-box'>
        <p><strong>Caution:</strong> This section allows placing live trading orders via your Upstox API. Ensure your Access Token is correct and understand the implications of placing real orders.</p>
        <p><strong>This app is for demonstration purposes. Use with extreme care in a live environment.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    order_type_selection = st.radio("Select Order Type", ["Single-Leg Order", "Multi-Leg Order", "Single-Leg GTT Order", "Multi-Leg GTT Order"])

    # --- Common Order Parameters (simplify for demo) ---
    # In a real app, you'd fetch instrument tokens, expiry dates etc.
    st.markdown("---")
    st.markdown("##### Common Order Parameters (for demonstration)")

    instrument_token_val = st.text_input("Instrument Token (e.g., NIFTY24AUG19500CE token)", value="YOUR_INSTRUMENT_TOKEN_HERE", key="inst_token_common")
    transaction_type_val = st.selectbox("Transaction Type", ["BUY", "SELL"], key="trans_type_common")
    quantity_val = st.number_input("Quantity", min_value=1, value=50, step=50, key="qty_common")
    product_type_val = st.selectbox("Product Type", ["D", "I", "C", "B"], help="D: Delivery, I: Intraday, C: Cover Order, B: Bracket Order", key="prod_type_common") # Assuming Upstox types
    order_mode_val = st.selectbox("Order Mode", ["REGULAR", "AMO"], help="REGULAR: Normal, AMO: After Market Order", key="order_mode_common")
    validity_val = st.selectbox("Validity", ["DAY", "IOC", "GTD", "GTC"], help="DAY: Day order, IOC: Immediate or Cancel, GTD: Good Till Date, GTC: Good Till Cancelled", key="validity_common")

    if order_type_selection == "Single-Leg Order":
        st.markdown("#### Place Single-Leg Order")
        st.info("This section allows placing a simple BUY/SELL order.")
        price_type_val = st.selectbox("Price Type", ["LIMIT", "MARKET"], key="price_type_single")
        price_val = st.number_input("Price (for LIMIT orders)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="price_single", disabled=(price_type_val == "MARKET"))
        trigger_price_val = st.number_input("Trigger Price (for SL orders)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="trigger_single")

        if st.button("Place Single-Leg Order", key="place_single_order_btn"):
            if not instrument_token_val or instrument_token_val == "YOUR_INSTRUMENT_TOKEN_HERE":
                st.error("Please enter a valid Instrument Token.")
            else:
                order_data = {
                    "instrument_token": instrument_token_val,
                    "transaction_type": transaction_type_val,
                    "quantity": quantity_val,
                    "price_type": price_type_val,
                    "price": price_val if price_type_val == "LIMIT" else 0.0,
                    "trigger_price": trigger_price_val,
                    "product_type": product_type_val,
                    "order_mode": order_mode_val,
                    "validity": validity_val
                }
                with st.spinner("Placing single-leg order..."):
                    response = asyncio.run(create_single_leg_order(access_token, order_data))
                    if response:
                        st.markdown(f"<div class='success-box'>Order Placed Successfully: {response}</div>", unsafe_allow_html=True)

    elif order_type_selection == "Multi-Leg Order":
        st.markdown("#### Place Multi-Leg Order")
        st.info("Define multiple legs for a strategy. Example: Buy Call + Sell Call for a spread.")

        if 'multi_legs' not in st.session_state:
            st.session_state.multi_legs = [{"leg_id": 1}]

        for i, leg in enumerate(st.session_state.multi_legs):
            st.subheader(f"Leg {i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                leg['instrument_token'] = st.text_input(f"Instrument Token Leg {i+1}", key=f"multi_inst_{i}", value=leg.get('instrument_token', ''))
            with col2:
                leg['transaction_type'] = st.selectbox(f"Transaction Type Leg {i+1}", ["BUY", "SELL"], key=f"multi_trans_{i}", index=["BUY", "SELL"].index(leg.get('transaction_type', 'BUY')))
            with col3:
                leg['quantity'] = st.number_input(f"Quantity Leg {i+1}", min_value=1, value=leg.get('quantity', 50), step=50, key=f"multi_qty_{i}")

            col4, col5 = st.columns(2)
            with col4:
                leg['price_type'] = st.selectbox(f"Price Type Leg {i+1}", ["LIMIT", "MARKET"], key=f"multi_price_type_{i}", index=["LIMIT", "MARKET"].index(leg.get('price_type', 'LIMIT')))
            with col5:
                leg['price'] = st.number_input(f"Price Leg {i+1} (for LIMIT)", min_value=0.0, value=leg.get('price', 0.0), step=0.05, format="%.2f", key=f"multi_price_{i}", disabled=(leg.get('price_type') == "MARKET"))

            if st.button(f"Remove Leg {i+1}", key=f"remove_leg_{i}"):
                st.session_state.multi_legs.pop(i)
                st.rerun()

        if st.button("Add Another Leg", key="add_leg_btn"):
            st.session_state.multi_legs.append({"leg_id": len(st.session_state.multi_legs) + 1})
            st.rerun()

        if st.button("Place Multi-Leg Order", key="place_multi_order_btn"):
            valid_legs = True
            for i, leg in enumerate(st.session_state.multi_legs):
                if not leg.get('instrument_token') or leg['instrument_token'] == "YOUR_INSTRUMENT_TOKEN_HERE":
                    st.error(f"Please provide Instrument Token for Leg {i+1}.")
                    valid_legs = False
                    break
            if valid_legs:
                order_data = {
                    "product_type": product_type_val,
                    "order_mode": order_mode_val,
                    "validity": validity_val,
                    "legs": [
                        {
                            "instrument_token": leg['instrument_token'],
                            "transaction_type": leg['transaction_type'],
                            "quantity": leg['quantity'],
                            "price_type": leg['price_type'],
                            "price": leg['price'] if leg['price_type'] == "LIMIT" else 0.0
                        } for leg in st.session_state.multi_legs
                    ]
                }
                with st.spinner("Placing multi-leg order..."):
                    response = asyncio.run(create_multi_leg_order(access_token, order_data))
                    if response:
                        st.markdown(f"<div class='success-box'>Multi-Leg Order Placed Successfully: {response}</div>", unsafe_allow_html=True)
                st.session_state.multi_legs = [{"leg_id": 1}] # Reset legs after submission
                st.rerun()

    elif order_type_selection == "Single-Leg GTT Order":
        st.markdown("#### Place Single-Leg GTT Order")
        st.info("Good Till Triggered (GTT) orders are active until triggered or cancelled. Requires a trigger price.")
        price_type_val = st.selectbox("Price Type", ["LIMIT"], key="price_type_gtt_single") # GTT is typically LIMIT
        price_val = st.number_input("Price (Limit Price)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="price_gtt_single")
        trigger_price_val = st.number_input("Trigger Price", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="trigger_gtt_single")
        gtt_expiry_date = st.date_input("GTT Expiry Date", min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=7))

        if st.button("Place Single-Leg GTT Order", key="place_gtt_single_order_btn"):
            if not instrument_token_val or instrument_token_val == "YOUR_INSTRUMENT_TOKEN_HERE":
                st.error("Please enter a valid Instrument Token.")
            elif trigger_price_val <= 0:
                st.error("Trigger Price must be greater than 0 for GTT orders.")
            else:
                order_data = {
                    "instrument_token": instrument_token_val,
                    "transaction_type": transaction_type_val,
                    "quantity": quantity_val,
                    "price_type": price_type_val,
                    "price": price_val,
                    "trigger_price": trigger_price_val,
                    "product_type": product_type_val,
                    "order_mode": order_mode_val,
                    "gtt_expiry_date": gtt_expiry_date.strftime("%Y-%m-%d")
                }
                with st.spinner("Placing single-leg GTT order..."):
                    response = asyncio.run(create_single_gtt_order(access_token, order_data))
                    if response:
                        st.markdown(f"<div class='success-box'>GTT Order Placed Successfully: {response}</div>", unsafe_allow_html=True)

    elif order_type_selection == "Multi-Leg GTT Order":
        st.markdown("#### Place Multi-Leg GTT Order")
        st.info("Define multiple legs for a GTT strategy. All legs trigger together when the GTT condition is met.")

        if 'multi_gtt_legs' not in st.session_state:
            st.session_state.multi_gtt_legs = [{"leg_id": 1}]

        gtt_expiry_date = st.date_input("GTT Expiry Date (for all legs)", min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=7), key="gtt_multi_expiry")
        trigger_price_val = st.number_input("Common Trigger Price (for Multi-Leg GTT)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="gtt_multi_trigger")

        for i, leg in enumerate(st.session_state.multi_gtt_legs):
            st.subheader(f"Leg {i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                leg['instrument_token'] = st.text_input(f"Instrument Token Leg {i+1} GTT", key=f"multi_gtt_inst_{i}", value=leg.get('instrument_token', ''))
            with col2:
                leg['transaction_type'] = st.selectbox(f"Transaction Type Leg {i+1} GTT", ["BUY", "SELL"], key=f"multi_gtt_trans_{i}", index=["BUY", "SELL"].index(leg.get('transaction_type', 'BUY')))
            with col3:
                leg['quantity'] = st.number_input(f"Quantity Leg {i+1} GTT", min_value=1, value=leg.get('quantity', 50), step=50, key=f"multi_gtt_qty_{i}")

            leg['price_type'] = st.selectbox(f"Price Type Leg {i+1} GTT", ["LIMIT"], key=f"multi_gtt_price_type_{i}", index=["LIMIT"].index(leg.get('price_type', 'LIMIT')))
            leg['price'] = st.number_input(f"Price Leg {i+1} (Limit Price) GTT", min_value=0.0, value=leg.get('price', 0.0), step=0.05, format="%.2f", key=f"multi_gtt_price_{i}")

            if st.button(f"Remove Leg {i+1} GTT", key=f"remove_gtt_leg_{i}"):
                st.session_state.multi_gtt_legs.pop(i)
                st.rerun()

        if st.button("Add Another Leg GTT", key="add_gtt_leg_btn"):
            st.session_state.multi_gtt_legs.append({"leg_id": len(st.session_state.multi_gtt_legs) + 1})
            st.rerun()

        if st.button("Place Multi-Leg GTT Order", key="place_multi_gtt_order_btn"):
            valid_legs = True
            for i, leg in enumerate(st.session_state.multi_gtt_legs):
                if not leg.get('instrument_token') or leg['instrument_token'] == "YOUR_INSTRUMENT_TOKEN_HERE":
                    st.error(f"Please provide Instrument Token for Leg {i+1} GTT.")
                    valid_legs = False
                    break
            if trigger_price_val <= 0:
                st.error("Common Trigger Price must be greater than 0 for GTT orders.")
                valid_legs = False

            if valid_legs:
                order_data = {
                    "product_type": product_type_val,
                    "order_mode": order_mode_val,
                    "gtt_expiry_date": gtt_expiry_date.strftime("%Y-%m-%d"),
                    "trigger_price": trigger_price_val,
                    "legs": [
                        {
                            "instrument_token": leg['instrument_token'],
                            "transaction_type": leg['transaction_type'],
                            "quantity": leg['quantity'],
                            "price_type": leg['price_type'],
                            "price": leg['price']
                        } for leg in st.session_state.multi_gtt_legs
                    ]
                }
                with st.spinner("Placing multi-leg GTT order..."):
                    response = asyncio.run(create_multi_leg_gtt_order(access_token, order_data))
                    if response:
                        st.markdown(f"<div class='success-box'>Multi-Leg GTT Order Placed Successfully: {response}</div>", unsafe_allow_html=True)
                st.session_state.multi_gtt_legs = [{"leg_id": 1}] # Reset legs
                st.rerun()

def render_trade_journal_tab(access_token):
    st.markdown('<p class="subheader">Trade Journal</p>', unsafe_allow_html=True)
    st.info("This section allows you to log manual trades and view your trade history.")

    # --- Manual Trade Logging Form ---
    st.markdown("#### Log a New Trade Manually")
    with st.form("log_trade_form"):
        col1, col2 = st.columns(2)
        with col1:
            symbol = st.text_input("Symbol (e.g., NIFTY)", key="journal_symbol")
            trade_type = st.selectbox("Trade Type", ["Long", "Short"], key="journal_trade_type")
            entry_price = st.number_input("Entry Price", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="journal_entry_price")
            exit_price = st.number_input("Exit Price", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="journal_exit_price")
        with col2:
            trade_date = st.date_input("Trade Date", value=datetime.today(), key="journal_trade_date")
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="journal_quantity")
            pnl = st.number_input("P&L", value=0.0, step=0.01, format="%.2f", key="journal_pnl")
            notes = st.text_area("Notes", key="journal_notes")

        submitted = st.form_submit_button("Log Trade")
        if submitted:
            if not symbol or entry_price <= 0 or quantity <= 0:
                st.error("Please fill in Symbol, Entry Price, and Quantity for the trade.")
            else:
                trade_data = {
                    "symbol": symbol,
                    "trade_type": trade_type,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "trade_date": trade_date.strftime("%Y-%m-%d"),
                    "quantity": quantity,
                    "pnl": pnl,
                    "notes": notes
                }
                with st.spinner("Logging trade..."):
                    response = asyncio.run(log_trade(access_token, trade_data))
                    if response:
                        st.markdown(f"<div class='success-box'>Trade Logged Successfully: {response}</div>", unsafe_allow_html=True)
                        st.session_state['journal_fetched'] = False # Force refresh of journal display
                    else:
                        st.markdown("<div class='error-box'>Failed to log trade.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Your Trade History")

    if st.button("Refresh Journal Entries", key="refresh_journal_btn"):
        st.session_state['journal_fetched'] = False # Force refetch

    if not st.session_state.get('journal_fetched', False):
        with st.spinner("Fetching journal entries..."):
            journal_entries = asyncio.run(fetch_journal_entries(access_token))
            if journal_entries:
                st.session_state['journal_entries'] = journal_entries
                st.session_state['journal_fetched'] = True
                st.markdown("<div class='success-box'>Journal entries fetched successfully!</div>", unsafe_allow_html=True)
            else:
                st.session_state['journal_entries'] = []
                st.session_state['journal_fetched'] = True # Mark as fetched even if empty or error
                st.markdown("<div class='info-box'>No journal entries found or an error occurred.</div>", unsafe_allow_html=True)
    
    if st.session_state.get('journal_entries'):
        df_journal = pd.DataFrame(st.session_state['journal_entries'])
        # Basic formatting for display
        df_journal['trade_date'] = pd.to_datetime(df_journal['trade_date']).dt.date
        st.dataframe(df_journal, use_container_width=True)
    else:
        st.info("No journal entries to display yet. Log a trade above or ensure your backend has entries.")


# --- Main Application Flow ---

st.markdown('<p class="main-header">VoluGuard Pro</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2em;">Comprehensive Volatility Analysis, Strategy & Trading Platform</p>', unsafe_allow_html=True)

st.sidebar.title("Configuration")
access_token = st.sidebar.text_input("Upstox API Access Token", type="password", help="Enter your Upstox API access token here.")

if not access_token:
    st.sidebar.warning("Please enter your Upstox API Access Token to proceed.")
    st.info("""
        <div class="info-box">
            <p><strong>To get started:</strong></p>
            <ol>
                <li>Enter your Upstox API Access Token in the sidebar.</li>
                <li>The application will then enable tabs for analysis and trading.</li>
            </ol>
            <p>Your Access Token is crucial for connecting to the backend to retrieve live market data and interact with trading functionalities.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Initialize session state for tabs if not present
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = "Dashboard"

    tab_titles = ["Dashboard", "Trade Execution", "Trade Journal"]
    dashboard_tab, trade_exec_tab, trade_journal_tab = st.tabs(tab_titles)

    with dashboard_tab:
        render_dashboard_tab(access_token)

    with trade_exec_tab:
        render_trade_execution_tab(access_token)

    with trade_journal_tab:
        render_trade_journal_tab(access_token)

