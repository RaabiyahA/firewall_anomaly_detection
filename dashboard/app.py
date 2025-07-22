import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Firewall Anomaly Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", "log2.csv")
    if not os.path.exists(filepath):
        st.error(f"❌ Data file not found: {filepath}")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    if 'anomaly' not in df.columns:
        st.warning("Run the anomaly detection notebook first to tag anomalies.")
    return df

df = load_data()

# Parse timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Time window filter
st.sidebar.subheader("🕒 Time Range")
time_window = st.sidebar.selectbox("Select Time Window", ["All", "Last 1 Hour", "Last 12 Hours", "Last 24 Hours"])

if time_window == "Last 1 Hour":
    df = df.last("1H")
elif time_window == "Last 12 Hours":
    df = df.last("12H")
elif time_window == "Last 24 Hours":
    df = df.last("24H")

# Sidebar filter
st.sidebar.header("📊 Filters")
byte_threshold = st.sidebar.slider("Minimum Bytes", 0, int(df['Bytes'].max()), 0)
df_filtered = df[df['Bytes'] >= byte_threshold]

# Title
st.title("🔥 Firewall Log Anomaly Dashboard")

# Summary
st.metric("Total Records", len(df))
st.metric("Anomalies Detected", (df['anomaly'] == -1).sum() if 'anomaly' in df.columns else "N/A")

# Main Plot
st.subheader("📈 Bytes vs Elapsed Time (Anomalies Highlighted)")
fig, ax = plt.subplots(figsize=(10, 5))
if 'anomaly' in df.columns:
    sns.scatterplot(data=df_filtered, x='Elapsed Time (sec)', y='Bytes', hue='anomaly', palette='coolwarm', ax=ax)
else:
    sns.scatterplot(data=df_filtered, x='Elapsed Time (sec)', y='Bytes', ax=ax)
st.pyplot(fig)

# Threat Type Chart
st.subheader("⚠️ Threat Type Breakdown")
if 'threat_type' in df.columns:
    threat_counts = df['threat_type'].value_counts()
    st.bar_chart(threat_counts)

# Raw Data Option
if st.checkbox("📄 Show Raw Data"):
    st.write(df_filtered.head(100))

# CSV Export
if st.button("💾 Download Anomalies as CSV"):
    anomaly_df = df[df['anomaly'] == -1]
    st.download_button("Click to Download", anomaly_df.to_csv().encode('utf-8'), "anomalies.csv", "text/csv")

    
