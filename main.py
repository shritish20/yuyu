import streamlit as st
import httpx
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

# --- Synchronous HTTP Client (using httpx.Client) ---
@st.cache_resource
def get_http_client():
    """Returns an httpx.Client instance, cached for efficiency."""
    return httpx.Client(base_url=FASTAPI_BASE_URL, timeout=60.0) # Increased timeout

client = get_http_client()

# --- Functions to call Backend API Endpoints (now synchronous) ---

def fetch_metrics(access_token: str):
    """Fetches core financial metrics from the backend."""
    try:
        response = client.get("/metrics", params={"access_token": access_token})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error fetching metrics: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error while fetching metrics: {e}</div>", unsafe_allow_html=True)
        return None

def fetch_strategy_suggestion(access_token: str):
    """Fetches strategy suggestions from the backend."""
    try:
        response = client.get("/strategy_suggestion", params={"access_token": access_token})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error fetching strategy suggestions: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error while fetching strategy suggestions: {e}</div>", unsafe_allow_html=True)
        return None

def create_single_leg_order(access_token: str, order_data: dict):
    """Places a single-leg order via the backend."""
    try:
        response = client.post("/create_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing order: {e}</div>", unsafe_allow_html=True)
        return None

def create_multi_leg_order(access_token: str, order_data: dict):
    """Places a multi-leg order via the backend."""
    try:
        response = client.post("/multi_leg_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing multi-leg order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing multi-leg order: {e}</div>", unsafe_allow_html=True)
        return None

def create_single_gtt_order(access_token: str, order_data: dict):
    """Places a single-leg GTT order via the backend."""
    try:
        response = client.post("/create_gtt_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing GTT order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing GTT order: {e}</div>", unsafe_allow_html=True)
        return None

def create_multi_leg_gtt_order(access_token: str, order_data: dict):
    """Places a multi-leg GTT order via the backend."""
    try:
        response = client.post("/multi_leg_gtt_order", params={"access_token": access_token}, json=order_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error placing multi-leg GTT order: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error placing multi-leg GTT order: {e}</div>", unsafe_allow_html=True)
        return None

def log_trade(access_token: str, trade_data: dict):
    """Logs a trade to the backend."""
    try:
        response = client.post("/trades", params={"access_token": access_token}, json=trade_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.markdown(f"<div class='error-box'>Error logging trade: {e.response.status_code} - {e.response.text}</div>", unsafe_allow_html=True)
        return None
    except httpx.RequestError as e:
        st.markdown(f"<div class='error-box'>Network error logging trade: {e}</div>", unsafe_allow_html=True)
        return None

def fetch_journal_entries(access_token: str):
    """Fetches trade journal entries from the backend."""
    try:
        response = client.get("/journal", params={"access_token": access_token})
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

    # Initialize session state for data if not present (good)
    if 'metrics_data_cache' not in st.session_state:
        st.session_state['metrics_data_cache'] = None
    if 'strategy_data_cache' not in st.session_state:
        st.session_state['strategy_data_cache'] = None

    # Initialize local variables to None at the very beginning of the function
    metrics_data = None
    strategy_data = None

    if st.button("Refresh Market Data", key="refresh_dashboard_btn"):
        # Explicitly clear cached data to force new fetch
        st.session_state['metrics_data_cache'] = None
        st.session_state['strategy_data_cache'] = None
        # Ensure local variables are also reset for the current run
        metrics_data = None
        strategy_data = None

    # If data is not in cache, attempt to fetch
    if st.session_state['metrics_data_cache'] is None or st.session_state['strategy_data_cache'] is None:
        with st.spinner("Fetching live market data and calculating insights..."):
            temp_metrics = fetch_metrics(access_token)
            if temp_metrics:
                st.session_state['metrics_data_cache'] = temp_metrics
                temp_strategy = fetch_strategy_suggestion(access_token)
                if temp_strategy:
                    st.session_state['strategy_data_cache'] = temp_strategy
                    st.markdown("<div class='success-box'>Market data fetched and insights generated successfully!</div>", unsafe_allow_html=True)
                else:
                    # Strategy failed to fetch, but metrics were fine. Keep strategy_data_cache as None.
                    st.session_state['strategy_data_cache'] = None # Explicitly set to None
                    st.markdown("<div class='warning-box'>Metrics fetched, but failed to fetch strategy suggestions. Backend issue?</div>", unsafe_allow_html=True)
            else:
                # Metrics failed to fetch. Both caches will remain None.
                st.session_state['metrics_data_cache'] = None # Explicitly set to None
                st.session_state['strategy_data_cache'] = None # Explicitly set to None
                st.markdown("<div class='error-box'>Failed to fetch market metrics. Please check your Access Token and backend server deployment.</div>", unsafe_allow_html=True)
    
    # Assign local variables from the cached session state values for current render cycle
    # This happens *after* the fetch attempt, ensuring local variables are always bound.
    metrics_data = st.session_state['metrics_data_cache']
    strategy_data = st.session_state['strategy_data_cache']


    # Now render based on the local variables
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
    else:
        st.info("Click 'Refresh Market Data' to load insights.")


    if strategy_data: # This is the line that caused the error, now `strategy_data` is guaranteed to be bound
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
    elif metrics_data: # Only show this warning if metrics were fetched but strategy failed
         st.markdown("<div class='warning-box'>Could not retrieve Volatility Regime and Strategy Suggestions. Please check backend logs for issues.</div>", unsafe_allow_html=True)


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
    st.markdown("---")
    st.markdown("##### Common Order Parameters (for demonstration)")

    # Provide a placeholder for instrument token and guide user
    st.markdown("""
    <div class="info-box">
        <p><strong>Instrument Token:</strong> You need to provide the correct instrument token for the specific option contract (e.g., NIFTY24AUG19500CE) from your broker's API documentation or a reliable source.</p>
        <p>Example for Nifty 50 CE option with strike 19500 expiring in Aug 2024: `NSE_FO|15948` (this is an example, actual token varies)</p>
    </div>
    """, unsafe_allow_html=True)
    instrument_token_val = st.text_input("Instrument Token", value="NSE_FO|YOUR_INSTRUMENT_TOKEN", key="inst_token_common")
    transaction_type_val = st.selectbox("Transaction Type", ["BUY", "SELL"], key="trans_type_common")
    quantity_val = st.number_input("Quantity", min_value=1, value=50, step=50, key="qty_common")
    product_type_val = st.selectbox("Product Type", ["D", "I", "C", "B"], help="D: Delivery, I: Intraday, C: Cover Order, B: Bracket Order", key="prod_type_common") # Assuming Upstox types
    order_mode_val = st.selectbox("Order Mode", ["REGULAR", "AMO"], help="REGULAR: Normal, AMO: After Market Order", key="order_mode_common")
    validity_val = st.selectbox("Validity", ["DAY", "IOC", "GTD", "GTC"], help="DAY: Day order, IOC: Immediate or Cancel, GTD: Good Till Date, GTC: Good Till Cancelled", key="validity_common")

    # Handle GTD validity date if selected
    gtd_date = None
    if validity_val == "GTD":
        gtd_date = st.date_input("Good Till Date", min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=7), key="gtd_validity_date")


    if order_type_selection == "Single-Leg Order":
        st.markdown("#### Place Single-Leg Order")
        st.info("This section allows placing a simple BUY/SELL order.")
        price_type_val = st.selectbox("Price Type", ["LIMIT", "MARKET"], key="price_type_single")
        price_val = st.number_input("Price (for LIMIT orders)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="price_single", disabled=(price_type_val == "MARKET"))
        trigger_price_val = st.number_input("Trigger Price (for SL orders)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="trigger_single")

        if st.button("Place Single-Leg Order", key="place_single_order_btn"):
            if not instrument_token_val or "YOUR_INSTRUMENT_TOKEN" in instrument_token_val:
                st.error("Please enter a valid Instrument Token.")
            elif price_type_val == "LIMIT" and price_val <= 0:
                st.error("Limit Price must be greater than 0 for LIMIT orders.")
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
                if validity_val == "GTD":
                    order_data["gtd_date"] = gtd_date.strftime("%Y-%m-%d")

                with st.spinner("Placing single-leg order..."):
                    response = create_single_leg_order(access_token, order_data) # Synchronous call
                    if response:
                        st.markdown(f"<div class='success-box'>Order Placed Successfully: {response}</div>", unsafe_allow_html=True)

    elif order_type_selection == "Multi-Leg Order":
        st.markdown("#### Place Multi-Leg Order")
        st.info("Define multiple legs for a strategy. Example: Buy Call + Sell Call for a spread.")

        if 'multi_legs' not in st.session_state:
            st.session_state.multi_legs = [{"leg_id": 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'}] # Initialize with defaults

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
            
            # Optional Trigger Price for each leg (if applicable for multi-leg in your backend)
            leg['trigger_price'] = st.number_input(f"Trigger Price Leg {i+1} (for SL)", min_value=0.0, value=leg.get('trigger_price', 0.0), step=0.05, format="%.2f", key=f"multi_trigger_{i}")

            if st.button(f"Remove Leg {i+1}", key=f"remove_leg_{i}"):
                st.session_state.multi_legs.pop(i)
                st.rerun()

        if st.button("Add Another Leg", key="add_leg_btn"):
            st.session_state.multi_legs.append({"leg_id": len(st.session_state.multi_legs) + 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'})
            st.rerun()

        if st.button("Place Multi-Leg Order", key="place_multi_order_btn"):
            valid_legs = True
            for i, leg in enumerate(st.session_state.multi_legs):
                if not leg.get('instrument_token') or "YOUR_INSTRUMENT_TOKEN" in leg['instrument_token']:
                    st.error(f"Please provide a valid Instrument Token for Leg {i+1}.")
                    valid_legs = False
                    break
                if leg.get('price_type') == "LIMIT" and leg.get('price') <= 0:
                    st.error(f"Limit Price for Leg {i+1} must be greater than 0 for LIMIT orders.")
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
                            "price": leg['price'] if leg['price_type'] == "LIMIT" else 0.0,
                            "trigger_price": leg['trigger_price'] # Include trigger price for each leg
                        } for leg in st.session_state.multi_legs
                    ]
                }
                if validity_val == "GTD":
                    order_data["gtd_date"] = gtd_date.strftime("%Y-%m-%d")

                with st.spinner("Placing multi-leg order..."):
                    response = create_multi_leg_order(access_token, order_data) # Synchronous call
                    if response:
                        st.markdown(f"<div class='success-box'>Multi-Leg Order Placed Successfully: {response}</div>", unsafe_allow_html=True)
                st.session_state.multi_legs = [{"leg_id": 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'}] # Reset legs after submission
                st.rerun()

    elif order_type_selection == "Single-Leg GTT Order":
        st.markdown("#### Place Single-Leg GTT Order")
        st.info("Good Till Triggered (GTT) orders are active until triggered or cancelled. Requires a trigger price and an expiry date.")
        price_type_val = st.selectbox("Price Type", ["LIMIT"], key="price_type_gtt_single") # GTT is typically LIMIT
        price_val = st.number_input("Price (Limit Price)", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="price_gtt_single")
        trigger_price_val = st.number_input("Trigger Price", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="trigger_gtt_single")
        gtt_expiry_date = st.date_input("GTT Expiry Date", min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=7))

        if st.button("Place Single-Leg GTT Order", key="place_gtt_single_order_btn"):
            if not instrument_token_val or "YOUR_INSTRUMENT_TOKEN" in instrument_token_val:
                st.error("Please enter a valid Instrument Token.")
            elif trigger_price_val <= 0:
                st.error("Trigger Price must be greater than 0 for GTT orders.")
            elif price_val <= 0:
                 st.error("Limit Price must be greater than 0 for GTT orders.")
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
                    response = create_single_gtt_order(access_token, order_data) # Synchronous call
                    if response:
                        st.markdown(f"<div class='success-box'>GTT Order Placed Successfully: {response}</div>", unsafe_allow_html=True)

    elif order_type_selection == "Multi-Leg GTT Order":
        st.markdown("#### Place Multi-Leg GTT Order")
        st.info("Define multiple legs for a GTT strategy. All legs trigger together when the GTT condition is met.")

        if 'multi_gtt_legs' not in st.session_state:
            st.session_state.multi_gtt_legs = [{"leg_id": 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'}]

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
            st.session_state.multi_gtt_legs.append({"leg_id": len(st.session_state.multi_gtt_legs) + 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'})
            st.rerun()

        if st.button("Place Multi-Leg GTT Order", key="place_multi_gtt_order_btn"):
            valid_legs = True
            for i, leg in enumerate(st.session_state.multi_gtt_legs):
                if not leg.get('instrument_token') or "YOUR_INSTRUMENT_TOKEN" in leg['instrument_token']:
                    st.error(f"Please provide Instrument Token for Leg {i+1} GTT.")
                    valid_legs = False
                    break
                if leg.get('price') <= 0:
                    st.error(f"Limit Price for Leg {i+1} GTT must be greater than 0.")
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
                    response = create_multi_leg_gtt_order(access_token, order_data) # Synchronous call
                    if response:
                        st.markdown(f"<div class='success-box'>Multi-Leg GTT Order Placed Successfully: {response}</div>", unsafe_allow_html=True)
                st.session_state.multi_gtt_legs = [{"leg_id": 1, 'transaction_type': 'BUY', 'price_type': 'LIMIT'}] # Reset legs
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
            trade_type = st.selectbox("Trade Type", ["Long", "Short", "Option_Buy", "Option_Sell"], key="journal_trade_type")
            entry_price = st.number_input("Entry Price", min_value=0.0, value=0.0, step=0.05, format="%.2f", key="journal_entry_price")
            exit_price = st.number_input("Exit Price (optional)", value=0.0, step=0.05, format="%.2f", key="journal_exit_price")
        with col2:
            trade_date = st.date_input("Trade Date", value=datetime.today(), key="journal_trade_date")
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="journal_quantity")
            pnl = st.number_input("P&L (optional)", value=0.0, step=0.01, format="%.2f", key="journal_pnl")
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
                    "exit_price": exit_price if exit_price > 0 else None, # Send None if not entered
                    "trade_date": trade_date.strftime("%Y-%m-%d"),
                    "quantity": quantity,
                    "pnl": pnl if pnl != 0 else None, # Send None if not entered
                    "notes": notes if notes else None
                }
                with st.spinner("Logging trade..."):
                    response = log_trade(access_token, trade_data) # Synchronous call
                    if response:
                        st.markdown(f"<div class='success-box'>Trade Logged Successfully: {response}</div>", unsafe_allow_html=True)
                        st.session_state['journal_fetched'] = False # Force refresh of journal display
                    else:
                        st.markdown("<div class='error-box'>Failed to log trade. Check backend for details.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Your Trade History")

    if st.button("Refresh Journal Entries", key="refresh_journal_btn"):
        st.session_state['journal_fetched'] = False # Force refetch

    # Initialize journal_entries in session state
    if 'journal_entries' not in st.session_state:
        st.session_state['journal_entries'] = []

    if not st.session_state.get('journal_fetched', False):
        with st.spinner("Fetching journal entries..."):
            journal_entries = fetch_journal_entries(access_token) # Synchronous call
            if journal_entries is not None: # Check explicitly for None
                st.session_state['journal_entries'] = journal_entries
                st.session_state['journal_fetched'] = True
                if journal_entries:
                    st.markdown("<div class='success-box'>Journal entries fetched successfully!</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='info-box'>No journal entries found in your record.</div>", unsafe_allow_html=True)
            else:
                st.session_state['journal_fetched'] = True # Mark as fetched even if error, to prevent infinite loop
                st.markdown("<div class='error-box'>Failed to fetch journal entries. Please check backend.</div>", unsafe_allow_html=True)
    
    if st.session_state.get('journal_entries'):
        df_journal = pd.DataFrame(st.session_state['journal_entries'])
        if not df_journal.empty:
            # Basic formatting for display
            if 'trade_date' in df_journal.columns:
                df_journal['trade_date'] = pd.to_datetime(df_journal['trade_date']).dt.date
            
            # Reorder columns for better readability if all expected columns are present
            desired_columns = ["trade_date", "symbol", "trade_type", "quantity", "entry_price", "exit_price", "pnl", "notes", "timestamp"]
            
            # Filter columns to only those present in the DataFrame
            display_columns = [col for col in desired_columns if col in df_journal.columns]
            
            st.dataframe(df_journal[display_columns], use_container_width=True)
        else:
            st.info("No journal entries to display yet. Log a trade above or ensure your backend has entries.")
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
    tab_titles = ["Dashboard", "Trade Execution", "Trade Journal"]
    dashboard_tab, trade_exec_tab, trade_journal_tab = st.tabs(tab_titles)

    with dashboard_tab:
        render_dashboard_tab(access_token)

    with trade_exec_tab:
        render_trade_execution_tab(access_token)

    with trade_journal_tab:
        render_trade_journal_tab(access_token)

