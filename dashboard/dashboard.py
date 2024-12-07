import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
/dashboard.py/__init__.py
# Load datasets
hour_df = pd.read_csv('/dashboard/hour.csv') 
day_df = pd.read_csv('/dashboard/day.csv')    
# Set up Streamlit layout
st.title("Bike Rentals Dashboard")
st.sidebar.header("Filters")

# Sidebar for selecting dataset type (Hourly or Daily)
dataset_type = st.sidebar.radio("Select Dataset Type", ['Hourly', 'Daily'])

# Filter data based on user selection
if dataset_type == 'Hourly':
    df = hour_df
else:
    df = day_df

# Display basic information about the selected dataset
st.write(f"Displaying dataset: {dataset_type} Data")
st.write(df.describe())

# Key Factor Visualizations
st.header("Key Factors Influencing Bike Rentals")

# Plot temperature vs bike rental count
st.subheader("Temperature vs Bike Rentals")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='temp', y='cnt', ax=ax)
ax.set_title('Temperature vs Bike Rentals')
ax.set_xlabel('Temperature')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Plot weather situation vs bike rental count
st.subheader("Weather Situation vs Bike Rentals")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='weathersit', y='cnt', ax=ax)
ax.set_title('Weather Situation vs Bike Rentals')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Plot casual vs registered rentals
st.subheader("Casual vs Registered Bike Rentals")
fig, ax = plt.subplots()
sns.kdeplot(df['casual'], label='Casual Users', shade=True)
sns.kdeplot(df['registered'], label='Registered Users', shade=True)
ax.set_title('Casual vs Registered Bike Rentals')
ax.set_xlabel('Number of Rentals')
ax.set_ylabel('Density')
ax.legend()
st.pyplot(fig)

# Bike Usage Patterns
st.header("Bike Usage Patterns")


st.subheader("Peak Hour Rentals")
if 'hr' in df.columns:
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='hr', y='cnt', ax=ax)
    ax.set_title('Bike Rentals by Hour of the Day')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Bike Rentals')
    st.pyplot(fig)
else:
    st.write("This visualization is not applicable for the Daily dataset.")

# Season-wise Bike Rentals
st.subheader("Bike Rentals by Season")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='season', y='cnt', ax=ax)
ax.set_title('Bike Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Working Day vs Holiday Rentals
st.subheader("Bike Rentals on Working Day vs Holiday")
fig, ax = plt.subplots()
sns.boxplot(data=df, x='workingday', y='cnt', ax=ax)
ax.set_title('Bike Rentals: Working Day vs Holiday')
ax.set_xlabel('Working Day (1: Yes, 0: No)')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)



# Display insights based on analysis
st.header("Insights from Analysis")
st.write("""
1. **Key Factors Influencing Bike Rentals**:
   - The **temperature** is a key factor influencing bike rentals. As temperatures rise, bike rentals tend to increase, which indicates a preference for outdoor activities when the weather is warm.
   - **Bad weather** significantly affects bike rental counts, as people tend to avoid outdoor activities during unfavorable weather conditions.
   - **Casual users** (informal renters) rent bikes more frequently than registered users, likely due to spontaneous use.
   
2. **Bike Usage Patterns**:
   - The highest bike rental activity is observed during **morning** and **afternoon** hours. This is likely due to commuting needs during these peak times.
   - The **Fall season** sees the highest bike rentals, likely due to its temperate weather and outdoor activity appeal.
   - **Weekdays** (Monday to Saturday) have the highest bike rental counts, as bike usage decreases on Sundays.

These insights can help in understanding the factors that influence bike rental patterns, allowing businesses to optimize bike availability and marketing strategies.
""")

