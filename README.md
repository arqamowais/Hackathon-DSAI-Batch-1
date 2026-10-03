🛒 E-Commerce Data Science Hackathon

An end-to-end Data Science and Machine Learning project for analyzing e-commerce data, understanding customer behavior, predicting customer churn, and performing sentiment analysis on customer reviews.

The project covers the complete data science workflow from SQL data analysis and cleaning to machine learning, NLP, visualization, and Streamlit deployment.

🚀 Project Features
📊 E-Commerce Dashboard

Total revenue

Total orders

Total customers

Monthly revenue trend

Category-wise revenue

City-wise revenue

Return rate analysis

🎯 Customer Churn Prediction

Three classification models were developed and compared:

Logistic Regression

Random Forest

Feed-Forward Neural Network

Evaluation metrics include:

Accuracy

Precision

Recall

F1-score

ROC-AUC

Confusion Matrix

💬 Sentiment Analysis

Customer reviews are classified into:

🟢 Positive

🟡 Neutral

🔴 Negative

The NLP pipeline uses:

Text cleaning

TF-IDF

Logistic Regression
```
🗂️ Project Structure
Hackathon-DSAI-Batch-1/
│
├── Final_Hackathon.ipynb       # Complete data science notebook
├── app.py                      # Streamlit application
├── ecommerce_hackathon.db      # SQLite database
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── models/
    ├── churn_model.pkl         # Saved churn model
    └── sentiment_model.pkl     # Saved sentiment model
```
🛠️ Technologies Used
Technology	Purpose
Python	Programming language
Pandas	Data manipulation
NumPy	Numerical operations
SQLite	Database
SQL	Business queries
Matplotlib	Data visualization
Seaborn	Statistical visualization
Scikit-learn	Machine Learning & NLP
TensorFlow/Keras	Neural Network
Streamlit	Web application
Joblib	Model serialization
📈 Data Analysis

SQL was used for the required business queries, including:

Total net revenue

Top customers by spending

Category-wise revenue

Category-wise order count

Quantity sold

Monthly net revenue

Top products by revenue

Pandas was used after extracting the required data from SQL for further analysis and visualization.

📊 Visualizations

The project includes the following visualizations:

Monthly Revenue Trend

Category-wise Revenue

City-wise Revenue

Return Rate by Product Category

These visualizations are used to identify revenue trends, high-performing categories, geographic performance, and product return behavior.

🎯 Customer Churn Prediction
Churn Definition

Customer features are created using orders up to:

31 May 2026


The target period is:

1 June 2026 → 31 August 2026


A customer is labeled:

Churn = 1


if they make no purchase during the target period.

Otherwise:

Churn = 0

Features

The following customer-level features are used:

Total orders

Total spending

Average order value

Days since last order

Return rate

Average delivery days

Age

Membership type

Model Comparison
Model	Accuracy	Precision	Recall	F1-score	ROC-AUC
Logistic Regression	0.711	0.663	0.835	0.739	0.784
Random Forest	0.698	0.661	0.788	0.719	0.763
Neural Network	0.706	0.657	0.838	0.737	0.784

The results show that the neural network did not provide a meaningful improvement over the simpler machine learning models.

💬 Sentiment Analysis

Review ratings are converted into sentiment labels:

Rating	Sentiment
1–2	Negative
3	Neutral
4–5	Positive
NLP Pipeline
Customer Review
       ↓
Text Cleaning
       ↓
TF-IDF
       ↓
Logistic Regression
       ↓
Sentiment Prediction


The model predicts whether a customer review is:

Positive
Neutral
Negative

Dataset Limitation

The sentiment labels are derived from star ratings rather than manually annotated review text. Therefore, some reviews may contain mixed or contradictory opinions even though their assigned sentiment is determined entirely by the rating.

🌐 Streamlit Application

The project includes an interactive Streamlit application with three sections:

1. 📊 Dashboard

Displays:

Revenue KPIs

Monthly revenue

Category revenue

City revenue

2. 🎯 Churn Prediction

Users can enter:

Total orders

Total spending

Average order value

Days since last order

Return rate

Average delivery days

Age

Membership type

The application returns:

Churn prediction

Churn probability

3. 💬 Sentiment Analysis

Users can enter a customer review and receive:

Predicted sentiment

Prediction confidence

⚙️ Installation

Clone the repository:

git clone https://github.com/arqamowais/Hackathon-DSAI-Batch-1.git


Navigate to the project:

cd Hackathon-DSAI-Batch-1


Install dependencies:

pip install -r requirements.txt

▶️ Run the Streamlit Application
streamlit run app.py


The application will open in your browser.

📓 Run the Notebook

Open:

Final_Hackathon.ipynb


using Jupyter Notebook, JupyterLab, or VS Code.

jupyter notebook

📦 Requirements

Example requirements.txt:

pandas
numpy
matplotlib
seaborn
scikit-learn
streamlit
joblib
tensorflow

👨‍💻 Author

Arqam Owais

GitHub:
https://github.com/arqamowais

📄 License

This project was developed as part of the Data Science & AI Hackathon – Batch 1.
