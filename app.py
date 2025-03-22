import streamlit as st
import pandas as pd

# Custom CSS for Responsive UI
st.markdown(
    """
    <style>
        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: auto;
        }
        .header {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #333;
        }
        .sub-header {
            text-align: center;
            font-size: 16px;
            color: #666;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
            width: 100%;
        }
        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
            overflow-x: auto;
        }
        .result-table th, .result-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .result-table th {
            background-color: #f4f4f4;
        }
        /* Responsive Table */
        @media screen and (max-width: 600px) {
            .result-table th, .result-table td {
                font-size: 12px;
                padding: 6px;
            }
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #888;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# UI Layout
st.markdown('<div class="container">', unsafe_allow_html=True)

# 🔥 Only One Header Now (Fixed)
st.markdown('<p class="header">🔍 Duplicate Consumer Check</p>', unsafe_allow_html=True)

# Input Field
device_input = st.text_input("Device Number (Case Insensitive)")

# Upload Excel File
uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read Excel File
        df = pd.read_excel(uploaded_file)

        # Standardizing Device Column for Case-Insensitive Search
        df['Device #'] = df['Device #'].astype(str).str.strip().str.lower()
        search_device = device_input.strip().lower()

        # Convert datetime columns to "DD-MM-YYYY"
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].dt.strftime('%d-%m-%Y')

        if st.button("🔍 Search", key="search_button", help="Click to Search", type="primary"):
            result_df = df[df['Device #'] == search_device]

            if not result_df.empty:
                # ❌ Removed Consumer Found Message
                # Extracting Details
                data = result_df.iloc[0].to_dict()

                # Displaying Details in a Structured Format
                st.markdown('<table class="result-table">', unsafe_allow_html=True)
                for key, value in data.items():
                    st.markdown(f"<tr><th>{key}</th><td>{value}</td></tr>", unsafe_allow_html=True)
                st.markdown('</table>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ No data found for this Device Number.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<p class="footer">Created by Noushad Akhter</p>', unsafe_allow_html=True)
