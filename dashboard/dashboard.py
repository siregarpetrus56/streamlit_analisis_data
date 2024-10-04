import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='whitegrid')

# Fungsi-fungsi yang sudah ada
def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"cnt": ["sum"]})
    return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({
        "registered": "sum"
    }).reset_index().rename(columns={"registered": "register_sum"})
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({
        "casual": ["sum"]
    }).reset_index().rename(columns={"casual": "casual_sum"})
    return cas_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season(day_df):
    season_df = day_df.groupby(by="season").cnt.sum().reset_index()
    return season_df

# Membaca dataset
days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

# Mengonversi kolom datetime
datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(drop=True, inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

# Menentukan rentang waktu
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    st.image("dashboard/bike.png", use_column_width=True)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

# Filter dataframe berdasarkan rentang waktu
main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) &
                       (days_df["dteday"] <= pd.to_datetime(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) &
                        (hours_df["dteday"] <= pd.to_datetime(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('🚲 Bike Sharing Dashboard :sparkles:')

st.subheader('📊 Daily Sharing Data')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

# Visualisasi Performa Penjualan
st.subheader("📈 Performa Penjualan Perusahaan dalam Beberapa Tahun Terakhir")
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(
    main_df_days["dteday"],
    main_df_days["cnt"],
    marker='o', 
    linewidth=2,
    color="#007BFF",
    markerfacecolor="#FF5733"
)
ax.set_title('Performa Penjualan (Jumlah Pemakaian Sepeda per Hari)', fontsize=16, color="#333333")
ax.set_xlabel('Tanggal', fontsize=14)
ax.set_ylabel('Jumlah Pemakaian', fontsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Visualisasi Perbandingan Registered vs Casual
st.subheader("🧍‍♂️ Perbandingan Customer yang Memilih Registered dan Casual")
labels = ['Casual', 'Registered']
sizes = [18.8, 81.2]
explode = (0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        colors=["#98DF8A", "#A4C8E1"], shadow=True, startangle=140)
ax1.axis('equal')
st.pyplot(fig1)
