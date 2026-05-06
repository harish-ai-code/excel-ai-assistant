import streamlit as st
import pandas as pd
import google.generativeai as genai

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="Harish's Pro Data Tool", layout="wide")
st.title("🚀 Harish's Advanced Data Assistant")
st.markdown("---")

# API Configuration
GOOGLE_API_KEY = "ఇక్కడ_మీ_API_KEY_పేస్ట్_చేయండి"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# సైడ్ బార్ లో మెనూ
menu = st.sidebar.selectbox("ఏం చేయాలనుకుంటున్నారు?", ["Data Analytics & AI", "Compare Two Sheets", "Advanced Cleaning"])

if menu == "Data Analytics & AI":
    uploaded_file = st.file_uploader("ఎక్సెల్ ఫైల్ అప్‌లోడ్ చేయండి", type=['xlsx', 'csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("### మీ డేటా ప్రివ్యూ")
        
        # 1. Search & Filter ఫీచర్
        search = st.text_input("🔍 డేటాలో వెతకండి (ఉదా: గ్రామం పేరు లేదా వర్కర్ పేరు)")
        if search:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        st.dataframe(df.astype(str))

        # 2. AI Chat
        st.divider()
        user_question = st.text_input("💬 ఈ డేటా గురించి AIని అడగండి (ఉదా: రిపోర్ట్ సమ్మరీ ఇవ్వు)")
        if user_question:
            prompt = f"Data Summary:\n{df.head(10).to_string()}\nQuestion: {user_question}"
            response = model.generate_content(prompt)
            st.info(f"AI సమాధానం: {response.text}")

elif menu == "Compare Two Sheets":
    st.write("### రెండు షీట్ల మధ్య తేడాలను చూడండి")
    file1 = st.file_uploader("మొదటి ఫైల్ (Old)", type=['xlsx', 'csv'])
    file2 = st.file_uploader("రెండో ఫైల్ (New)", type=['xlsx', 'csv'])
    
    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        # తేడాలను గుర్తించడం
        diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
        st.write("✅ కొత్తగా మారిన లేదా యాడ్ అయిన డేటా ఇక్కడ ఉంది:")
        st.dataframe(diff)

elif menu == "Advanced Cleaning":
    uploaded_file = st.file_uploader("క్లీనింగ్ కోసం ఫైల్ అప్‌లోడ్ చేయండి", type=['xlsx', 'csv'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        
        # 3. Column Splitter
        col_to_split = st.selectbox("ఏ కాలమ్ ని విడగొట్టాలి?", df.columns)
        sep = st.text_input("దేని ఆధారంగా విడగొట్టాలి? (ఉదాహరణకు స్పేస్ లేదా కామా)", " ")
        if st.button("Split Column"):
            new_cols = df[col_to_split].str.split(sep, expand=True)
            df = pd.concat([df, new_cols], axis=1)
            st.success("కాలమ్ విడగొట్టబడింది!")
            st.dataframe(df.head())

        # 4. Data Validation (Phone Number)
        if st.button("Check Phone Numbers"):
            # ఫోన్ నంబర్లు 10 అంకెలు లేని వాటిని గుర్తించడం
            invalid = df[df.apply(lambda row: any(len(str(x)) != 10 for x in row if str(x).isdigit()), axis=1)]
            st.warning(f"తప్పుగా ఉన్న నంబర్ల సంఖ్య: {len(invalid)}")
            st.dataframe(invalid)

# డౌన్లోడ్ బటన్
if 'df' in locals():
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 అప్‌డేట్ చేసిన ఫైల్‌ని డౌన్‌లోడ్ చేసుకోండి", data=csv, file_name='Harish_Updated_Data.csv')
