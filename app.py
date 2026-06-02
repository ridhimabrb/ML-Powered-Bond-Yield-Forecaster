import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.bond import bond_price
from utils.forecast import (
    forecast_yield, latest_yield )

st.set_page_config(
    page_title="Bond Pricing Dashboard",
    page_icon="📈",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title(" Quant Bond Pricing Dashboard")

tab1, tab2, tab3 = st.tabs(
[
    "Bond Analytics",
    "ML Forecast",
    "Scenario Analysis"
]
)


 # SIDEBAR

st.sidebar.header("Bond Parameters")

face_value = st.sidebar.number_input(
    "Face Value",
    value=1000
)

coupon_rate = st.sidebar.slider(
    "Coupon Rate %",
    0.0,
    20.0,
    8.0
)

market_yield = st.sidebar.slider(
    "Market Yield %",
    0.0,
    20.0,
    10.0
)

years = st.sidebar.slider(
    "Years",
    1,
    30,
    10
)

with tab1:
    price = bond_price(
    face_value,
    coupon_rate,
    market_yield,
    years
    )
    st.markdown(
    """
    Analyze bond prices,
    cashflows,
    and yield sensitivity.
    """
    )

# TOP METRICS

    col1, col2, col3 = st.columns(3)

    coupon = face_value * coupon_rate / 100

    col1.metric(
    "Bond Price",
    f"₹{price:,.2f}"
    )

    col2.metric(
    "Annual Coupon",
    f"₹{coupon:,.2f}"
    )

    col3.metric(
    "Years",
    years
    )

    st.divider()

# CASHFLOW TABLE

    cashflows = []
    pv_values = []

    for t in range(1, years + 1):

        if t == years:
            cf = coupon + face_value
        else:
            cf = coupon

        pv = cf / ((1 + market_yield / 100) ** t)

        cashflows.append(cf)
        pv_values.append(pv)

    df = pd.DataFrame({
    "Year": range(1, years + 1),
    "Cashflow": cashflows,
    "Present Value": pv_values
    })

    left, right = st.columns(2)

    with left:

        st.subheader("Cashflow Schedule")

        st.dataframe(
            df,
            use_container_width=True
        )

    with right:

        st.subheader("Present Value Distribution")

        fig = px.bar(
            df,
            x="Year",
            y="Present Value"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

# YIELD CURVE

    st.subheader("Yield Sensitivity")

    yield_range = []
    prices = []

    for y in range(1, 21):

        p = bond_price(
            face_value,
            coupon_rate,
            y,
            years
        )

        yield_range.append(y)
        prices.append(p)

    curve_df = pd.DataFrame({
        "Yield": yield_range,
        "Price": prices
    })

    fig2 = px.line(
        curve_df,
        x="Yield",
        y="Price",
        markers=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with tab2:
    st.caption(
    "Forecast generated using Random Forest Regression trained on Indian 10-Year Government Security yield data."
    )

    predicted_yield = forecast_yield()

    current_yield = latest_yield()

    st.subheader("Yield Forecast")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Yield",
        f"{current_yield:.2f}%"
    )

    col2.metric(
        "Predicted Yield",
        f"{predicted_yield:.2f}%"
    )

    col3.metric(
        "Change",
        f"{predicted_yield-current_yield:.2f}%"
    )


    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
        mode="gauge+number",
        value=predicted_yield,
        title={"text":"Predicted Yield"}
        )
    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )

with tab3:

    st.subheader("Forecasted Bond Impact")

    # ML prediction
    predicted_yield = forecast_yield()

    # Use sidebar market yield as current yield
    current_yield = market_yield

    # Current bond valuation
    current_price = bond_price(
        face_value,
        coupon_rate,
        current_yield,
        years
    )

    # Forecasted bond valuation
    future_price = bond_price(
        face_value,
        coupon_rate,
        predicted_yield,
        years
    )

    # Expected return
    change = (
        (future_price - current_price)
        / current_price
    ) * 100

    # Yield comparison
    st.markdown("### Yield Comparison")

    y1, y2 = st.columns(2)

    y1.metric(
        "Current Market Yield",
        f"{current_yield:.2f}%"
    )

    y2.metric(
        "ML Forecast Yield",
        f"{predicted_yield:.2f}%"
    )

    st.divider()

    # Price comparison
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Price",
        f"₹{current_price:,.2f}"
    )

    col2.metric(
        "Forecast Price",
        f"₹{future_price:,.2f}"
    )

    col3.metric(
        "Expected Return %",
        f"{change:.2f}%"
    )

    st.divider()

    st.info(
        """
        The Random Forest model forecasts future Indian
        Government Security yields using historical yield data.

        The forecasted yield is then used to re-price the bond
        using discounted cash flow valuation.

        Try adjusting the Market Yield, Coupon Rate, Face Value,
        and Maturity in the sidebar to see how bond valuations
        change under different interest-rate scenarios.
        """
    )