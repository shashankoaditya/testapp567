import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="SAP T-Code Explorer", layout="centered")

st.title("SAP T-Code Explorer")
st.write("Enter a SAP T-code to understand its purpose and module.")

# Input field
tcode = st.text_input("Enter SAP T-Code")

# Button
if st.button("Get Details"):

    if not tcode:
        st.warning("Please enter a T-code")
    else:
        with st.spinner("Fetching details..."):

            prompt = f"""
            Provide concise details for SAP T-code: {tcode}

            Format:
            Purpose: <short explanation>
            Module: <module name>
            Type: <Transactional / Configuration / Display>
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )

                result = response.choices[0].message.content

                st.success("Result")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")
