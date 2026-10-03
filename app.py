
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

DB_PATH = "ecommerce_hackathon.db"


# --------------------------------------------------
# Database helper
# --------------------------------------------------

def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# --------------------------------------------------
# Load models
# --------------------------------------------------

@st.cache_resource
def load_models():

    churn_model = joblib.load(
        "models/churn_model.pkl"
    )

    sentiment_model = joblib.load(
        "models/sentiment_model.pkl"
    )

    return churn_model, sentiment_model


churn_model, sentiment_model = load_models()


# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

st.sidebar.title("E-Commerce Analytics")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Churn Prediction",
        "Sentiment Analysis"
    ]
)


# ==================================================
# PAGE 1 - DASHBOARD
# ==================================================

if page == "Dashboard":

    st.title("📊 E-Commerce Dashboard")

    # ----------------------------------------------
    # KPI calculations
    # ----------------------------------------------

    revenue = run_query("""
        SELECT
            ROUND(
                SUM(
                    (quantity * unit_price)
                    - COALESCE(discount, 0)
                ),
                2
            ) AS total_revenue
        FROM orders
        WHERE returned = 0
    """)

    orders = run_query("""
        SELECT COUNT(DISTINCT order_id) AS total_orders
        FROM orders
    """)

    customers = run_query("""
        SELECT COUNT(DISTINCT customer_id) AS total_customers
        FROM customers
    """)

    total_revenue = revenue.iloc[0]["total_revenue"] or 0
    total_orders = orders.iloc[0]["total_orders"] or 0
    total_customers = customers.iloc[0]["total_customers"] or 0

    # ----------------------------------------------
    # KPI cards
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    st.divider()

    # ----------------------------------------------
    # Monthly Revenue
    # ----------------------------------------------

    monthly_revenue = run_query("""
        SELECT
            strftime('%Y-%m', order_date) AS month,

            ROUND(
                SUM(
                    (quantity * unit_price)
                    - COALESCE(discount, 0)
                ),
                2
            ) AS net_revenue

        FROM orders

        WHERE returned = 0

        GROUP BY strftime('%Y-%m', order_date)

        ORDER BY month
    """)

    # ----------------------------------------------
    # Category Revenue
    # ----------------------------------------------

    category_revenue = run_query("""
        SELECT
            p.category,

            ROUND(
                SUM(
                    (o.quantity * o.unit_price)
                    - COALESCE(o.discount, 0)
                ),
                2
            ) AS net_revenue

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        WHERE o.returned = 0

        GROUP BY p.category

        ORDER BY net_revenue DESC
    """)

    # ----------------------------------------------
    # Charts
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Monthly Revenue")

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.lineplot(
            data=monthly_revenue,
            x="month",
            y="net_revenue",
            marker="o",
            linewidth=2,
            ax=ax
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Net Revenue")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        plt.close(fig)

    with col2:

        st.subheader("Revenue by Category")

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        sns.barplot(
            data=category_revenue,
            x="net_revenue",
            y="category",
            hue="category",
            palette="viridis",
            legend=False,
            ax=ax
        )

        ax.set_xlabel("Net Revenue")
        ax.set_ylabel("Category")

        st.pyplot(fig)

        plt.close(fig)

    # ----------------------------------------------
    # City Revenue
    # ----------------------------------------------

    city_revenue = run_query("""
        SELECT
            c.city,

            ROUND(
                SUM(
                    (o.quantity * o.unit_price)
                    - COALESCE(o.discount, 0)
                ),
                2
            ) AS net_revenue

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        WHERE o.returned = 0

        GROUP BY c.city

        ORDER BY net_revenue DESC

        LIMIT 10
    """)

    st.subheader("Top 10 Cities by Revenue")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    sns.barplot(
        data=city_revenue,
        x="net_revenue",
        y="city",
        hue="city",
        palette="Blues_r",
        legend=False,
        ax=ax
    )

    ax.set_xlabel("Net Revenue")
    ax.set_ylabel("City")

    st.pyplot(fig)

    plt.close(fig)


# ==================================================
# PAGE 2 - CHURN PREDICTION
# ==================================================

elif page == "Churn Prediction":

    st.title("🎯 Customer Churn Prediction")

    st.write(
        "Enter customer purchase history and customer information "
        "to estimate the probability of churn."
    )

    # ----------------------------------------------
    # Input fields
    # ----------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        total_orders = st.number_input(
            "Total Orders",
            min_value=1,
            value=5
        )

        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=1000.0
        )

        average_order_value = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=200.0
        )

        days_since_last_order = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30
        )

    with col2:

        return_rate = st.number_input(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01
        )

        average_delivery_days = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=3.0
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        membership_type = st.selectbox(
            "Membership Type",
            [
                "Basic",
                "Silver",
                "Gold",
                "Premium"
            ]
        )

    # ----------------------------------------------
    # Prediction
    # ----------------------------------------------

    if st.button(
        "Predict Churn",
        type="primary"
    ):

        input_data = pd.DataFrame({
            "total_orders": [total_orders],
            "total_spending": [total_spending],
            "average_order_value": [average_order_value],
            "days_since_last_order": [days_since_last_order],
            "return_rate": [return_rate],
            "average_delivery_days": [average_delivery_days],
            "age": [age],
            "membership_type": [membership_type]
        })

        prediction = churn_model.predict(
            input_data
        )[0]

        probability = churn_model.predict_proba(
            input_data
        )[0][1]

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if prediction == 1:

                st.error(
                    "⚠️ Customer is predicted to CHURN"
                )

            else:

                st.success(
                    "✅ Customer is predicted to STAY"
                )

        with col2:

            st.metric(
                "Churn Probability",
                f"{probability:.2%}"
            )

            st.progress(
                float(probability)
            )


# ==================================================
# PAGE 3 - SENTIMENT ANALYSIS
# ==================================================

elif page == "Sentiment Analysis":

    st.title("💬 Review Sentiment Analysis")

    st.write(
        "Enter a customer review to predict its sentiment."
    )

    review_text = st.text_area(
        "Customer Review",
        placeholder="Enter review text here...",
        height=150
    )

    if st.button(
        "Analyze Sentiment",
        type="primary"
    ):

        if not review_text.strip():

            st.warning(
                "Please enter a review."
            )

        else:

            prediction = sentiment_model.predict(
                [review_text]
            )[0]

            # Probability if supported
            probabilities = sentiment_model.predict_proba(
                [review_text]
            )[0]

            classes = sentiment_model.classes_

            confidence = probabilities.max()

            st.divider()

            if prediction == "Positive":

                st.success(
                    f"😊 Sentiment: **{prediction}**"
                )

            elif prediction == "Negative":

                st.error(
                    f"😞 Sentiment: **{prediction}**"
                )

            else:

                st.warning(
                    f"😐 Sentiment: **{prediction}**"
                )

            st.metric(
                "Prediction Confidence",
                f"{confidence:.2%}"
            )
