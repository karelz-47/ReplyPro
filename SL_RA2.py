import streamlit as st
from openai import OpenAI

# Initialize session state for draft response
if 'draft_response' not in st.session_state:
    st.session_state['draft_response'] = ""  # For the generated draft

if 'final_response' not in st.session_state:
    st.session_state['final_response'] = ""  # For the translated final version

# App title
st.title("ReplyPro - Intelligent Review Responses")

# --- Section 1: Draft Generation ---
st.header("1. Generate Draft Response")

# Inputs for draft generation
client_review = st.text_area("Client's Review or Comment", placeholder="Enter the client's feedback...")
insights = st.text_area("Additional Context or Insights (optional)")
draft_language = st.selectbox("Language of Draft:", ["English", "Slovak", "Italian", "Icelandic", "Hungarian", "German", "Czech", "Polish", "Vulcan"])
api_key = st.text_input("OpenAI API Key", type="password")

# Generate draft button
if st.button("Generate Draft"):
    if not api_key:
        st.error("Please provide your OpenAI API Key.")
    elif not client_review.strip():
        st.error("Please enter a client review to generate a draft.")
    else:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)

            # Prepare messages for draft generation
            messages = [
                {
                "role": "system", 
                "content": (
                        "You are a professional customer service assistant. "
                        "Generate empathetic, professional, and well-rounded responses to customer reviews. "
                        "Make sure the responses express understanding and appreciation while being concise but thoughtful. "
                        "Ensure to use correct professional terminology, especially for industry-specific and legal terms. "
                        "Avoid overly generic replies and tailor the response to the review."
                    )
                },
                {"role": "user", "content": f"Review: {client_review}\nLanguage: {draft_language}\nInsights: {insights}"}
            ]

            # Generate draft response
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:personal:replypro1:Aah8tN4s",
                messages=messages,
                max_tokens=2000
            )

            # Save the draft response in session state
            # Update draft response in session state
            st.session_state['draft_response'] = response.choices[0].message.content

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Section 2: Final Version ---
st.header("2. Translate Final Version")

# Editable field showing the draft response
draft_response = st.text_area("Draft Response (Editable)", value=st.session_state['draft_response'], height=200)

# Inputs for final version
final_language = st.selectbox("Language of Final Version:", ["English", "Slovak", "Italian", "Icelandic", "Hungarian", "German", "Czech", "Polish", "Vulcan"])

# Translate button
if st.button("Translate Final Version"):
    if not api_key:
        st.error("Please provide your OpenAI API Key.")
    elif not st.session_state['draft_response'].strip():
        st.error("Please generate a draft response or edit the current one.")
    else:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)

            # Prepare messages for translation
            messages = [
                {
                    "role": "system", 
                    "content": (
                        f"You are a professional translator. When translating, ensure to use correct "
                        f"localized and professional terminology, especially for industry-specific terms. "
                        f"Translate the following text into {final_language}, preserving formal tone and precision."
                    )
                },
                {"role": "user", "content": draft_response}
            ]

            # Perform translation
            translation = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:personal:replypro1:Aah8tN4s",
                messages=messages,
                max_tokens=2000
            )

            # Update the draft response with the translation
            # Update final response in session state
            st.session_state['final_response'] = translation.choices[0].message.content


        except Exception as e:
            st.error(f"An error occurred: {e}")

# Show updated response
# Final response section (editable after translation)
st.text_area("Final Response (Translated)", value=st.session_state['final_response'], height=200, key="final_response_area")
