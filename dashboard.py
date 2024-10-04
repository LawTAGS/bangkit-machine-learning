import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

tab = ["Peak hour(s)", "Regular vs. Casual Customers"]

file = './Bike-sharing-dataset/hour.csv'
df = pd.read_csv(file)

st.title("Bike Sharing Data Analysis")

st.header("Introduction to Bike Sharing")
st.markdown(
    """
    <div style="text-align: justify;">
    Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic.
    Through these systems, user is able to easily rent a bike from a particular position and return back at another position.
    </div>
    """, unsafe_allow_html=True
)



st.header("Data Analysis")
st.subheader("Purpose of Analysing Bike Sharing Data")
st.markdown(
    """
    <div style="text-align: justify;">
    By analyzing the dataset of the bike-sharing systems, we can determine the peak hours and compare casual users to registered users.
    This analysis can be used to provide better services and increase engagement.
    </div>
    """, unsafe_allow_html=True
)

st.subheader("Data Visualization")
st.markdown(
    """
    <div style="text-align: justify;">
    The data on peak usage hours and comparison between casual and registered users are visualized below
    </div>
    """, unsafe_allow_html=True
)

tabs = st.tabs(tab)

with tabs[0]:
    # Pertanyaan 1
    colors = ["#D3D3D3"] * 13 + ["#72BCD4"] * 5 + ["#D3D3D3"] * 6

    plt.figure(figsize=(12, 6))
    hist = sns.histplot(df['hr'], bins=24)

    for bar, color in zip(hist.patches, colors):
        bar.set_facecolor(color)
        
    plt.title('Distribution of Bike Sharing Usage Frequency per Hour')
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    st.write(
        """
        The distribution above shows that the peak hour of bike sharing usage are from 01.00 PM to 05.00 PM.
        """
    )

with tabs[1]:
    # Pertanyaan 2
    casual_yr1 = []
    registered_yr1 = []
    casual_yr2 = []
    registered_yr2 = []

    df_unique_month = df['mnth'].unique()

    for i in df_unique_month:
        df_month_filter = df[df['mnth'] == i]

        df_year_0 = df_month_filter[df_month_filter['yr'] == 0]
        df_year_1 = df_month_filter[df_month_filter['yr'] == 1]

        if not df_year_0.empty:
            casual_yr1.append(df_year_0['casual'].sum())
            registered_yr1.append(df_year_0['registered'].sum())

        if not df_year_1.empty:
            casual_yr2.append(df_year_1['casual'].sum())
            registered_yr2.append(df_year_1['registered'].sum())

    data_yr1 = pd.DataFrame({
        'Month': df_unique_month,
        'Casual': casual_yr1,
        'Registered': registered_yr1
    })

    data_yr2 = pd.DataFrame({
        'Month': df_unique_month,
        'Casual': casual_yr2,
        'Registered': registered_yr2
    })

    data_yr1_melted = pd.melt(data_yr1, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')
    data_yr2_melted = pd.melt(data_yr2, id_vars='Month', value_vars=['Casual', 'Registered'], var_name='User_Type', value_name='User_Count')

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Month', y='User_Count', hue='User_Type',
                data=data_yr1_melted, palette=['#ADD8E6', '#FFE4B5'],
                errorbar=None, dodge=True)

    bars = plt.gca().patches
    bars[0].set_facecolor('blue')
    bars[12].set_facecolor('orange')
    bars[5].set_facecolor('blue')
    bars[17].set_facecolor('orange') 

    plt.title('Distribution of Users Type per Month (Year 1)')
    plt.xlabel('Month')
    plt.ylabel('Total Users')
    plt.legend()
    st.pyplot(plt)

    st.write(
        """
        The distribution above shows that the highest difference between casual and registered users in the first year occurs in the sixth month, while the lowest difference occurs in the first month.
        """
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Month', y='User_Count', hue='User_Type',
                data=data_yr2_melted, palette=['#ADD8E6', '#FFE4B5'],
                errorbar=None, dodge=True)

    bars = plt.gca().patches
    bars[0].set_facecolor('blue')
    bars[12].set_facecolor('orange')
    bars[8].set_facecolor('blue')
    bars[20].set_facecolor('orange') 

    plt.title('Distribution of Users Type per Month (Year 2)')
    plt.xlabel('Month')
    plt.ylabel('Total Users')
    plt.legend()
    st.pyplot(plt)

    st.write(
        """
        The distribution above shows that the highest difference between casual and registered users in the first year occurs in the ninth month, while the lowest difference occurs in the first month.
        """
    )

st.header("Conclusions and Suggestions")
st.subheader("Conclusions")
st.markdown(
    """
    - The peak usage time for the Bike Sharing system is around 1:00 PM to 5:00 PM, with the number of users exceeding 700.
    - The comparison of the number of casual users to registered users in the first year shows the largest difference in the sixth month of the first year and the ninth month of the second year.
    Meanwhile, the difference in the number of casual users to those who have already registered is observed in the first month of both the first and second years.
    """
)

st.subheader("Suggestions")
st.markdown(
    """
    - Increase Availability During Peak Hours:
    To enhance user satisfaction, it is recommended to increase the availability of bikes during peak hours (1:00 PM to 5:00 PM). This could include deploying additional bikes or ensuring maintenance is scheduled outside of peak usage times.

    - Targeted Marketing Campaigns:
    Implement targeted marketing strategies aimed at casual users, especially during months where the disparity between user types is greatest. Promotional offers or incentives for signing up during these months could help convert casual users into registered users.

    - Engagement Initiatives:
    Develop engagement initiatives to encourage casual users to register, such as loyalty programs or referral discounts. Highlighting the benefits of being a registered user may motivate more casual users to sign up.

    - Seasonal Promotions:
    Consider implementing seasonal promotions or events to attract more users during the identified peak usage months. This could involve partnerships with local businesses or community events that encourage bike-sharing as a convenient transport option.
    """
)