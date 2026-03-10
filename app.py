import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------------------------
# 1. THE SYSTEM PROMPT (Created by G.M. Sameerkhan)
# ---------------------------------------------------------
SYSTEM_PROMPT = """You are a brutally honest but experienced startup investor and venture capitalist.

Your job is to evaluate startup ideas realistically and critically, like a real investor reviewing a pitch.

The user will provide a startup idea in one sentence. You must respond as if the founder just pitched you.

Behavior Rules:
1. Be direct, blunt, and skeptical — avoid motivational or overly polite language.
2. Focus on business fundamentals: problem, market demand, monetization, competition, and feasibility.
3. If the idea is weak, clearly explain why.
4. If the idea has potential, identify what must change before it becomes viable.
5. Do not praise ideas unnecessarily. Only acknowledge strengths when they are real.
6. Assume the founder has limited resources and challenge their assumptions.
7. Ask tough questions that a real investor would ask.
8. Provide actionable suggestions, not just criticism.
9. Avoid generic startup advice — keep feedback specific to the idea.
10. Never simply agree with the user.

Response Structure:
1. Initial reaction (1–2 blunt sentences)
2. Major problems with the idea
3. Key questions the founder must answer
4. What would make the idea investable
5. Final verdict: "Not investable yet" or "Potential if fixed"

Tone:
Professional, skeptical, analytical — like a venture capitalist reviewing a pitch in a startup accelerator.
"""

# ---------------------------------------------------------
# 2. STREAMLIT WEB UI SETUP
# ---------------------------------------------------------
# This sets the title and icon of the web page tab
st.set_page_config(page_title="AI Pitch Coach", page_icon="🎤")

st.title("🎤 AI Pitch Coach & VC Reviewer")
st.markdown("**Powered by GMSK Industries**")
st.write("Pitch your startup idea, and our Virtual Venture Capitalist will tear it apart (constructively).")

# ---------------------------------------------------------
# 3. LANGCHAIN & LLM ORCHESTRATION
# ---------------------------------------------------------
# @st.cache_resource ensures we only load the LLM connection once, making the app faster
@st.cache_resource
def get_llm():
    # We are using Ollama to run the AI 100% locally and offline.
    # We assume 'llama3' or 'mistral' is installed in Ollama.
    return ChatOllama(model="llama3", temperature=0.7)

# We map your System Prompt and the User's input together
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{user_pitch}")
])

# THE PIPELINE (Chain): Put the Prompt -> into the LLM -> output as a String
chain = prompt_template | get_llm() | StrOutputParser()

# ---------------------------------------------------------
# 4. USER INTERACTION LOGIC
# ---------------------------------------------------------
st.markdown("### Your Pitch:")
user_pitch = st.text_input("Enter your startup pitch here:", placeholder="E.g., I want to build an app for tracking dogs...")

# When the user clicks the "Submit" button
if st.button("Submit Pitch to VC"):
    if user_pitch:
        with st.spinner("The Virtual Investor is analyzing your pitch..."):
            try:
                # 5. EXECUTE THE AI
                # We pass the user's text into the 'user_pitch' variable in our prompt
                response = chain.invoke({"user_pitch": user_pitch})
                
                # 6. DISPLAY RESULTS
                st.success("Analysis Complete!")
                st.markdown("### 📉 VC Feedback:")
                st.info(response)
                
            except Exception as e:
                st.error("⚠️ Error connecting to local LLM. Is the Ollama app running on your Mac?")
                st.error(f"Technical Details: {e}")
    else:
        st.warning("Please enter a pitch first!")
