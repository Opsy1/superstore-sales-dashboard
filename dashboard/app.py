import streamlit as st
import pandas as pd
import plotly.express as px



# Custom CSS for dark theme
st.markdown(
    """
    <style>
   
    /* Main background and text */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    /* Sidebar background and text */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #262730 0%, #1a1c24 100%);
        color: #ab63fa;
    }
     [data-testid="stSidebar"] * {
        color: #ab63fa;
    }
    /* Header background */
    header[data-testid="stHeader"] {
        background-color: #0e1117;
    }
    /* === KPI Styling === */
    .stMetric {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #3d3d3d;
       
    }
    .stMetric label {
        color: #fafafa;
        
   }
    .stMetric [data-testid="stMetricValue"] {
        color: #ab63fa;
        font-weight: bold;
    }
    .stDownloadButton > button {
        background-color: #4CAF50; 
        color: white;
        border-radius: 8px; 
    }
     /* === Chart Styling === */
    .stPlotlyChart {
        border: 2px solid #3d3d3d;
        border-radius: 12px;
        overflow: hidden;
        background-color: #262730;
    }
    
   

    
    </style>
    """,
    unsafe_allow_html=True
)

def style_chart(fig, bg_color="#262730", text_color="#fafafa"):
    """Apply consistent dark theme to any Plotly figure"""
    fig.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, size=14),
        title_font=dict(color=text_color, size=16),
        xaxis=dict(
            title_font=dict(color=text_color, size=14),
            gridcolor="#3d3d3d",
            linecolor="#3d3d3d",
            tickfont=dict(color=text_color)
        ),
        yaxis=dict(
            title_font=dict(color=text_color, size=14),
            gridcolor="#3d3d3d",
            linecolor="#3d3d3d",
            tickfont=dict(color=text_color)
        ),
        
        legend=dict(
            font=dict(color=text_color, size=12)
        )
    )
    return fig


df = pd.read_csv('data/superstore.csv')
df.head()
# Remove duplicates
df = df.drop_duplicates()

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=True)
# Create Month column
df['Month'] = df['Order Date'].dt.month_name()
# Create Year column
df['Year'] = df['Order Date'].dt.year


# Total Sales
df['Total Sales'] = df['Sales'].sum()
# Total Profit
df['Total_Profit'] = df['Profit'].sum()
# Average Sales
df['Avg_Sales'] = df['Sales'].mean()



# 1. SETUP (Data settings)

st.set_page_config(page_title='Superstore Sales Dashboard', layout='wide', page_icon='🏪')



# Sidebar Menu
st.sidebar.title('Dashboard Menu')
dashboard_menu= st.sidebar.radio(
    'Select Dashboard',
    ['Sales Overview', 'Profit Analysis', 'Customer & Geographical Analysis', 'Business Insights']
    
)

st.sidebar.divider()

#Sidebar Year Filter
select_year = ['All'] + list(df['Year'].sort_values(ascending=True).unique( ))
year = st.sidebar.selectbox(
    'Year',
    select_year
    
    
)

# Sidebar Region Filter
select_region = ['All'] + list(df['Region'].unique())
region = st.sidebar.selectbox(
    'Region',
    select_region,
    
)
if year == 'All' and region == 'All':
    filtered_df = df
elif year == 'All' and region != 'All':
    filtered_df = df[(df['Region'] == region)]
elif year != 'All' and region == 'All':
    filtered_df = df[df['Year'] == year]
else:
    filtered_df = df[(df['Region'] == region) & (df['Year'] == year)]

# === Image at the bottom of the sidebar ===
st.sidebar.divider()
st.sidebar.image(
    "hieliteLogo.png",
    use_container_width=True,
    caption="Opeyemi Fayemi - Data Analyst Trainee | Hielite Academy",
    output_format="PNG"
)

# Dashboard Header and Download Button
dashboard_title_col1, download_button_col2 = st.columns([5,1])
with dashboard_title_col1:
    st.title('Superstore Sales Performance Dashboard (2011-2014)') 
with download_button_col2:
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="sales_data.csv",
        mime="text/csv",
        width='stretch'
        
) 
#st.divider()

if dashboard_menu == 'Sales Overview':
    st.header('Sales Overview Dashboard')
    
    
    # KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    Avg_Sales = df['Sales'].mean()
    Total_Quantity = df['Quantity'].sum()
    Profit_Margin = total_profit / total_sales * 100

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric('Total Sales', f"${total_sales:,.2f}")
    col2.metric('Total Profit', f"${total_profit:,.2f}")
    col3.metric('Average Sales', f"${Avg_Sales:,.2f}")
    col4.metric('Total Quantity Sold', f"{Total_Quantity:,}")
    col5.metric('Profit Margin', f"{Profit_Margin:.2f}%")
    
    



# Chart: Sales Overview

    col1, col2 = st.columns(2)
    # 1. Total Sales by Region
    with col1:
       
        sales_by_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig1 = px.bar(
            sales_by_region,
            x='Region',
            y='Sales',
            color='Region',
            title='Total Sales by Region',
            
        )
        
        fig1 = style_chart(fig1)
        st.plotly_chart(fig1)

    # 2. Total Sales by Category
    with col2:
        #st.subheader('Sales by Category')
        sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig2 = px.pie(
            sales_by_category,
            values='Sales',
            names='Category',
            hole=0.5,
            title='Sales Contribution by Category'
        )
        fig2.update_traces(textinfo='value+percent', textposition='outside', texttemplate='$%{value:,.2f}<br>%{percent:.1%}')
        fig2 = style_chart(fig2)
        st.plotly_chart(fig2)
    #st.divider()

    # 3. Monthly Sales Trend
    monthly_sales_col1, top_10_products_col2 = st.columns(2)
    with monthly_sales_col1:
        df['MonthNum'] = filtered_df['Order Date'].dt.month
        monthly_sales = df.groupby(['MonthNum', 'Month'])['Sales'].sum().reset_index()
        monthly_sales = monthly_sales.sort_values('MonthNum')

        fig3 = px.line(
            monthly_sales,
            x='Month',
            y='Sales',
            title='Monthly Sales Trend',
            markers=True
            
        )
        fig3 = style_chart(fig3)
        st.plotly_chart(fig3)
    

    

    
    # 4. Top 10 Products by Sales
    with top_10_products_col2:
        #st.subheader('Top 10 Products by Sales')
        top_10_products = filtered_df.groupby('Product Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=True).tail(10)
        # The Magic Line: Cut names at 25 characters and add "..."
        top_10_products['Short Name'] = top_10_products['Product Name'].apply(lambda x: x[:25] + '...' if len(x) > 25 else x)
        fig4 = px.bar(
            top_10_products,
            x='Sales',
            y='Short Name',
            color='Sales',
            color_continuous_scale=['#43325d', '#a78bfa'],
            title='Top 10 Products by Sales'
            

        )
        fig4.update_layout(coloraxis_showscale=False, showlegend=False, coloraxis_reversescale=True)
        
        fig4 = style_chart(fig4)
        st.plotly_chart(fig4)

    sales_by_subcategory_col1, year_over_year_col2 = st.columns(2)
    # 5. Sales by Sub-Category
    with sales_by_subcategory_col1:
        #st.subheader('Sales by Sub-Category')
        sales_by_subcategory = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)    
        fig5 = px.bar(
            sales_by_subcategory,
            x='Sub-Category',
            y='Sales',
            color='Sales',
            color_continuous_scale=['#43325d', '#a78bfa'],
            title='Sales by Sub-Category'           
        )
        fig5.update_layout(coloraxis_showscale=False, showlegend=False, coloraxis_reversescale=True)
        fig5 = style_chart(fig5)
        st.plotly_chart(fig5)
    

    with year_over_year_col2:
        # 6. Year-over-Year Sales Forecast  
        # Get last two years
        years = sorted(df['Year'].unique())[-2:]
        prev_year, curr_year = years

        # Monthly sales for both years
        df['MonthNum'] = df['Order Date'].dt.month

        prev_sales = df[df['Year'] == prev_year].groupby('MonthNum')['Sales'].sum()
        curr_sales = df[df['Year'] == curr_year].groupby('MonthNum')['Sales'].sum()

        # Simple forecast (average growth applied)
        growth = (curr_sales.sum() / prev_sales.sum() - 1) if prev_sales.sum() > 0 else 0
        forecast = curr_sales * (1 + growth)

        # Combine data
        chart_df = pd.DataFrame({
            'Month': list(range(1, 13)),
            str(prev_year): prev_sales.reindex(range(1, 13), fill_value=0).values,
            str(curr_year): curr_sales.reindex(range(1, 13), fill_value=0).values,
            'Forecast': forecast.reindex(range(1, 13), fill_value=0).values
        })

        # Create chart
        fig6 = px.line(
            chart_df.melt(id_vars='Month', var_name='Type', value_name='Sales'),
            x='Month', y='Sales', color='Type',
            title="Year-over-Year Sales Forecast",
            markers=True,
            
        )
        fig6 = style_chart(fig6)
        st.plotly_chart(fig6)

# Chart: Profit Analysis
elif dashboard_menu == 'Profit Analysis':
    st.header('Profit Analysis Dashboard')
    
    #st.divider()
    profit_rgion_col1, profit_margin_region_col2 = st.columns(2)
# 7. Profit by Region
    with profit_rgion_col1:
        #st.subheader('Profit by Region')
        Profit_by_region = filtered_df.groupby('Region')['Profit'].sum().reset_index()
        fig7 = px.bar(
            Profit_by_region,
            x='Region',
            y='Profit',
            title='Total Profit by Region',
            color_discrete_sequence=['#ab63fa'] 
        )
        fig7.update_layout(coloraxis_showscale=False, showlegend=False)
        fig7 = style_chart(fig7)
        st.plotly_chart(fig7)

    # 8. Profit Margin by Region
    with profit_margin_region_col2:
        #st.subheader('Profit Margin by Region')
        profit_margin = filtered_df.groupby('Region').apply(lambda x: x['Profit'].sum() / x['Sales'].sum() * 100).reset_index(name='Profit Margin'  )
        fig8 = px.pie(
            profit_margin,
            values='Profit Margin',
            names='Region',
            color='Region',
            hole=0.5,
            title='Profit Margin by Region'
        )
        fig8 = style_chart(fig8)
        st.plotly_chart(fig8)

    

    profit_by_year_col1, top_10_city_by_profit_col2 = st.columns(2)    
    with profit_by_year_col1:
    # 9. Profit by Year
        #st.subheader('Profit by Year')
        Profit_by_year = filtered_df.groupby('Year')['Profit'].sum().reset_index().sort_values('Year')
        fig9 = px.area(
            Profit_by_year,
            x='Year',
            y='Profit',
            title='Profit Trend by Year',
            markers=True,
            color_discrete_sequence=['#ab63fa'] 

        )
        fig9 = style_chart(fig9)
        fig9.update_xaxes(type='category') 
        st.plotly_chart(fig9)

    with top_10_city_by_profit_col2:
    # 10. Top 10 city by Profit
        #st.subheader('Top 10 City Performance by Profit')
        top_10_city_by_profit = filtered_df.groupby('City',as_index=False)['Profit'].sum().reset_index().sort_values('Profit', ascending=False).head(10)
        fig10 = px.bar(
            top_10_city_by_profit,
            x='City',
            y='Profit',
            title='Top 10 Cities by Profit',
            color_discrete_sequence=['#ab63fa'] 
        )
        fig10.update_layout(showlegend=False)
        fig10 = style_chart(fig10)
        st.plotly_chart(fig10)
    

# Chart: Customer & Geographical Analysis
elif dashboard_menu == 'Customer & Geographical Analysis':
    
    st.header('Customer & Geographical Analysis Dashboard')
    st.divider()
    customer_segment_col1, sales_by_state_col2 = st.columns(2)
    #11. Sales by Customer Segment
    with customer_segment_col1:
        #st.subheader('Sales by Customer Segment')
        sales_by_customer_segment = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        fig11 = px.bar(
            sales_by_customer_segment,
            x='Segment',
            y='Sales',
            color='Segment',
            title='Sales by Customer Segment'
        )
        fig11.update_layout(showlegend=False)
        fig11 = style_chart(fig11)
        st.plotly_chart(fig11)

    #12. Sales by State
    with sales_by_state_col2:
        #st.subheader('Sales Contribution by State')
        sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
        fig12 = px.choropleth(
            sales_by_state,
            locations='State',
            locationmode='USA-states',
            color='Sales',
            scope='usa',
            color_continuous_scale='Purples',
            title='Sales by State'
            
        )
        
        fig12 = style_chart(fig12)
        st.plotly_chart(fig12)

    
    
    salesProfit_by_segment_col1, top_10_customers_col2 = st.columns(2)
    #13. Segment Profitability Matrix
    with salesProfit_by_segment_col1:
       
        summary = df.groupby('Segment').sum(numeric_only=True).reset_index()

        # Melt data to make it compatible with Plotly group bars
        melted_df = summary.melt(id_vars=['Segment'], value_vars=['Sales', 'Profit'], 
                                var_name='Metric', value_name='Amount')

        
        fig13 = px.bar(
            melted_df,
            title='Segment Profitability: Sales vs Profit Breakdown', 
            x='Segment', 
            y='Amount', 
            color='Metric', 
            barmode='group',
            color_discrete_map={'Sales': '#ab63fa', 'Profit': '#00cc96'}
        )
        fig13 = style_chart(fig13)

        st.plotly_chart(fig13)

    

    #14. Top 10 Customers by Sales
    with top_10_customers_col2:
        
        top_10_customers = filtered_df.groupby('Customer Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=True).tail(10)
        fig14 = px.bar(
            top_10_customers,
            x='Sales',
            y='Customer Name',
            color='Sales',
            color_continuous_scale=['#a78bfa', '#43325d'],
            title='Top 10 Customers by Sales'
        )
        fig14.update_layout(coloraxis_showscale=False, showlegend=False)
       
        fig14 = style_chart(fig14)
        st.plotly_chart(fig14)

    

# Business Insights
elif dashboard_menu == 'Business Insights':
    st.header('Key Business Insights')

    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        
    
                    
        st.markdown('#### Sales and Profit Performance')
        st.write("""
        * The West region shows the highest sales, follow by the East Region. The Central and South region also perform above the average of West and East region. This shows if marketing and inventory are expanded in Central and South region, both will also perform better.
        * The West region has the highest sales and profit margin, indicating efficient operations and pricing strategies. Unlike Central region which have high sales than the South region but have low profit margin compared to South region. This could be as a result of high discount and logistics.
        * New York City shows the highest performing city with over 50% more than other cities in the top 10 cities by profit.
        * Monthly sales trend shows a growth in sales from January to December each year and for cumulative year. There is 20% growth in sales in year 2014 which was used as a basic for sales forecast in year 2015.
            
            **What to focus on:**
            * Focus on the top-performing region for aggressive growth.
            * High-profit cities should receive more marketing and inventory support but focus should be on other cities leaving New York City.
            * Reduce discounts and logistics in low-profit regions to improve margins.
            * Expand operations in high-profit states identified on the map.

            
        """)
        

    with col2:
        
        st.markdown("### Product & Category Insights")
        st.write("""
        * All the product category performs well in the years reviewed as the percentage contributed are closed to each other.
        
            **What to focus on:**
            * Protect and promote the Top 10 products as they drive significant revenue.
            * Expand high-performing sub-categories and review low-performing ones.

        """)

        
        st.markdown("### Customer & Segment Strategy")
        st.write("""
        * Consumer segment shows highest sales and profit compared to corporate segment and home office.
            
            **What to focus on:**
            * Prioritize the most profitable customer segment for targeted campaigns.
            * Ensure customers loyalty program in other to retain active customers.
            * Review segments with high sales but low profit margins.
            * Use the Sales vs Profit chart to identify and optimize underperforming products.

        """)

        st.markdown('<div class="insights-text">', unsafe_allow_html=True)      



