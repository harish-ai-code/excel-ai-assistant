Python

import streamlit as st
import pandas as pd
import io

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="Harish's Smart AI Assistant", layout="wide")

# ప్రొఫెషనల్ బ్లూ అండ్ వైట్ థీమ్ కోసం స్టైలింగ్
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stHeader { color: #003366; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Harish's Smart AI Data Assistant")
st.write("One-Click Data Analysis & Cleaning by Harish Khan Sarma")

# ఫైల్ అప్‌లోడ్
uploaded_file = st.file_uploader("మీ ఎక్సెల్ లేదా CSV ఫైల్‌ని ఇక్కడ అప్‌లోడ్ చేయండి", type=['xlsx', 'csv'])

if uploaded_file is not None:
    # డేటా లోడ్ చేయడం
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("ఫైల్ అప్‌లోడ్ అయ్యింది!")
    st.write("### డేటా ప్రివ్యూ (మొదటి 5 లైన్లు):")
    st.dataframe(df.head())

    # వన్-క్లిక్ బటన్స్
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Remove Duplicates"):
            original_count = len(df)
            df = df.drop_duplicates()
            st.warning(f"{original_count - len(df)} డూప్లికేట్స్ తీసివేయబడ్డాయి!")
            st.dataframe(df.head())

    with col2:
        if st.button("📊 Quick Analysis"):
            st.write("### డేటా సమ్మరీ:")
            st.write(df.describe())

    with col3:
        # మోడిఫై చేసిన ఫైల్ డౌన్లోడ్
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        st.download_button(label="📥 Download Cleaned File", data=processed_data, file_name="Harish_Cleaned_Data.xlsx")

    # AI Chat Section
    st.divider()
    st.header("🤖 AI Data Chat (Beta)")
    user_question = st.text_input("ఈ డేటా గురించి ఏదైనా అడగండి (ఉదా: ఏ మండలంలో కేసులు ఎక్కువగా ఉన్నాయి?):")
    if user_question:
        st.info("AI విశ్లేషిస్తోంది... (దీనికి Google API కనెక్ట్ చేయాల్సి ఉంటుంది)")
        # ఇక్కడ మీరు డేటా గురించి సింపుల్ లెక్కలు చూడొచ్చు
        if "rows" in user_question.lower() or "లైన్లు" in user_question:
            st.write(f"ఈ షీట్ లో మొత్తం {len(df)} లైన్లు ఉన్నాయి.")
