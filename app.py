import streamlit as st
import tempfile
import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# RAG Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Matchmaking DB Imports
from database import get_all_founders, add_founder

# ---------------------------------------------------------
# 1. THE SYSTEM PROMPTS (Feature 2 & 3)
# ---------------------------------------------------------
SENTIMENT_PROMPT = """Analyze the following startup pitch for Tone, Confidence, and Clarity.
Return ONLY a short paragraph assessing if the founder sounds nervous, overly-confident, or professional.

Pitch: {user_pitch}
"""

VC_PROMPT = """You are a brutally honest startup investor.

Context from Pitch Deck / Resume:
{context}

Original Pitch: {user_pitch}

Behavior Rules:
1. Be direct, blunt, and skeptical.
2. Focus on business fundamentals: problem, market demand, competition.
3. If the idea is weak, clearly explain why using facts from the Context.
4. Do not praise ideas unnecessarily.

Provide your harsh, analytical critique.
"""

COACH_PROMPT = """You are a supportive Pitch Coach. Your job is to read the harsh VC's feedback and the Tone Analysis, and give the founder 3 actionable steps to improve.

Tone Analysis: {sentiment}

VC Critique: {vc_feedback}

Provide 3 bullet points on exactly what the founder should fix before pitching again. Be constructive and encouraging.
"""

MATCHMAKER_PROMPT = """You are an expert startup Co-Founder Matchmaker.
Your job is to read the new founder's profile, and then look at the database of existing founders to find the BEST complement.

New Founder Profile:
- Name: {user_name}
- Role: {user_role}
- Skills: {user_skills}
- Pitch: {user_pitch}

Database of Potential Co-Founders:
{database_profiles}

INSTRUCTIONS:
1. Pick the ONE best person from the database who has complementary skills (e.g., if the user is technical, find someone business-focused).
2. Explain exactly WHY they are a perfect match based on their skills and the user's pitch.
3. Keep it to one concise paragraph.
"""

# ---------------------------------------------------------
# 2. STREAMLIT WEB UI SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="AI Pitch Coach", page_icon="🎤")

st.title("🎤 AI Pitch Coach & VC Reviewer")
st.markdown("**Powered by N. V. Data Systems**")
st.write("Upload your Pitch Deck or Resume, enter your one-sentence pitch, and our Virtual Venture Capitalist will tear it apart (constructively).")

# ---------------------------------------------------------
# 3. LANGCHAIN & LLM ORCHESTRATION
# ---------------------------------------------------------
@st.cache_resource
def get_llm():
    return ChatOllama(model="llama3.2:3b", temperature=0.7)

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create the independent chains
prompt_sentiment = ChatPromptTemplate.from_template(SENTIMENT_PROMPT)
prompt_vc = ChatPromptTemplate.from_template(VC_PROMPT)
prompt_coach = ChatPromptTemplate.from_template(COACH_PROMPT)
prompt_matchmaker = ChatPromptTemplate.from_template(MATCHMAKER_PROMPT)

llm = get_llm()
chain_sentiment = prompt_sentiment | llm | StrOutputParser()
chain_vc = prompt_vc | llm | StrOutputParser()
chain_coach = prompt_coach | llm | StrOutputParser()
chain_matchmaker = prompt_matchmaker | llm | StrOutputParser()

# ---------------------------------------------------------
# 4. RAG DOCUMENT PROCESSING (Feature 1)
# ---------------------------------------------------------
import pytesseract
from pdf2image import convert_from_path
from langchain_core.documents import Document

def extract_text_with_ocr(pdf_path):
    st.info("🔍 Scanned PDF detected! Starting OCR Vision Extraction (Tesseract)...")
    text = ""
    # Convert PDF to list of images
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        st.write(f"Scanning Page {i+1}/{len(pages)}...")
        # Extract text from the image
        page_text = pytesseract.image_to_string(page)
        text += page_text + "\n\n"
    return text

def process_pdf(uploaded_file):
    # 1. Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        # 2. Extract Text from PDF (Standard PyPDF)
        st.info("📄 Reading document...")
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        # Check if PyPDF extracted actual text (often scanned PDFs return blank pages)
        is_empty = True
        for doc in documents:
            if doc.page_content.strip():
                is_empty = False
                break

        # If it's empty, trigger OCR!
        if is_empty:
            ocr_text = extract_text_with_ocr(tmp_path)
            if not ocr_text.strip():
                st.error("OCR failed to extract logic from the PDF.")
                return None
            
            # Convert raw text back into a LangChain Document format
            documents = [Document(page_content=ocr_text, metadata={"source": "OCR"})]
            st.success("✅ OCR Extraction Complete.")

        # 3. Chunk the text
        st.info("🔪 Slicing document into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # 4. Create FAISS Vector Database
        st.info("🧠 Memorizing the chunks into the Vector Database (FAISS)...")
        embeddings = get_embeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        return vectorstore
    
    finally:
        os.remove(tmp_path) # Clean up temp file

# ---------------------------------------------------------
# 5. USER INTERACTION LOGIC & TABS (Feature 3 included)
# ---------------------------------------------------------
from openai import OpenAI

# Sidebar for File Upload
with st.sidebar:
    st.header("1. Upload Knowledge Context")
    uploaded_file = st.file_uploader("Upload Pitch Deck (PDF)", type=["pdf"])
    
    if uploaded_file and "vectorstore" not in st.session_state:
        vectorstore = process_pdf(uploaded_file)
        if vectorstore:
            st.session_state["vectorstore"] = vectorstore
            st.success("✅ Database Ready!")

# Create Tabs for different features
tab1, tab2, tab3 = st.tabs([
    "🎤 AI Pitch Coach (Local)", 
    "🌍 Market Research (Cloud)",
    "🤝 Co-Founder Matchmaker"
])

# ====== TAB 1: The Core Pitch Coach (Local RAG) ======
with tab1:

    user_pitch = st.text_input("Enter your startup pitch here:", placeholder="E.g., I want to build an app for tracking dogs...")
    
    if st.button("Submit Pitch to VC"):
        if user_pitch:
            with st.spinner("The Virtual Investor is analyzing your pitch..."):
                try:
                    # 6. RETRIEVAL LOGIC (RAG)
                    context_text = "No document uploaded."
                    if "vectorstore" in st.session_state:
                        # Search the FAISS database for the 3 most relevant chunks to the user's pitch
                        retriever = st.session_state["vectorstore"].as_retriever(search_kwargs={"k": 3})
                        relevant_docs = retriever.invoke(user_pitch)
                        # Combine the retrieved chunks into one large string
                        context_text = "\\n\\n".join([doc.page_content for doc in relevant_docs])
    
                    # 7. EXECUTE THE MULTI-STAGE AI (Feature 2)
                    
                    # Stage 1: Tone Analysis
                    st.markdown("### 🕵️‍♂️ Stage 1: Sentiment & Tone Analysis")
                    with st.spinner("Analyzing your confidence and tone..."):
                        sentiment_result = chain_sentiment.invoke({"user_pitch": user_pitch})
                        st.info(sentiment_result)
    
                    # Stage 2: The Harsh VC
                    st.markdown("### 📉 Stage 2: VC Critique")
                    with st.spinner("The Virtual Investor is reviewing your business model..."):
                        vc_result = chain_vc.invoke({
                            "context": context_text,
                            "user_pitch": user_pitch
                        })
                        st.error(vc_result)
    
                    # Stage 3: The Pitch Coach
                    st.markdown("### 🏆 Stage 3: Coach's Reinforcement Feedback")
                    with st.spinner("Your coach is generating actionable advice..."):
                        coach_result = chain_coach.invoke({
                            "sentiment": sentiment_result,
                            "vc_feedback": vc_result
                        })
                    st.success(coach_result)
                
                    st.balloons()
                    
                    # Show Dev View of Retrieved RAG Context
                    if "vectorstore" in st.session_state:
                        with st.expander("🛠️ Developer View: What the AI retrieved from FAISS database"):
                            st.write(context_text)
                    
                except Exception as e:
                    st.error("⚠️ Error connecting to local LLM.")
                    st.error(f"Technical Details: {e}")
        else:
            st.warning("Please enter a pitch first!")


# ====== TAB 2: Market Research & Brainstorming (OpenRouter API) ======
with tab2:
    st.markdown("### 🌍 Global Market Insights")
    st.write("Need brainstorming ideas or want to simulate public opinion? Ask an external Cloud AI model.")
    
    # In a real app, use st.secrets. For this resume project, we ask for it securely.
    api_key = st.text_input("Enter your OpenRouter API Key:", type="password")
    
    brainstorm_query = st.text_area("What do you want to brainstorm?", placeholder="e.g. What are 3 alternative use cases for a smart terminal in the healthcare space?")
    
    if st.button("Generate Insights"):
        if not api_key:
            st.error("Please provide an OpenRouter API key first.")
        elif brainstorm_query:
            with st.spinner("Connecting to 3rd Party Cloud API (OpenRouter)..."):
                try:
                    # Initialize the OpenAI Client, but point it to OpenRouter
                    client = OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=api_key,
                    )
                    
                    # We use a free tier OpenRouter model for testing
                    completion = client.chat.completions.create(
                        model="meta-llama/llama-3.2-3b-instruct:free",
                        messages=[
                            {"role": "system", "content": "You are a creative business strategist brainstorming ideas."},
                            {"role": "user", "content": brainstorm_query}
                        ]
                    )
                    
                    st.success("Cloud Analysis Complete!")
                    st.info(completion.choices[0].message.content)
                    
                except Exception as e:
                    st.error("⚠️ Failed to connect to third-party API.")
                    st.error(f"Details: {e}")
        else:
            st.warning("Please enter a question to brainstorm.")

# ====== TAB 3: Co-Founder Matchmaker (SQLite DB) ======
with tab3:
    st.markdown("### 🤝 Find Your Perfect Co-Founder")
    st.write("We use a local SQLite database to store user profiles and match them based on complementary skills.")
    
    # 1. Show existing database
    with st.expander("📂 View Current Startup Network (Database)"):
        founders = get_all_founders()
        for f in founders:
            st.markdown(f"**{f['name']}** ({f['role']}) - Skills: {f['skills']}")
            
    st.markdown("---")
    
    # 2. Add new user to database
    st.markdown("#### 👤 Step 1: Create Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Your Name:")
        new_role = st.selectbox("Primary Role:", ["Technical/Software", "Hardware Engineering", "Business/Marketing", "Operations/Finance", "Design/Product"])
    with col2:
        new_skills = st.text_input("Top 3 Skills (e.g., Python, C++, PCB Design):")
        new_pitch = st.text_input("Your Startup Idea:")
        
    if st.button("Save Profile to Database"):
        if new_name and new_skills and new_pitch:
            add_founder(new_name, new_role, new_skills, new_pitch)
            st.success(f"Profile saved! Welcome to the network, {new_name}.")
            st.rerun() # Refresh to show new data
        else:
            st.warning("Please fill out all fields.")
            
    st.markdown("---")
    
    # 3. AI Matchmaking Logic
    st.markdown("#### 🧠 Step 2: AI Matchmaking")
    st.write("Click below to let our Local LLM analyze the database and find your best match.")
    
    if st.button("Find My Co-Founder"):
        if new_name and new_skills and new_pitch:
            with st.spinner("Analyzing database profiles for semantic skill matching..."):
                try:
                    # Convert the list of dicts into a single string for the prompt
                    db_string = ""
                    for f in get_all_founders():
                        if f['name'] != new_name: # Don't match with yourself
                            db_string += f"- {f['name']} ({f['role']}): {f['skills']} | Idea: {f['pitch']}\n"
                    
                    if not db_string.strip():
                        st.warning("Not enough other people in the database yet!")
                    else:
                        match_result = chain_matchmaker.invoke({
                            "user_name": new_name,
                            "user_role": new_role,
                            "user_skills": new_skills,
                            "user_pitch": new_pitch,
                            "database_profiles": db_string
                        })
                        
                        st.success("Match Found!")
                        st.info(match_result)
                        st.balloons()
                except Exception as e:
                    st.error("Error running Matchmaker.")
                    st.error(e)
        else:
            st.warning("Please create your profile in Step 1 first!")
