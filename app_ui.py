# app.py
import streamlit as st
from sqlagent import ask_agent  # your method

st.title("Doctor's Availability Chatbot for https://medicasapp.com/")
st.markdown(
    """
    Ask questions about doctor availability.
    Example: "Is Dr B. L. Avinash available on 2025-10-15 at 1:00 PM?"
    """
)

# User input
user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Fetching answer..."):
            try:
                # Call your existing method
                answer = ask_agent(user_question)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
