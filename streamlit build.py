import streamlit as st
import openai

st.title("ChatGPT-like clone")

# Set OpenAI API key directly in the code
openai.api_key = "sk-wlV9xkHlk6PUHTwewZjGdNy2lYf-6hXqQWXVf_G8cFT3BlbkFJAwmIxaGoBYtwx6pqZLWV5eMCC3bS4XG407lyq2jB8A"

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Send request to OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=False,  # Turn off streaming to handle the response properly
            )
            assistant_message = response.choices[0].message["content"]
        except Exception as e:
            st.error(f"Error: {str(e)}")
            assistant_message = "There was an error processing the request."

        st.markdown(assistant_message)
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
