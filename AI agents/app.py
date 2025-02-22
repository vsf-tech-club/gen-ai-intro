import streamlit as st
import asyncio
from ai_agent import AIAgent

st.title("AI Agent Interface")
st.write("Submit your task and the AI agent will analyze it, create a plan, and execute it.")

# Initialize session state for the agent if it doesn't exist
if 'agent' not in st.session_state:
    st.session_state.agent = AIAgent()

# Create the input text area
user_task = st.text_area(
    "Enter your task",
    placeholder="Example: Create a study plan for learning artificial intelligence",
    height=100
)

# Create the submit button
if st.button("Submit"):
    if user_task:
        with st.spinner('Processing your task...'):
            try:
                # Create a new asyncio event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Execute the task
                response = loop.run_until_complete(st.session_state.agent.execute_task(user_task))
                
                # Get agent insights
                insights = st.session_state.agent.memory
                
                # Display the response in a nice format
                st.success("Task Completed!")
                
                st.subheader("Response:")
                st.write(response)
                
                st.subheader("Agent Insights:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tasks Completed", len(insights['task_history']))
                with col2:
                    st.metric("Learning Entries", len(insights['learnings']))
                with col3:
                    st.metric("Conversation Turns", len(insights['conversation_history']))
                
                # Close the event loop
                loop.close()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a task first.")