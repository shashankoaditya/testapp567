import streamlit as st
from openai import OpenAI

# ---- CONFIG ----
MODEL_NAME = "gpt-4.1-mini"
USD_TO_INR = 83  # approx conversion

# Pricing (update if needed)
INPUT_COST_PER_1K = 0.00015
OUTPUT_COST_PER_1K = 0.0006

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- PAGE CONFIG ----
st.set_page_config(page_title="SAP T-Code Explorer", layout="wide")

# ---- IMPROVED CSS (FIXED VISIBILITY) ----
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }

    .stTextInput > div > div > input {
        background-color: #1f2937;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #374151;
    }

    .stButton button {
        border-radius: 10px;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
    }

    .metric-box {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        color: #ffffff;
        font-size: 15px;
        line-height: 1.6;
    }

    .metric-box b {
        color: #60a5fa;
    }

    h1, h2, h3, h4 {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# ---- SESSION STATE ----
if "response" not in st.session_state:
    st.session_state.response = ""
if "usage" not in st.session_state:
    st.session_state.usage = {}

# ---- LAYOUT ----
left_col, right_col = st.columns([3, 1])

# ---- LEFT PANEL ----
with left_col:
    st.title("SAP T-Code Explorer")

    tcode = st.text_input("Enter SAP T-Code")

    col1, col2 = st.columns(2)

    # ---- GET DETAILS ----
    with col1:
        if st.button("Get Details"):
            if tcode:
                with st.spinner("Fetching details..."):

                    prompt = f"""
                    Provide concise details for SAP T-code: {tcode}

                    Format:
                    Purpose: <short explanation>
                    Module: <module name>
                    Type: <Transactional / Configuration / Display>
                    """

                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2
                    )

                    result = response.choices[0].message.content
                    usage = response.usage

                    # Save state
                    st.session_state.response = result
                    st.session_state.usage = usage
            else:
                st.warning("Please enter a T-code")

    # ---- REFRESH BUTTON ----
    with col2:
        if st.button("Refresh"):
            st.session_state.response = ""
            st.session_state.usage = {}
            st.rerun()

    # ---- DISPLAY RESPONSE ----
    if st.session_state.response:
        st.subheader("Result")
        st.write(st.session_state.response)

# ---- RIGHT PANEL ----
with right_col:
    st.subheader("Usage Analytics")

    usage = st.session_state.usage

    if usage:
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        # Cost calculation
        input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
        output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K
        total_cost_usd = input_cost + output_cost
        total_cost_inr = total_cost_usd * USD_TO_INR

        st.markdown(f"""
        <div class="metric-box">
        <b>Input Tokens:</b> {input_tokens}<br>
        <b>Output Tokens:</b> {output_tokens}<br>
        <b>Total Tokens:</b> {total_tokens}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
        <b>Cost (USD):</b> ${total_cost_usd:.6f}<br>
        <b>Cost (INR):</b> ₹{total_cost_inr:.4f}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("No data yet")

    # ---- MODEL INFO ----
    st.markdown(f"""
    <div class="metric-box">
    <b>Model Used:</b><br>{MODEL_NAME}
    </div>
    """, unsafe_allow_html=True)
