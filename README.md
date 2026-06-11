# Airline Loyalty Behavioral Intelligence Framework

## Overview

This project was developed as part of an airline loyalty analytics challenge focused on understanding customer disengagement, identifying high-value customer segments, and designing targeted retention strategies.

Traditional loyalty programs often rely on historical metrics such as Customer Lifetime Value (CLV), points balances, and cancellation records to evaluate customer health. However, these indicators frequently fail to capture early signs of behavioral disengagement, resulting in missed retention opportunities and hidden revenue risk.

This project combines customer behavior analysis, churn prediction, customer segmentation, and business-focused retention recommendations to provide a more proactive approach to loyalty program management.

---

## Project Objectives

The project addresses three key business questions:

### 1. Churn Prediction
Identify loyalty members who are at risk of disengaging from the airline program before customer value is lost.

### 2. Customer Segmentation
Group members into meaningful behavioral segments based on travel activity, engagement patterns, and loyalty behavior.

### 3. Retention Strategy
Develop targeted interventions that align with the needs and behaviors of different customer groups.

---

## Methodology

The analytical workflow includes:

- Data cleaning and preprocessing
- Customer behavior feature engineering
- Churn definition using cancellation and inactivity signals
- Predictive modeling for churn risk estimation
- Behavioral customer segmentation
- Business insight generation
- Retention strategy design
- Interactive dashboard development

---

## Key Insights

Some of the major findings from the analysis include:

- Customer disengagement is often behavioral rather than administrative.
- High historical customer value does not necessarily imply low churn risk.
- Behavioral indicators outperform demographic attributes when predicting future disengagement.
- Distinct customer segments exhibit different retention needs and risk profiles.
- Targeted retention actions are more effective than broad, one-size-fits-all campaigns.

---

## Deliverables

### Technical Report
A business-focused report summarizing:

- Problem framing
- Data preparation decisions
- Modeling approach
- Customer segmentation logic
- Key findings
- Strategic recommendations

### Interactive Dashboard
A Streamlit-based dashboard designed to:

- Monitor churn risk
- Explore customer segments
- Identify priority customers
- Support retention decision-making

---

## Repository Structure

```text
├── notebooks/
│   └── analysis.ipynb
│
├── data/
│   └── processed datasets
│
├── dashboard/
│   └── streamlit application
│
├── reports/
│   └── technical report
│
└── README.md
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- Matplotlib
- Plotly
- Streamlit
