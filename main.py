
import streamlit as st
from prediction import predict_cancellation, prepare_df


st.set_page_config(
    page_title="Hotel Booking Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
)


st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
    color: #1f77b4;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    text-align: center;
}

.high-risk {
    background-color: rgba(255,75,75,0.15);
    border-left: 5px solid red;
}

.low-risk {
    background-color: rgba(0,200,83,0.15);
    border-left: 5px solid green;
}

.stButton > button {
    width: 100%;
    height: 3rem;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("🏨 About")

    st.write("""
    This application predicts whether a hotel booking is likely to be cancelled.

    ### Model Information
    - Algorithm: Random Forest
    - Target Variable: `is_canceled`
    - Purpose: Reduce revenue loss from cancellations

    ### Features Used
    - Lead Time
    - ADR
    - Booking Changes
    - Waiting List Days
    - Special Requests
    - Previous Cancellations
    - Customer Information
    """)


st.markdown("""
<h1>🏨 Hotel Booking Cancellation Predictor</h1>

<p style='text-align:center; font-size:18px;'>
Predict the likelihood of a hotel booking being cancelled using Machine Learning.
</p>
""", unsafe_allow_html=True)

st.divider()


with st.expander("📋 Booking Information", expanded=True):

    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(2)

    with row1[0]:
        lead_time = st.number_input(
            "Lead Time (Days)",
            min_value=0,
            value=30
        )

    with row1[1]:
        adr = st.number_input(
            "Average Daily Rate (ADR)",
            min_value=0.0,
            value=100.0
        )

    with row1[2]:
        booking_changes = st.number_input(
            "Booking Changes",
            min_value=0,
            value=0
        )

    with row2[0]:
        days_in_waiting_list = st.number_input(
            "Days in Waiting List",
            min_value=0,
            value=0
        )

    with row2[1]:
        total_of_special_requests = st.number_input(
            "Special Requests",
            min_value=0,
            value=1
        )

    with row2[2]:
        previous_bookings_not_canceled = st.number_input(
            "Previous Successful Bookings",
            min_value=0,
            value=0
        )

    with row3[0]:
        market_segment = st.selectbox(
            "Market Segment",
            [
                'Complementary',
                'Corporate',
                'Direct',
                'segment_Groups',
                'Offline TA/TO',
                'Online TA',
                'Undefined'
            ]
        )

    with row3[1]:
        distribution_channel = st.selectbox(
            "Distribution Channel",
            [
                'Direct',
                'GDS',
                'TA/TO',
                'Undefined'
            ]
        )

    with row3[2]:
        deposit_type = st.selectbox(
            "Deposit Type",
            [
                'Non Refund',
                'Refundable'
            ]
        )

    with row4[0]:
        customer_type = st.selectbox(
            "Customer Type",
            [
                'Group',
                'Transient',
                'Transient-Party'
            ]
        )

    with row4[1]:
        previous_cancellations = st.number_input(
            "Previous Cancellations",
            min_value=0,
            value=0
        )


if st.button("🚀 Predict Cancellation Risk"):

    df = prepare_df(
        lead_time,
        previous_cancellations,
        booking_changes,
        total_of_special_requests,
        previous_bookings_not_canceled,
        adr,
        days_in_waiting_list,
        market_segment,
        distribution_channel,
        deposit_type,
        customer_type
    )

    with st.spinner("Analyzing booking details..."):
        prediction, probability = predict_cancellation(df)

    st.divider()

    st.subheader("📊 Prediction Results")

    st.metric(
        "Cancellation Probability",
        f"{probability:.2%}"
    )

    st.progress(float(probability))

    if prediction == 1:
        st.markdown(f"""
        <div class="result-box high-risk">
            <h2>⚠️ High Risk of Cancellation</h2>
            <h3>Probability: {probability:.2%}</h3>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="result-box low-risk">
            <h2>✅ Low Risk of Cancellation</h2>
            <h3>Probability: {probability:.2%}</h3>
        </div>
        """, unsafe_allow_html=True)


st.markdown("---")
