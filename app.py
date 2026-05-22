import streamlit as st
from langchain_groq import ChatGroq
from streamlit_js_eval import streamlit_js_eval

if "messages" not in st.session_state:
    st.session_state.messages = []
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "asked_for_feedback" not in st.session_state:
    st.session_state.asked_for_feedback = False

def sign_up():
    if st.session_state.name and st.session_state.company and st.session_state.skills:
        st.session_state.signed_up = True
        st.success("You have successfully signed up for the interview!")
    else:
        st.error("Please fill in all the details to sign up.")

def asked_for_feedback():
    st.session_state.asked_for_feedback = True

st.header("AI C++ Interviewer")

st.divider()

if not st.session_state["signed_up"]:
    st.subheader("Fill in your details to sign up for the interview")
    
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "company" not in st.session_state:
        st.session_state.company = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""
    
    st.session_state["name"] = st.text_input("Name", max_chars=50)
    st.session_state["company"] = st.text_input("Company", max_chars=50)
    st.session_state["skills"] = st.text_input("Skills (comma separated)", max_chars=100)

    st.button("Sign Up", on_click=sign_up)

if not st.session_state.asked_for_feedback and st.session_state["signed_up"]:
    st.subheader("Welcome to the AI C++ Interview! Start with an introduction.")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])

    if st.session_state.user_message_count < 5:
        if user_input := st.chat_input(placeholder="Your Answer", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").markdown(user_input)
            if st.session_state.user_message_count < 4:
                groq = ChatGroq(api_key=st.secrets["GROQ_KEY"], model="llama-3.1-8b-instant", max_tokens=512, temperature=0.7)
                messages = [
                    {"role": "system", "content": "You are an AI interviewer for a C++ programming position. Ask the candidate questions about their experience, skills, and knowledge in C++. Provide feedback on their answers and ask follow-up questions to assess their understanding."},
                    *st.session_state.messages
                ]
                response = groq.invoke(messages)
                assistant_message = response.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.chat_message("assistant").markdown(assistant_message)
            st.session_state.user_message_count += 1
      
     
if not st.session_state.asked_for_feedback and st.session_state.user_message_count >= 5:
    st.subheader("Thank you for completing the interview! Please provide your feedback.")
    st.button("Ask for feedback", on_click=asked_for_feedback)
        
if st.session_state.asked_for_feedback:
    groq = ChatGroq(api_key=st.secrets["GROQ_KEY"], model="llama-3.1-8b-instant", max_tokens=512, temperature=0.7)
    feedback_prompt = [
        {"role": "system", "content": "You are an AI interviewer for a C++ programming position. Provide feedback on the candidate's performance in the interview based on their answers to the questions. Highlight their strengths and areas for improvement."},
        *st.session_state.messages
    ]
    feedback_response = groq.invoke(feedback_prompt)
    st.subheader("Feedback on your interview performance:")
    st.markdown(feedback_response.content)
    if st.button("Restart Interview"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")




            




