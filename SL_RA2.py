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
                        "You are an Expert CUSTOMER SERVICE PROFESSIONAL."
                        "Your task is to FORMULATE empathetic, professional, and well-rounded responses to customer reviews."
                        "Follow these steps to ensure success:"
                        "1. READ each customer review CAREFULLY to fully understand the customer's experience and perspective."
                        "2. EXPRESS UNDERSTANDING and APPRECIATION in your response by acknowledging the customer's feelings and thanking them for their feedback."
                        "3. ENSURE that your replies are CONCISE yet THOUGHTFUL, providing a personalized touch that reflects the specific content of each review."
                        "4. USE correct PROFESSIONAL TERMINOLOGY, particularly industry-specific and legal terms where appropriate, to maintain professionalism."
                        "5. TAILOR each response directly to the review's details, avoiding generic language that could apply to any situation."
                        "6. OFFER solutions or next steps when addressing any issues raised by the customer, demonstrating a proactive approach."
                        "Remember that you MUST always maintain a tone of empathy and professionalism."
                        "Take a Deep Breath."
                    )
                },
                {"role": "user", "content": f"Review: {client_review}\nLanguage: {draft_language}\nInsights: {insights}"}
            ]

            # Generate draft response
            response = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:personal:replypro1:Aah8tN4s",
                messages=messages,
                max_tokens=4000
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
                    
                    f"You are an Expert PROFESSIONAL TRANSLATOR. Your task is to CONVERT the following" 
                    f"text into {final_language} with utmost ACCURACY and PRECISION.Proceed with these steps:"
                    f"1. READ the source text thoroughly to UNDERSTAND the context and the INDUSTRY-SPECIFIC terms used."
                    f"2. IDENTIFY any terms that require SPECIALIZED KNOWLEDGE and RESEARCH their equivalent in the {final_language},"
                    f"ensuring they are LOCALLY APPROPRIATE and PROFESSIONALLY RECOGNIZED."
                    f"3. PAY ATTENTION to grammatical structures and idiomatic expressions, ADAPTING them to fit the "
                    f"linguistic norms of {final_language} while preserving their intended meaning."
                    f"4. ENSURE that all terminology is used CONSISTENTLY throughout the translation and is in line with industry standards."
                    f"5. REVIEW your translation for any possible AMBIGUITIES or inaccuracies, and make necessary adjustments "
                    f"for CLARITY and FLOW."
                    f"7. PROOFREAD your work to eliminate any spelling or typographical errors."
                    f"Take a Deep Breath."
                    )
                },
                {"role": "user", "content": draft_response}
            ]

            # Perform translation
            translation = client.chat.completions.create(
                model="ft:gpt-4o-2024-08-06:personal:replypro1:Aah8tN4s",
                messages=messages,
                max_tokens=4000
            )

            # Update the draft response with the translation
            # Update final response in session state
            st.session_state['final_response'] = translation.choices[0].message.content


        except Exception as e:
            st.error(f"An error occurred: {e}")

# Show updated response
# Final response section (editable after translation)
st.text_area("Final Response (Translated)", value=st.session_state['final_response'], height=200, key="final_response_area")
