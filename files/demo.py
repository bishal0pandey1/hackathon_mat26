import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st 

### MONTH 1 

m1Revenue_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='M1 Revenue')
m1Activities_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='M1 Activities')
m1Labour_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='M1 Labour')
m1Exceptions_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='M1 Exceptions')
m1Inventory_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='M1 Inventory')

# warehouse customer, pricing , product data

customer_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Customer Master')
pricing_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Standard Pricing')
customer_pricing_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Customer Pricing')

cost_allocation_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Cost Allocation')
management_allocation_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Management Allocation Cost')
product_master_df=pd.read_excel('../Datasets/warehouse_dataset.xlsx',sheet_name='Product Master')

################################################################################################################################

#know your customers
customer_df=customer_df.astype('object')

import streamlit as st
import plotly.express as px
import pandas as pd

# Page setup
st.set_page_config(page_title="Customer Portfolio Dashboard", layout="wide")
st.title("📊 Customer Portfolio Analysis")

# ==========================================
# 1. COLOR MAPPING (Keep your custom colors)
# ==========================================
archetype_colors = {
    "Stable Performer": "#2ecc71",
    "Strategic Account": "#27ae60",
    "Margin Expansion Opportunity": "#a3e4d7",
    "Scale Without Return": "#f39c12",
    "Activity Intensive": "#e67e22",
    "Operational Complexity": "#d35400",
    "Service Intensive": "#884ea0",
    "Underutilised Account": "#3498db",
    "Storage Intensive": "#2980b9",
    "Space Inefficient": "#5d6d7e",
    "Revenue Leakage": "#e74c3c",
    "Fixed Fee Risk": "#c0392b",
    "Seasonal Volatility": "#9b59b6"
}

# ==========================================
# 2. INDUSTRY PIE CHART
# ==========================================
industry_counts = customer_df['Industry'].value_counts().reset_index(name='Count')

fig_pie = px.pie(
    industry_counts, 
    values='Count', 
    names='Industry', 
    title='<b>Customer Portfolio Mix by Industry</b>',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_pie.update_traces(textinfo='percent+label')

st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# 3. CONTRACT TYPE BAR CHART
# ==========================================
contract_counts = customer_df['Contract Type'].value_counts().reset_index(name='Count')

fig_bar = px.bar(
    contract_counts, 
    x='Contract Type', 
    y='Count', 
    title='<b>Analysis of Active Contract Types</b>',
    color='Contract Type',
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig_bar.update_layout(showlegend=False)

st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# 4. ARCHETYPE BUBBLE CHART (Fixed - No Error)
# ==========================================
archetype_counts = customer_df['Internal Archetype'].value_counts().reset_index(name='Count')

fig_bubble = px.scatter(
    archetype_counts, 
    x='Internal Archetype', 
    y='Count',
    size='Count', 
    color='Internal Archetype',
    color_discrete_sequence=px.colors.qualitative.Bold,   # ← Changed to avoid error
    title='<b>Management Archetype Concentration</b>',
    size_max=50
)
fig_bubble.update_layout(height=550, xaxis_tickangle=45, showlegend=False)

st.plotly_chart(fig_bubble, use_container_width=True)

# ==========================================
# 5. TREEMAP
# ==========================================
treemap_data = (
    customer_df.groupby(['Industry', 'Contract Type', 'Internal Archetype'])
    .size()
    .reset_index(name='Count')
)

fig_tree = px.treemap(
    treemap_data,
    path=['Industry', 'Contract Type', 'Internal Archetype'],
    values='Count',
    color='Industry',
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="<b>Customer Portfolio Structural Breakdown</b>"
)

fig_tree.update_traces(textinfo="label+value+percent parent")
fig_tree.update_layout(height=650)

st.plotly_chart(fig_tree, use_container_width=True)