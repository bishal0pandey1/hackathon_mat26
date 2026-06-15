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

########################################################################################################


median_rework = customer_pricing_df[customer_pricing_df['Activity Type'] == 'Rework']['Contract Rate'].median()
customer_pricing_df['Contract Rate'] = customer_pricing_df['Contract Rate'].fillna(median_rework)


fig_box = px.box(
    customer_pricing_df,
    x='Activity Type',
    y='Contract Rate',
    color='Activity Type',
    title="<b>Contract Rate Distribution by Activity Type</b><br><sup>Shows pricing consistency across customers</sup>",
    points="all",             
    hover_data=['Customer Id']
)

fig_box.update_layout(
    height=600,
    width=950,
    showlegend=False,
    yaxis_title="Contract Rate ($)",
    xaxis_title="Activity Type",
    title_font=dict(size=18),
    boxmode='group'
)

st.plotly_chart(fig_box)

#####################################################################################################
fig_strip = px.strip(
    customer_pricing_df,
    x='Activity Type',
    y='Contract Rate',
    color='Activity Type',
    title="<b>Individual Customer Contract Rates by Activity</b>",
    hover_data=['Customer Id'],
    stripmode='overlay'
)

fig_strip.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_strip,use_container_width=True)
##########################################################################

avg_rate = customer_pricing_df.groupby('Activity Type')['Contract Rate'].mean().reset_index()

fig2 = px.bar(
    avg_rate,
    x='Activity Type',
    y='Contract Rate',
    color='Activity Type',
    title="<b>Average Contract Rate by Activity Type</b>",
    text=avg_rate['Contract Rate'].round(2)
)

fig2.update_traces(textposition='outside')
fig2.update_layout(
    height=550,
    showlegend=False,
    yaxis_title="Average Contract Rate ($)",
    title_font=dict(size=18)
)

st.plotly_chart(fig2,use_container_width=True)
###################################################################


# ==========================================
# Enhanced Pricing Variation Summary (with CV)
# ==========================================

summary = customer_pricing_df.groupby('Activity Type').agg(
    No_of_Customers=('Customer Id', 'nunique'),
    Min_Rate=('Contract Rate', 'min'),
    Max_Rate=('Contract Rate', 'max'),
    Median_Rate=('Contract Rate', 'median'),
    Mean_Rate=('Contract Rate', 'mean'),
    Std_Dev=('Contract Rate', 'std')
).reset_index()

# Calculate both types of variation
summary['Range'] = summary['Max_Rate'] - summary['Min_Rate']
summary['Variation_MaxMin_%'] = ((summary['Max_Rate'] - summary['Min_Rate']) / summary['Median_Rate'] * 100).round(1)
summary['CV_%'] = ((summary['Std_Dev'] / summary['Mean_Rate']) * 100).round(1)

# Clean column names
summary = summary.rename(columns={
    'Activity Type': 'Activity',
    'Min_Rate': 'Min ($)',
    'Max_Rate': 'Max ($)',
    'Median_Rate': 'Median ($)',
    'Mean_Rate': 'Mean ($)',
    'Std_Dev': 'Std Dev'
})

# Sort by CV (more statistical)
summary = summary.sort_values('CV_%', ascending=False).reset_index(drop=True)

# Round values
summary = summary.round(2)

st.write("=== PRICING VARIATION SUMMARY ===\n")
st.write(summary[['Activity', 'No_of_Customers', 'Min ($)', 'Max ($)', 'Median ($)', 'Variation_MaxMin_%', 'CV_%']])
#####################################################################################################################


# Pivot the data for heatmap
heatmap_data = customer_pricing_df.pivot(
    index='Customer Id', 
    columns='Activity Type', 
    values='Contract Rate'
)

# Create the heatmap
fig_heatmap = px.imshow(
    heatmap_data,
    color_continuous_scale='Viridis',        # Good options: 'Viridis', 'Plasma', 'Blues', 'RdYlGn'
    aspect="auto",
    title="<b>Contract Rates Heatmap</b><br><sup>All Customers (C001–C030) × All Activities</sup>",
    labels=dict(
        x="Activity Type", 
        y="Customer", 
        color="Contract Rate ($)"
    )
)

# Improve layout
fig_heatmap.update_layout(
    height=750,
    width=950,
    title_font=dict(size=18),
    xaxis_title="Activity Type",
    yaxis_title="Customer ID",
    coloraxis_colorbar=dict(
        title="Rate ($)",
        thickness=15,
        len=0.8
    )
)

# Add hover information
fig_heatmap.update_traces(
    hovertemplate="<b>Customer:</b> %{y}<br><b>Activity:</b> %{x}<br><b>Rate:</b> $%{z:.2f}<extra></extra>"
)

st.plotly_chart(fig_heatmap,use_container_width=True)
######################################################################################
st.write("COST ALLOCATIONl WHAT KEEPS WAREHOUSE OPEN")
cost_allocation_df_m1=cost_allocation_df[cost_allocation_df['Month']=='Month 1']
st.write(cost_allocation_df_m1)

###############################

import plotly.graph_objects as go

# Step 1: Re-create your exact cost allocation data frame
cost_data = {
    'Month': ['Month 1', 'Month 1', 'Month 1', 'Month 1', 'Month 1'],
    'Cost Category': ['Rent', 'Utilities', 'Equipment', 'Warehouse Management', 'Corporate Overhead'],
    'Monthly Cost': [52000, 12500, 18500, 34000, 28000],
    'Cost Type': ['Fixed', 'Semi-variable', 'Fixed', 'Fixed', 'Allocated']
}
cost_allocation_m1 = pd.DataFrame(cost_data)
total_cost = cost_allocation_m1['Monthly Cost'].sum()
# Step 2: Pivot data into a clean structural matrix & fill empty blocks with 0
cost_matrix = cost_allocation_m1.pivot(
    index='Cost Category', 
    columns='Cost Type', 
    values='Monthly Cost'
).fillna(0)

# Step 3: Chronologically order columns from most rigid to most flexible
desired_order = ['Fixed', 'Semi-variable', 'Allocated']
cost_matrix = cost_matrix[[col for col in desired_order if col in cost_matrix.columns]]

# Step 4: Generate a matrix heatmap with explicit cost values
fig_matrix = go.Figure(data=go.Heatmap(
    z=cost_matrix.values,
    x=cost_matrix.columns,
    y=cost_matrix.index,
    colorscale='YlOrRd',  # Warm corporate gradient
    text=[[f"${val:,.0f}" if val > 0 else "-" for val in row] for row in cost_matrix.values],
    texttemplate="<b>%{text}</b>",  # Forces bold numbers inside cells
    textfont=dict(size=14),
    showscale=False,  # Hides unnecessary colorbar to keep it clean
    hoverongaps=False
))

# Step 5: Executive Layout Formats
fig_matrix.update_layout(
    title=dict(
        text="<b>Cost Allocation Matrix: Baseline Operational Commitments</b><br><sup>Categorizing Month 1 Facility-Sustaining Expenses</sup>",
        font=dict(size=20)
    ),
    xaxis_title="<b>Cost Classification (Financial Behavior) ➔</b>",
    yaxis_title="<b>Operating Cost Category ➔</b>",
    height=500,
    margin=dict(t=80, b=50, l=180, r=40) # Generous left margin to fit long names
)

fig_matrix.add_annotation(
    xref="paper", yref="paper",
    x=1.0, y=1.12,  # Places it beautifully in the upper-right area
    text=f"<b>TOTAL MONTH 1 OVERHEAD</b><br><span style='font-size:18px; color:#c0392b;'><b>${total_cost:,.0f}</b></span>",
    showarrow=False,
    align="center",
    bordercolor="#bdc3c7",
    borderwidth=1,
    borderpad=6,
    bgcolor="#fdfefe"
)

st.plotly_chart(fig_matrix)
############################################
management_allocation_df_m1=management_allocation_df[management_allocation_df['Month']=='Month 1'].copy()
import plotly.express as px
import pandas as pd

# ==========================================
# Horizontal Bar Chart - All 30 Customers
# ==========================================

# Prepare and sort data
bar_data = management_allocation_df_m1[['Customer Id', 'Management Allocated Cost']].copy()
bar_data = bar_data.sort_values('Management Allocated Cost', ascending=True)  # ascending for horizontal chart

# Calculate total for title
total_mgmt_cost = bar_data['Management Allocated Cost'].sum()

# Create Horizontal Bar Chart
fig_management = px.bar(
    bar_data,
    x='Management Allocated Cost',
    y='Customer Id',
    orientation='h',
    title=f"<b>Management Cost Allocation by Customer (Month 1)</b><br><sup>Total Allocated Cost: ${total_mgmt_cost:,.2f}</sup>",
    text=bar_data['Management Allocated Cost'].round(0),   # Show values on bars
    color='Management Allocated Cost',
    color_continuous_scale='Viridis'
)

# Improve layout and text
fig_management.update_traces(
    textposition='outside',
    textfont=dict(size=10),
    hovertemplate="<b>Customer:</b> %{y}<br>Allocated Cost: $%{x:,.2f}<extra></extra>"
)

fig_management.update_layout(
    height=800,
    width=900,
    title_font=dict(size=18),
    xaxis_title="Management Allocated Cost ($)",
    yaxis_title="Customer ID",
    yaxis=dict(categoryorder='total ascending'),   # Ensures highest at top
    coloraxis_colorbar=dict(
        title="Allocated Cost ($)",
        thickness=15
    ),
    plot_bgcolor='black',
    paper_bgcolor='black'
)

st.plotly_chart(fig_management)
############################################

# Create crosstab
handling_pd = pd.crosstab(
    product_master_df['Handling Type'], 
    product_master_df['Product Size']
)

# Reorder for better visualization (optional but recommended)
size_order = ['Small', 'Medium', 'Large', 'Oversize']
handling_order = ['Standard', 'Ambient', 'Chilled', 'Fragile']

handling_pd = handling_pd.reindex(index=handling_order, columns=size_order)

# Create Heatmap
fig_product = px.imshow(
    handling_pd,
    text_auto=True,                          
    color_continuous_scale='Viridis',          # Or 'Viridis', 'Plasma', 'Greens'
    aspect="auto",
    title="<b>Product Mix: Handling Type vs Product Size</b><br><sup>Number of Products in Each Category</sup>"
)

fig_product.update_layout(
    height=550,
    width=750,
    title_font=dict(size=18),
    xaxis_title="Product Size",
    yaxis_title="Handling Type",
    coloraxis_colorbar=dict(
        title="Count of Products",
        thickness=15
    )
)

# Improve text inside heatmap
fig_product.update_traces(
    textfont=dict(size=14, color="black"),
    hovertemplate="<b>Handling Type:</b> %{y}<br><b>Product Size:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>"
)

st.plotly_chart(fig_product)
###########################################################################

customer_revenue_m1 = m1Revenue_df.groupby('Customer Id').agg(
    Total_Revenue=('Revenue', 'sum'),
    Total_Transactions=('Revenue', 'count')   # Optional: number of transaction lines
).reset_index()

# Sort by highest revenue
customer_revenue_m1 = customer_revenue_m1.sort_values('Total_Revenue', ascending=False).reset_index(drop=True)

# Calculate percentage of total revenue
total_revenue_m1 = customer_revenue_m1['Total_Revenue'].sum()
customer_revenue_m1['Revenue_Share_%'] = (customer_revenue_m1['Total_Revenue'] / total_revenue_m1 * 100).round(2)

fig_revenue = px.bar(
    customer_revenue_m1,
    x='Total_Revenue',
    y='Customer Id',
    orientation='h',
    title="<b>Total Revenue by Customer - Month 1</b>",
    text='Revenue_Share_%',                 
    color='Total_Revenue',
    color_continuous_scale='Viridis'
)

fig_revenue .update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    textfont=dict(size=9),
    hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.2f}<br>Share: %{text:.2f}%<extra></extra>"
)

fig_revenue .update_layout(
    height=800,
    width=950,
    title_font=dict(size=18),
    xaxis_title="Total Revenue ($)",
    yaxis_title="Customer ID",
    yaxis=dict(categoryorder='total ascending'),
    coloraxis_colorbar=dict(title="Total Revenue ($)"),
    plot_bgcolor='black'
)

st.plotly_chart(fig_revenue)
#####################################################################################################

import plotly.express as px
profitability_view = customer_revenue_m1[['Customer Id', 'Total_Revenue']].merge(
    management_allocation_df_m1[['Customer Id', 'Management Allocated Cost']],
    on='Customer Id',
    how='left'
)

fig_rm = px.scatter(
    profitability_view,
    x='Total_Revenue',
    y='Management Allocated Cost',
    hover_name='Customer Id',
    trendline='ols',                 
    title="<b>Current Method :Management Allocated Cost vs Customer Revenue</b><br><sup>Do higher revenue customers get higher cost allocation?</sup>",
    labels={
        'Total_Revenue': 'Total Revenue ($)',
        'Management Allocated Cost': 'Management Allocated Cost ($)'
    }
)

fig_rm.update_traces(
    marker=dict(size=10, color='#E63946'),
    hovertemplate="<b>%{hovertext}</b><br>Revenue: $%{x:,.2f}<br>Allocated Cost: $%{y:,.2f}<extra></extra>"
)

fig_rm.update_layout(
    height=600,
    width=850,
    title_font=dict(size=18),
    plot_bgcolor='black',
    paper_bgcolor='black'
)

st.plotly_chart(fig_rm)
#######################################################################################

def check_customer_date_completeness(df):
    customers = df['Customer Id'].unique()
    missing_info = {}

    for cust in customers:
        cust_df = df[df['Customer Id'] == cust]
        full_range = pd.date_range(start=cust_df['Date'].min(), 
                                   end=cust_df['Date'].max(), 
                                   freq='D')
        missing = full_range.difference(cust_df['Date'])
        
        if not missing.empty:
            missing_info[cust] = missing

    if missing_info:
        print("Customers with missing dates:")
        for cust, dates in missing_info.items():
            print(f"{cust}: {len(dates)} missing dates")
    else:
        print("All customers have complete daily data for Month 1 (no missing dates).")

    return missing_info

# Run the check
missing_dates = check_customer_date_completeness(m1Revenue_df)

# ==========================================
# Faceted Daily Revenue Trend - Black Theme
# ==========================================

fig_rtrend = px.area(
    m1Revenue_df,
    x='Date',
    y='Revenue',
    color='Customer Id',
    facet_col='Customer Id',
    facet_col_wrap=5,
    title="<b>Daily Revenue Trend by Customer - Month 1</b>",
    labels={'Revenue': 'Daily Revenue ($)'}
)

fig_rtrend.update_traces(
    hovertemplate="<b>%{x|%d %b}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
)

fig_rtrend.update_layout(
    height=4000,
    width=3000,
    title_font=dict(size=20, color='white'),
    showlegend=False,
    plot_bgcolor='black',          
    paper_bgcolor='black',          
    font=dict(color='white')        
)

# Grid Lines (lighter color for visibility on black)
fig_rtrend.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='#444444',           
    color='white'                   
)

fig_rtrend.update_yaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='#444444',
    color='white'
)

# Clean facet titles
fig_rtrend.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

st.plotly_chart(fig_rtrend)
##############################################################################



# ==========================================
# Prepare Weekly Data
# ==========================================

weekly_df = m1Revenue_df.copy()
weekly_df['Week'] = weekly_df['Date'].dt.to_period('W').astype(str)

weekly_revenue = weekly_df.groupby(['Customer Id', 'Week'])['Revenue'].sum().reset_index()
weekly_revenue = weekly_revenue.sort_values(['Customer Id', 'Week'])

# ==========================================
# Faceted Weekly Revenue Trend - Black Theme
# ==========================================

fig_weekly= px.area(
    weekly_revenue,
    x='Week',
    y='Revenue',
    color='Customer Id',
    facet_col='Customer Id',
    facet_col_wrap=5,
    title="<b>Weekly Revenue Trend by Customer - Month 1</b>",
    labels={'Revenue': 'Weekly Revenue ($)'}
)

fig_weekly.update_traces(
    hovertemplate="<b>Week:</b> %{x}<br>Revenue: $%{y:,.2f}<extra></extra>"
)

fig_weekly.update_layout(
    height=1600,
    width=1400,
    title_font=dict(size=20, color='white'),
    showlegend=False,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)

# Grid Lines
fig_weekly.update_xaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='#444444',
    color='white'
)

fig_weekly.update_yaxes(
    showgrid=True, 
    gridwidth=1, 
    gridcolor='#444444',
    color='white'
)

# Clean facet titles
fig_weekly.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

st.plotly_chart(fig_weekly)
###################################################################################


import plotly.graph_objects as go
from plotly.subplots import make_subplots

revenue_by_activity = (
    m1Revenue_df
    .groupby('Charge Type')
    .agg(
        Quantity=('Charged Quantity','sum'),
        Revenue=('Revenue','sum')
    )
    .reset_index()
)

revenue_by_activity['Revenue per Unit'] = (
    revenue_by_activity['Revenue']
    / revenue_by_activity['Quantity']
)

revenue_by_activity['Revenue %'] = (
    revenue_by_activity['Revenue']
    / revenue_by_activity['Revenue'].sum()
    * 100
)

revenue_by_activity.sort_values('Revenue', ascending=False)
# Sorting
df_qty = revenue_by_activity.sort_values(by='Quantity', ascending=False)
df_rev = revenue_by_activity.sort_values(by='Revenue', ascending=False)
df_rpu = revenue_by_activity.sort_values(by='Revenue per Unit', ascending=False)
df_pct = revenue_by_activity.sort_values(by='Revenue %', ascending=False)

# Dark theme dashboard
fig_b = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Operational Volume",
        "Total Revenue",
        "Revenue per Unit",
        "Revenue Contribution %"
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.08
)

# Helper function for hover
def hover_template(label):
    return label + ": %{y:,.2f}<extra></extra>"

# 1. Quantity
fig_b.add_trace(
    go.Bar(
        x=df_qty['Charge Type'],
        y=df_qty['Quantity'],
        marker=dict(
            color=df_qty['Quantity'],
            colorscale='Blues',
            line=dict(width=0.5, color='white')
        ),
        hovertemplate=hover_template("Quantity")
    ),
    row=1, col=1
)

# 2. Revenue
fig_b.add_trace(
    go.Bar(
        x=df_rev['Charge Type'],
        y=df_rev['Revenue'],
        marker=dict(
            color=df_rev['Revenue'],
            colorscale='Greens',
            line=dict(width=0.5, color='white')
        ),
        hovertemplate=hover_template("Revenue")
    ),
    row=1, col=2
)

# 3. Revenue per Unit
fig_b.add_trace(
    go.Bar(
        x=df_rpu['Charge Type'],
        y=df_rpu['Revenue per Unit'],
        marker=dict(
            color=df_rpu['Revenue per Unit'],
            colorscale='Plasma',
            line=dict(width=0.5, color='white')
        ),
        hovertemplate=hover_template("Rev/Unit")
    ),
    row=2, col=1
)

# 4. Revenue %
fig_b.add_trace(
    go.Bar(
        x=df_pct['Charge Type'],
        y=df_pct['Revenue %'],
        marker=dict(
            color=df_pct['Revenue %'],
            colorscale='Inferno',
            line=dict(width=0.5, color='white')
        ),
        hovertemplate=hover_template("Revenue %")
    ),
    row=2, col=2
)

# Layout (this is where it becomes "sexy")
fig_b.update_layout(
    title=dict(
        text="Activity Performance Dashboard (Volume vs Revenue vs Efficiency) for Month 1",
        x=0.5,
        xanchor='center',
        font=dict(size=22, color="white")
    ),
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white"),
    height=850,
    showlegend=False,
    transition=dict(duration=800)
)

fig_b.update_xaxes(tickangle=35, gridcolor="rgba(255,255,255,0.05)")
fig_b.update_yaxes(gridcolor="rgba(255,255,255,0.05)")

st.plotly_chart(fig_b)
###################################################################################################

m1Activities_df.drop('Data Quality Note',axis=1,inplace=True)

highest_vol_activity=m1Activities_df.groupby('Activity Type')['Quantity'].sum().reset_index().sort_values(ascending=False,by='Quantity')


fig_c = px.bar(
    highest_vol_activity.sort_values('Quantity', ascending=True),
    x='Quantity',
    y='Activity Type',
    orientation='h',
    title="<b>Total Quantity Processed by Activity Type - Month 1</b>",
    text='Quantity',
    color='Activity Type'
)

fig_c.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside',
    textfont=dict(size=12, color='black')
)

fig_c.update_layout(
    height=550,
    showlegend=False,
    xaxis_title="Total Quantity Processed",
    yaxis_title="Activity Type",
    plot_bgcolor='white'
)

st.plotly_chart(fig_c)
############################################################################################
m1Labour_df.drop('Data Quality Note',axis=1,inplace=True)
activity_labor_df = m1Labour_df.iloc[:217].copy()

activity_labor_df['hourly_rate'] = (
    activity_labor_df['Labour Cost'] / activity_labor_df['Labour Hours']
)
activity_labor_df['hourly_rate']=activity_labor_df['hourly_rate'].round(2)
activity_labor_df['hourly_rate'] = activity_labor_df['hourly_rate'].fillna(47.5)

activity_labor_df.loc[
    activity_labor_df['Labour Cost'].isna(),
    'Labour Cost'
] = (
    activity_labor_df['Labour Hours'] *
    activity_labor_df['hourly_rate']
)



# Data with your categorization
data = {
    'Activity Type': ['Storage', 'Dispatch', 'Receipt', 'Urgent Order', 'Returns', 'Rework', 'Pick'],
    'Total_Profit': [2284920.91, 177738.57, 67221.57, 80853.01, 49825.04, 20527.54, -155956.18],
    'Cost_per_Unit': [0.03, 2.53, 2.21, 5.93, 6.72, 9.89, 0.30],
    'Total_Revenue': [2293527.44, 524233.02, 196552.69, 135496.05, 164834.40, 135953.03, 142948.00],
    'Category': [
        'Core Value Creator', 
        'Value Creator', 
        'Stable Contributor', 
        'Premium but Costly', 
        'Value Eroder', 
        'Value Destroyer', 
        'Major Value Destroyer'
    ],
    'Color': ['#00C853', '#00C853', '#00C853', '#FFC107', '#FF9800', '#F44336', '#D32F2F']
}

df = pd.DataFrame(data)

# Create the scatter plot (Value Matrix)
fig_activity = px.scatter(
    df,
    x='Total_Profit',
    y='Cost_per_Unit',
    size='Total_Revenue',
    color='Category',
    color_discrete_map={
        'Core Value Creator': '#00C853',
        'Value Creator': '#00C853',
        'Stable Contributor': '#00C853',
        'Premium but Costly': '#FFC107',
        'Value Eroder': '#FF9800',
        'Value Destroyer': '#F44336',
        'Major Value Destroyer': '#D32F2F'
    },
    text='Activity Type',
    title="<b>Activities Value Matrix - Month 1</b><br><sup>X = Total Profit | Y = Cost per Unit (Lower is Better) | Size = Total Revenue</sup>",
    labels={
        'Total_Profit': 'Total Profit ($)',
        'Cost_per_Unit': 'Cost per Unit ($)'
    },
    size_max=70
)

fig_activity.update_traces(
    textposition='top center',
    textfont=dict(size=11, color='white'),
    marker=dict(
        line=dict(width=1.5, color='white'),
        opacity=0.9
    ),
    hovertemplate="<b>%{text}</b><br>" +
                  "Category: %{fullData.name}<br>" +
                  "Total Profit: $%{x:,.0f}<br>" +
                  "Cost per Unit: $%{y:.2f}<br>" +
                  "Total Revenue: $%{marker.size:,.0f}<extra></extra>"
)

fig_activity.update_layout(
    height=700,
    width=1000,
    title_font=dict(size=18, color='white'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#444444',
        zeroline=True,
        zerolinecolor='#888888',
        title_font=dict(color='white')
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#444444',
        zeroline=True,
        zerolinecolor='#888888',
        title_font=dict(color='white'),
        autorange='reversed'   # Lower cost per unit = better (higher on chart)
    ),
    legend=dict(
        title="Category",
        orientation="v",
        yanchor="middle",
        y=0.5,
        font=dict(size=11)
    )
)

st.plotly_chart(fig_activity)
##################################################################################################

import plotly.express as px

figPlr = px.bar(
    df.sort_values('Total_Profit', ascending=True),
    x='Total_Profit',
    y='Activity Type',
    orientation='h',
    title="<b>Total Profit by Activity Type</b>",
    text='Total_Profit',
    color='Total_Profit',
    color_continuous_scale=['#D32F2F', '#FFC107', '#00C853']
)

figPlr.update_traces(
    texttemplate='$%{text:,.0f}',
    textposition='outside',
    textfont=dict(size=11, color='white')
)

figPlr.update_layout(
    height=500,
    width=850,
    title_font=dict(size=18, color='white'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(showgrid=True, gridcolor='#444444'),
    yaxis_title="Activity Type",
    xaxis_title="Total Profit ($)",
    coloraxis_colorbar=dict(title="Profit ($)")
)

st.plotly_chart(figPlr)
#################################################################
import plotly.express as px

figRm = px.bar(
    df.sort_values('Cost_per_Unit', ascending=False),
    x='Cost_per_Unit',
    y='Activity Type',
    orientation='h',
    title="<b>Cost per Unit by Activity Type</b>",
    text='Cost_per_Unit',
    color='Cost_per_Unit',
    color_continuous_scale='Reds'
)

figRm.update_traces(
    texttemplate='$%{text:.2f}',
    textposition='outside',
    textfont=dict(size=11, color='white')
)

figRm.update_layout(
    height=500,
    width=850,
    title_font=dict(size=18, color='white'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(showgrid=True, gridcolor='#444444'),
    yaxis_title="Activity Type",
    xaxis_title="Cost per Unit ($)",
    coloraxis_colorbar=dict(title="Cost per Unit ($)")
)

st.plotly_chart(figRm)
#####################################################################################
activity_cost_baseline = activity_labor_df.groupby('Activity Type').agg(
    Total_Units_Processed=('Units Processed', 'sum'),
    Total_Labour_Hours=('Labour Hours', 'sum'),
    Total_Labour_Cost=('Labour Cost', 'sum')
).reset_index()
activity_cost_baseline['Cost_per_Unit'] = (
    activity_cost_baseline['Total_Labour_Cost'] /
    activity_cost_baseline['Total_Units_Processed']
)

customer_activity_df = m1Activities_df.copy()

customer_activity_df = customer_activity_df.groupby(
    ['Customer Id', 'Activity Type']
)['Quantity'].sum().reset_index()

customer_cost_df = customer_activity_df.merge(
    activity_cost_baseline[['Activity Type', 'Cost_per_Unit']],
    on='Activity Type',
    how='left'
)

customer_cost_df['Activity_Cost'] = (
    customer_cost_df['Quantity'] * customer_cost_df['Cost_per_Unit']
)

customer_total_cost = customer_cost_df.groupby('Customer Id').agg(
    Total_Cost_to_Serve=('Activity_Cost', 'sum')
).reset_index()


total_revenue_per_customer = m1Revenue_df.groupby('Customer Id')['Revenue'].sum().reset_index()
total_revenue_per_customer.columns = ['Customer Id', 'Total_Revenue']

customer_profit_df = total_revenue_per_customer.merge(
    customer_total_cost,
    on='Customer Id',
    how='left'
)
# Calculate average inventory metrics per customer
inventory_summary = m1Inventory_df.groupby('Customer Id').agg(
    Avg_Units_On_Hand = ('Units On Hand', 'mean'),
    Avg_Days_In_Stock = ('Avg Days In Stock', 'mean')
).reset_index()

# Create Space Usage metric
inventory_summary['Space_Usage'] = (
    inventory_summary['Avg_Units_On_Hand'] * inventory_summary['Avg_Days_In_Stock']
).round(2)

# Total Space Usage across all customers
total_space_usage = inventory_summary['Space_Usage'].sum()

# Calculate allocation percentage for each customer
inventory_summary['Space_Allocation_%'] = (
    (inventory_summary['Space_Usage'] / total_space_usage) * 100
).round(2)

# Allocate Rent + Equipment ($52,000 + $18,500 = $70,500)
rent_equipment_total = 70500
inventory_summary['Allocated_Space_Cost'] = (
    (inventory_summary['Space_Allocation_%'] / 100) * rent_equipment_total
).round(2)


# Get total quantity (activity volume) per customer from Activities data
activity_volume = m1Activities_df.groupby('Customer Id')['Quantity'].sum().reset_index()
activity_volume.columns = ['Customer Id', 'Total_Activity_Volume']

# Calculate allocation percentage
total_volume = activity_volume['Total_Activity_Volume'].sum()
activity_volume['Activity_Volume_Allocation_%'] = (
    (activity_volume['Total_Activity_Volume'] / total_volume) * 100
).round(2)

# Allocate Warehouse Management cost ($34,000) + utilities (12500)
warehouse_mgmt_total = 46500
activity_volume['Allocated_Warehouse_Mgmt_Cost'] = (
    (activity_volume['Activity_Volume_Allocation_%'] / 100) * warehouse_mgmt_total
).round(2)

# ==========================================
# Merge All Allocated Costs into Main DataFrame
# ==========================================

# main customer profitability data
customer_cost_df = customer_profit_df[['Customer Id', 'Total_Revenue', 'Total_Cost_to_Serve']].copy()

# Merge Allocated Space Cost (Rent + Equipment)
customer_cost_df = customer_cost_df.merge(
    inventory_summary[['Customer Id', 'Allocated_Space_Cost']],
    on='Customer Id',
    how='left'
)

# Merge Allocated Operations Cost (Utilities + Warehouse Management)
customer_cost_df = customer_cost_df.merge(
    activity_volume[['Customer Id', 'Allocated_Warehouse_Mgmt_Cost']],
    on='Customer Id',
    how='left'
)

# Update Total Cost to Serve (add both new allocated costs)
customer_cost_df['Final_Cost_to_Serve'] = (
    customer_cost_df['Total_Cost_to_Serve'] +
    customer_cost_df['Allocated_Space_Cost'] +
    customer_cost_df['Allocated_Warehouse_Mgmt_Cost']
).round(2)

customer_cost_df['True_Profit']=customer_cost_df['Total_Revenue']-customer_cost_df['Final_Cost_to_Serve']

customer_cost_df['Profit_Margin_%'] = (
    (customer_cost_df['True_Profit'] / customer_cost_df['Total_Revenue']) * 100
).round(2)

def margin_segment(margin):
    if margin < 40:
        return "Problem Customers (<40%)"
    elif 40 <= margin < 67:
        return "Average Customers (40–66%)"
    elif 67 <= margin <= 85:
        return "Strong Customers (67–85%)"
    else:
        return "Premium Customers (>85%)"

customer_cost_df['Margin_Segment'] = customer_cost_df['Profit_Margin_%'].apply(margin_segment)


fighr = px.treemap(
    customer_cost_df,
    path=[px.Constant("MONTH 1"), 'Margin_Segment', 'Customer Id'],
    values='Total_Revenue',   # FIX: prevents red squeezing
    color='Margin_Segment',

    color_discrete_map={
        "Premium Customers (>85%)": "#00E676",
        "Strong Customers (67–85%)": "#42A5F5",
        "Average Customers (40–66%)": "#FFB300",
        "Problem Customers (<40%)": "#EF5350"
    },

    hover_data={
        "True_Profit": ":,.2f",
        "Profit_Margin_%": ":.2f"
    },

    title="<b>Customer Segmentation – Month 1 Based on Profit_Margin %</b>"
)

#  CLEAN LOOK (no text inside tiles)
fighr.update_traces(
    textinfo="label",   # only customer id + segment, no numbers
    marker=dict(line=dict(width=2, color="black")),

    hovertemplate=
        "<b>Customer: %{label}</b><br><br>" +
        "True Profit: %{customdata[0]:,.2f}<br>" +
        "Profit Margin: %{customdata[1]:.2f}%<extra></extra>"
)

fighr.update_layout(
    height=850,
    width=1300,

    paper_bgcolor="black",
    plot_bgcolor="black",

    font=dict(color="white", size=13),

    title=dict(
        x=0.5,
        font=dict(size=22, color="white")
    ),

    margin=dict(t=80, l=10, r=10, b=10)
)

st.plotly_chart(fighr)
################################################################################

mean_cost = customer_cost_df['Final_Cost_to_Serve'].mean()
std_cost = customer_cost_df['Final_Cost_to_Serve'].std()

customer_cost_df['Cost_Z'] = (
    customer_cost_df['Final_Cost_to_Serve'] - mean_cost
) / std_cost

def segment(z):
    if z <= -0.5:
        return "Highly Efficient"
    elif z <= 1:
        return "Medium Cost"
    else:
        return "High Cost"
        
customer_cost_df['Cost_Segment'] = customer_cost_df['Cost_Z'].apply(segment)
import plotly.express as px

figik = px.treemap(
    customer_cost_df,
    path=[px.Constant("MONTH 1"), 'Cost_Segment', 'Customer Id'],
    values='Final_Cost_to_Serve',
    color='Cost_Segment',

    color_discrete_map={
        "Highly Efficient": "#43544C",          # green
        "Medium Cost": "#543D07",               # amber
        "High Cost ": "#9D0704"        # red
    },

    title="<b>Customer Cost-to-Serve</b><br><sup>Month 1 Operational Cost Pressure Map</sup>"
)

figik.update_traces(
    textinfo="label",
    marker=dict(line=dict(width=2, color="black")),
    
    hovertemplate=
        "<b>Customer: %{label}</b><br><br>" +
        "Cost to Serve: %{value:,.2f}<extra></extra>"
)

figik.update_layout(
    height=850,
    width=1300,

    paper_bgcolor="black",
    plot_bgcolor="black",

    font=dict(color="white", size=13),

    title=dict(
        x=0.5,
        font=dict(size=22, color="white")
    ),

    margin=dict(t=80, l=10, r=10, b=10)
)

st.plotly_chart(figik)
#####################################################################################################################

customer_activity_matrix = m1Activities_df.groupby(
    ['Customer Id', 'Activity Type']
)['Quantity'].sum().reset_index()

customer_activity_pivot = customer_activity_matrix.pivot(
    index='Customer Id',
    columns='Activity Type',
    values='Quantity'
).fillna(0)

data = {
    'Activity Type': ['Storage', 'Dispatch', 'Receipt', 'Urgent Order', 'Returns', 'Rework', 'Pick'],
    'Category': [
        'Core Value Creator', 
        'Value Creator', 
        'Stable Contributor', 
        'Premium but Costly', 
        'Value Eroder', 
        'Value Destroyer', 
        'Major Value Destroyer'
    ]
}
activity_map = dict(zip(
    data['Activity Type'],
    data['Category']
))
customer_category_profile = customer_activity_pivot.copy()

customer_category_profile.columns = customer_category_profile.columns.map(activity_map)



true_revenue_from_activity = m1Activities_df.merge(
    customer_pricing_df,
    on=['Customer Id', 'Activity Type'],
    how='left'
)

true_revenue_from_activity['True_Revenue'] = (
    true_revenue_from_activity['Quantity'] *
    true_revenue_from_activity['Contract Rate']
)

activity_revenue_true = true_revenue_from_activity.groupby(
    'Activity Type'
)[['True_Revenue','Quantity']].sum().reset_index()

activity_cost = activity_labor_df.groupby(
    'Activity Type'
)[['Labour Cost','Units Processed']].sum().reset_index()

activity_profit = activity_revenue_true.merge(
    activity_cost,
    on='Activity Type',
    how='inner'
)
activity_profit['Profit'] = (
    activity_profit['True_Revenue'] - activity_profit['Labour Cost']
)
activity_profit.sort_values('Profit', ascending=False)

activity_profit_df=activity_profit[['Activity Type','Units Processed','Profit']].copy()

activity_profit_df['Profit_per_Unit'] = (
    activity_profit_df['Profit'] / activity_profit_df['Units Processed']
)

profit_per_unit_map = dict(zip(
    activity_profit_df['Activity Type'],
    activity_profit_df['Profit_per_Unit']
))

customer_profit_impact = customer_activity_pivot.copy()

for activity in customer_profit_impact.columns:
    customer_profit_impact[activity] = (
        customer_profit_impact[activity] * profit_per_unit_map[activity]
    )
customer_profit_impact['Net_Activity_Profit_Impact'] = customer_profit_impact.sum(axis=1)

driver_summary = customer_profit_impact.drop(columns=['Net_Activity_Profit_Impact']).sum().sort_values()
st.write('Profitability Drivers')
st.write(driver_summary)
####################################################################
df_long = customer_profit_impact.drop(
    columns=['Net_Activity_Profit_Impact']
).reset_index().melt(
    id_vars='Customer Id',
    var_name='Activity',
    value_name='Profit Impact'
)



# prepare data (wide format)
df = customer_profit_impact.drop(columns=['Net_Activity_Profit_Impact'])

customers = df.index.tolist()
activities = df.columns.tolist()

# 6 rows × 5 cols = 30 customers
figijk = make_subplots(
    rows=6,
    cols=5,
    subplot_titles=customers
)

row = 1
col = 1

for i, cust in enumerate(customers):
    figijk.add_trace(
        go.Bar(
            x=activities,
            y=df.loc[cust],
            marker_color=df.loc[cust].apply(
                lambda x: "green" if x > 0 else "red"
            )
        ),
        row=row,
        col=col
    )

    col += 1
    if col > 5:
        col = 1
        row += 1

figijk.update_layout(
    title="Customer Profit Impact by Activity (All Customers)",
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white"),
    height=1400,
    width=2000,
    showlegend=False
)

st.plotly_chart(figijk)
###########################################################################