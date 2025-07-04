import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="VoluGuard: Option Seller Cockpit",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Enhanced CSS for Visual Appeal ---
st.markdown("""
    <style>
    /* Dark Theme with Neon Green Accents */
    .main {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 2px solid #00FF00;
        border-radius: 5px;
        padding: 8px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #00FF00, #00CC00);
        color: #121212;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #00CC00, #00FF00);
    }
    .stSidebar {
        background-color: #1E1E1E;
        border-right: 2px solid #00FF00;
    }
    .stTabs > div > button {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 2px solid #00FF00;
        border-radius: 5px;
        margin: 5px;
    }
    .stTabs > div > button:hover {
        background: linear-gradient(45deg, #00FF00, #00CC00);
        color: #121212;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00FF00;
        text-shadow: 0 0 5px #00FF00;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E1E1E, #252526);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 255, 0, 0.2);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .error {
        color: #FF4D4D;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 5px;
    }
    .success {
        color: #00FF00;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 5px;
    }
    .header {
        background: linear-gradient(45deg, #00FF00, #00CC00);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 2.5em;
        text-align: center;
        animation: gradient 3s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
BASE_API_URL = "https://golu-8xwd.onrender.com"  # Real API URL
SESSION_STATE_KEY = "access_token"

# --- Helper Functions ---
def validate_access_token(token: str) -> bool:
    """Validates the Upstox access token by hitting the /expiries endpoint."""
    try:
        response = requests.get(f"{BASE_API_URL}/expiries", params={"access_token": token}, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        st.error(f"Token validation failed: {str(e)}")
        return False

def api_request(endpoint: str, method: str = "GET", params: dict = None, json_data: dict = None):
    """Makes an API request with the access token."""
    token = st.session_state.get(SESSION_STATE_KEY)
    if not token:
        return None, "Please enter a valid access token."
    params = params or {}
    params["access_token"] = token
    try:
        if method == "GET":
            response = requests.get(f"{BASE_API_URL}{endpoint}", params=params, timeout=10)
        elif method == "POST":
            response = requests.post(f"{BASE_API_URL}{endpoint}", json=json_data, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.HTTPError as e:
        return None, f"API Error: {e.response.status_code} - {e.response.text}"
    except requests.RequestException as e:
        return None, f"Network Error: {str(e)}"

# --- Session Management ---
if "access_token" not in st.session_state:
    st.session_state[SESSION_STATE_KEY] = None
    st.session_state["authenticated"] = False

# --- Login Screen ---
if not st.session_state["authenticated"]:
    st.markdown("<h1 class='header'>🔐 VoluGuard: Option Seller Cockpit</h1>", unsafe_allow_html=True)
    st.markdown("Enter your Upstox access token to unlock the trading cockpit.")
    
    with st.form("login_form"):
        access_token = st.text_input("Upstox Access Token", type="password", placeholder="Enter your access token")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if access_token and validate_access_token(access_token):
                st.session_state[SESSION_STATE_KEY] = access_token
                st.session_state["authenticated"] = True
                st.success("✅ Access token validated! Welcome to VoluGuard.")
                st.rerun()
            else:
                st.error("❌ Insert correct access token.")
else:
    # --- Main Dashboard ---
    st.markdown("<h1 class='header'>📈 VoluGuard: Option Seller Cockpit</h1>", unsafe_allow_html=True)
    st.markdown(f"**Connected** | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")

    # Logout Button
    if st.button("🚪 Logout"):
        st.session_state[SESSION_STATE_KEY] = None
        st.session_state["authenticated"] = False
        st.rerun()

    # Sidebar Navigation
    with st.sidebar:
        selected = option_menu(
            "Navigation",
            ["Dashboard", "Strategy Suggestions", "Risk Evaluation", "Option Chain", "Trade Log", "Journal"],
            icons=["speedometer2", "lightbulb", "shield-check", "table", "book", "journal-text"],
            menu_icon="rocket",
            default_index=0,
            styles={
                "container": {"background-color": "#1E1E1E"},
                "icon": {"color": "#00FF00"},
                "nav-link": {"color": "#E0E0E0", "--hover-color": "#00FF00"},
                "nav-link-selected": {"background": "linear-gradient(45deg, #00FF00, #00CC00)", "color": "#121212"},
            }
        )

    # --- Dashboard Tab ---
    if selected == "Dashboard":
        st.header("Option Seller Dashboard")
        data, error = api_request("/option-seller-dashboard")
        
        if error:
            st.error(error)
        elif data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### Market Overview")
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("Nifty Spot", f"₹{data.get('nifty_spot', 0):.2f}")
                st.metric("India VIX", f"{data.get('india_vix', 0):.2f}")
                st.metric("Days to Expiry", f"{data.get('days_to_expiry', 0)}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("### ATM Metrics")
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("ATM Strike", f"₹{data.get('atm_strike', 0):.2f}")
                st.metric("Straddle Price", f"₹{data.get('straddle_price', 0):.2f}")
                st.metric("Average IV", f"{data.get('avg_iv', 0):.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("### Greeks & Volatility")
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("Theta", f"{data.get('theta', 0):.2f}")
                st.metric("Vega", f"{data.get('vega', 0):.2f}")
                st.metric("7-Day HV", f"{data.get('hv_7_day', 0):.2f}%")
                st.metric("GARCH 7-Day", f"{data.get('garch_7_day', 0):.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("### Market Metrics")
            col4, col5 = st.columns(2)
            with col4:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("Put-Call Ratio (PCR)", f"{data.get('pcr', 0):.2f}")
                st.metric("Max Pain", f"₹{data.get('max_pain', 0):.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col5:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("IV-RV Spread", f"{data.get('iv_rv_spread', 0):.2f}%")
                st.metric("Probability of Profit (POP)", f"{data.get('pop', 0):.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- Strategy Suggestions Tab ---
    elif selected == "Strategy Suggestions":
        st.header("Strategy Suggestions")
        data, error = api_request("/suggest/strategy")
        
        if error:
            st.error(error)
        elif data:
            st.markdown(f"**Market Regime**: {data.get('regime', 'N/A')} (Score: {data.get('score', 0)})")
            st.markdown(f"**Note**: {data.get('note', 'N/A')}")
            st.markdown(f"**Explanation**: {data.get('explanation', 'N/A')}")
            if data.get("event_warning"):
                st.warning(f"⚠️ {data['event_warning']}")
            
            st.subheader("Recommended Strategies")
            for strategy in data.get("strategies", []):
                with st.expander(f"📊 {strategy}", expanded=False):
                    st.write(f"**Rationale**: {data.get('rationale', 'N/A')}")
                    lots = st.number_input(f"Number of Lots for {strategy}", min_value=1, max_value=10, value=1, step=1)
                    details, details_error = api_request(
                        "/strategy/details",
                        method="POST",
                        json_data={"strategy": strategy, "lots": lots}
                    )
                    if details_error:
                        st.error(details_error)
                    elif details:
                        st.write(f"**Premium**: ₹{details.get('premium_total', 0):.2f}")
                        st.write(f"**Max Profit**: ₹{details.get('max_profit', 0):.2f}")
                        max_loss = details.get('max_loss', float('inf'))
                        st.write(f"**Max Loss**: {'Unlimited' if max_loss == float('inf') else f'₹{max_loss:.2f}'}")
                        st.write("**Strikes**:")
                        for strike in details.get("strikes", []):
                            st.write(f"- ₹{strike:.2f}")
                        st.write("**Orders**:")
                        orders_df = pd.DataFrame([
                            {
                                "Instrument": order.get("instrument_key", "N/A"),
                                "Type": order.get("transaction_type", "N/A"),
                                "Quantity": order.get("quantity", 0),
                                "Price": f"₹{order.get('price', 0):.2f}",
                                "Current Price": f"₹{order.get('current_price', 0):.2f}"
                            } for order in details.get("orders", [])
                        ])
                        st.table(orders_df)
                        # Execute Strategy Button
                        if st.button(f"Execute {strategy}", key=f"execute_{strategy}"):
                            execute_data = {
                                "orders": details.get("orders", []),
                                "strategy": strategy
                            }
                            execute_response, execute_error = api_request(
                                "/place/multileg",
                                method="POST",
                                json_data=execute_data
                            )
                            if execute_error:
                                st.error(f"Execution failed: {execute_error}")
                            else:
                                st.success(f"✅ {strategy} executed successfully! Order ID: {execute_response.get('order_id', 'N/A')}")

    # --- Risk Evaluation Tab ---
    elif selected == "Risk Evaluation":
        st.header("Portfolio Risk Evaluation")
        active_trades = []  # Fetch real positions from Upstox if available
        data, error = api_request(
            "/evaluate/risk",
            method="POST",
            json_data={"active_trades": active_trades}
        )
        
        if error:
            st.error(error)
        elif data:
            portfolio = data.get("portfolio", {})
            st.subheader("Portfolio Summary")
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Total Funds", f"₹{portfolio.get('Total Funds', 0):.2f}")
            st.metric("Capital Deployed", f"₹{portfolio.get('Capital Deployed', 0):.2f}")
            st.metric("Exposure", f"{portfolio.get('Exposure Percent', 0):.2f}%")
            st.metric("Risk on Table", f"₹{portfolio.get('Risk on Table', 0):.2f}")
            st.metric("Total Vega", f"{portfolio.get('Total Vega Exposure', 0):.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.subheader("Flags")
            for flag in portfolio.get("Flags", []):
                if "❌" in flag or "⚠️" in flag:
                    st.error(flag)
                else:
                    st.success(flag)
            
            st.subheader("Strategy Breakdown")
            summary_df = pd.DataFrame(data.get("summary", []))
            if not summary_df.empty:
                st.dataframe(summary_df.style.format({
                    "Capital Used": "₹{:.2f}",
                    "Cap Limit": "₹{:.2f}",
                    "% Used": "{:.2f}%",
                    "Potential Risk": "₹{:.2f}",
                    "Risk Limit": "₹{:.2f}",
                    "Realized P&L": "₹{:.2f}",
                    "Unrealized P&L": "₹{:.2f}",
                    "Vega": "{:.2f}"
                }))
                # Risk Visualization
                fig = go.Figure(data=[
                    go.Bar(name="Capital Used", x=summary_df["Strategy"], y=summary_df["Capital Used"], marker_color='#00FF00'),
                    go.Bar(name="Cap Limit", x=summary_df["Strategy"], y=summary_df["Cap Limit"], marker_color='#00CC00')
                ])
                fig.update_layout(
                    title="Capital Utilization by Strategy",
                    barmode="group",
                    template="plotly_dark",
                    height=400,
                    plot_bgcolor="#121212",
                    paper_bgcolor="#121212",
                    font_color="#E0E0E0"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No risk data available. Ensure active trades are present.")

    # --- Option Chain Tab ---
    elif selected == "Option Chain":
        st.header("Option Chain Analysis")
        data, error = api_request("/full-chain-table")
        
        if error:
            st.error(error)
        elif data:
            chain_df = pd.DataFrame(data.get("data", []))
            if not chain_df.empty:
                st.dataframe(chain_df.style.format({
                    "Strike": "₹{:.2f}",
                    "Call IV": "{:.2f}%",
                    "Put IV": "{:.2f}%",
                    "IV Skew": "{:.4f}",
                    "Total Theta": "{:.2f}",
                    "Total Vega": "{:.2f}",
                    "Straddle Price": "₹{:.2f}",
                    "Total OI": "{:,.0f}"
                }))
                # IV Skew Plot
                fig = px.line(chain_df, x="Strike", y="IV Skew", title="IV Skew Across Strikes", color_discrete_sequence=['#00FF00'])
                fig.update_layout(
                    template="plotly_dark",
                    height=400,
                    plot_bgcolor="#121212",
                    paper_bgcolor="#121212",
                    font_color="#E0E0E0"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No option chain data available.")

    # --- Trade Log Tab ---
    elif selected == "Trade Log":
        st.header("Trade Log")
        status_filter = st.selectbox("Filter by Status", ["All", "open", "closed"])
        if st.button("🔄 Refresh Trades"):
            st.rerun()
        params = {}
        if status_filter != "All":
            params["status"] = status_filter
        data, error = api_request("/fetch/trades", params=params)
        
        if error:
            st.error(f"Failed to fetch trades: {error}")
        elif data:
            trades_df = pd.DataFrame(data.get("trades", []))
            if not trades_df.empty:
                st.dataframe(trades_df.style.format({
                    "entry_price": "₹{:.2f}",
                    "quantity": "{:.0f}",
                    "realized_pnl": "₹{:.2f}",
                    "unrealized_pnl": "₹{:.2f}",
                    "capital_used": "₹{:.2f}",
                    "potential_loss": "₹{:.2f}",
                    "vega": "{:.2f}"
                }))
            else:
                st.info("No trades found. Check Supabase configuration or place trades to populate the log.")

    # --- Journal Tab ---
    elif selected == "Journal":
        st.header("Trading Journal")
        with st.form("journal_form"):
            title = st.text_input("Title", placeholder="Enter journal title")
            content = st.text_area("Content", placeholder="Describe your trading day or insights")
            mood = st.selectbox("Mood", ["Positive", "Neutral", "Negative"])
            tags = st.text_input("Tags (comma-separated)", placeholder="e.g., volatility, strategy, learning")
            submit = st.form_submit_button("Add Journal Entry")
            
            if submit:
                if not title or not content:
                    st.error("Title and Content are required.")
                else:
                    journal_data = {"title": title, "content": content, "mood": mood, "tags": tags}
                    data, error = api_request("/log/journal", method="POST", json_data=journal_data)
                    if error:
                        st.error(f"Failed to save journal: {error}")
                    else:
                        st.success("✅ Journal entry saved successfully!")
                        st.rerun()
        
        data, error = api_request("/fetch/journals")
        if error:
            st.error(f"Failed to fetch journals: {error}")
        elif data:
            journals_df = pd.DataFrame(data.get("journals", []))
            if not journals_df.empty:
                for _, journal in journals_df.iterrows():
                    with st.expander(journal.get("title", "Untitled")):
                        st.write(f"**Mood**: {journal.get('mood', 'N/A')}")
                        st.write(f"**Content**: {journal.get('content', 'N/A')}")
                        st.write(f"**Tags**: {journal.get('tags', 'N/A')}")
                        st.write(f"**Timestamp**: {journal.get('timestamp', 'N/A')}")
            else:
                st.info("No journal entries found. Add entries to start tracking your trading insights.")
