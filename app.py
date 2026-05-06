import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page Settings
st.set_page_config(page_title="Harish's Pro Data Tool", layout="wide")
st.title("🚀 Harish's Super-Fast AI Assistant")
st.markdown("---")

# API Configuration
GOOGLE_API_KEY = "ఇక్కడ_మీ_API_KEY_పేస్ట్_చేయండి"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- స్పీడ్ పెంచడానికి క్యాచింగ్ ఫంక్షన్ ---
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Sidebar Menu
menu = st.sidebar.selectbox("ఏం చేయాలనుకుంటున్నారు?", ["Data Analytics & AI", "Compare Two Sheets", "Advanced Cleaning"])

if menu == "Data Analytics & AI":
    uploaded_file = st.file_uploader("ఎక్సెల్ ఫైల్ అప్‌లోడ్ చేయండి", type=['xlsx', 'csv'])
    
    if uploaded_file:
        df = load_data(uploaded_file) # ఇక్కడ క్యాచింగ్ వాడుతున్నాం
        st.write("### మీ డేటా ప్రివ్యూ")
        
        search = st.text_input("🔍 డేటాలో వెతకండి (Enter నొక్కండి)")
        if search:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        st.dataframe(df.astype(str))

        st.divider()
        # AI ప్రశ్న అడిగే బాక్స్
        user_question = st.text_input("💬 AIని అడగండి (ప్రశ్న టైప్ చేసి Enter నొక్కండి)")
        if user_question:
            with st.spinner('AI ఆలోచిస్తోంది... చాలా వేగంగా సమాధానం వస్తుంది!'):
                # కేవలం అవసరమైన డేటాను మాత్రమే AIకి పంపి స్పీడ్ పెంచుతున్నాం
                prompt = f"Data Summary:\n{df.describe().to_string()}\nSample Rows:\n{df.head(5).to_string()}\nQuestion: {user_question}"
                response = model.generate_content(prompt)
                st.info(f"AI సమాధానం: {response.text}")

elif menu == "Compare Two Sheets":
    st.write("### రెండు షీట్ల మధ్య తేడాలను చూడండి")
    file1 = st.file_uploader("మొదటి ఫైల్ (Old)", type=['xlsx', 'csv'])
    file2 = st.file_uploader("రెండో ఫైల్ (New)", type=['xlsx', 'csv'])
    
    if file1 and file2:
        df1 = load_data(file1)
        df2 = load_data(file2)
        diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
        st.write("✅ కొత్తగా మారిన డేటా:")
        st.dataframe(diff.astype(str))

# Download Button
if 'df' in locals():
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 అప్‌డేట్ చేసిన ఫైల్‌ని డౌన్‌లోడ్ చేసుకోండి", data=csv, file_name='Harish_Data.csv')
