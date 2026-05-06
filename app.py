# 2. AI చాట్ బాక్స్ - వేగంగా పనిచేయడానికి (Form with Enter Button)
    st.divider()
    st.markdown("### 💬 మీ డేటా గురించి AIని అడగండి")
    
    # ఫామ్ ఉపయోగించడం వల్ల ఎంటర్ నొక్కగానే పని చేస్తుంది
    with st.form(key='ai_chat_form', clear_on_submit=False):
        user_question = st.text_input("ప్రశ్న ఇక్కడ టైప్ చేయండి:", placeholder="ఉదా: మొత్తం ఎన్ని వేకెన్సీలు ఉన్నాయి?")
        submit_button = st.form_submit_button(label='Send / Enter')

    if submit_button and user_question:
        with st.spinner('AI ఆలోచిస్తోంది...'): # వేగంగా జరుగుతున్నట్లు యూజర్ కి తెలుస్తుంది
            try:
                # డేటాను టెక్స్ట్ రూపంలో పంపడం వల్ల AI వేగంగా స్పందిస్తుంది
                data_summary = df.head(20).to_string() 
                prompt = f"Data Context:\n{data_summary}\n\nUser Question: {user_question}\nAnswer clearly in Telugu or English."
                
                response = model.generate_content(prompt)
                st.info(f"AI సమాధానం: {response.text}")
            except Exception as e:
                st.error(f"చిన్న సమస్య వచ్చింది: {e}")
