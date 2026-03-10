# AI Pitch Coach & Founder Matchmaker

Welcome to the **AI Pitch Coach & Founder Matchmaker**, an intelligent virtual tool designed for ambitious founders. Whether you're preparing for a brutal VC critique or trying to find the perfect complementary co-founder to build your startup, this application leverages advanced Local Large Language Models (LLMs) and Vector Databases to provide actionable, data-driven feedback.

## 🚀 Key Features

1. **AI Knowledge Base (Local RAG)**
   - Upload your pitch deck, business plan, or resume (PDF).
   - Powered by **LangChain**, **HuggingFace Embeddings**, and **FAISS**, your documents are securely embedded into a local vector database.
   - Includes robust **Vision & OCR pipelines** (`Tesseract`, `pdf2image`) to automatically extract text even from legacy scanned documents.

2. **Advanced Multi-Stage Pitch Reviewer**
   - Submit your one-sentence pitch to trigger a sequential LLM pipeline powered by a local **Ollama (Llama 3)** model.
   - **Stage 1 (Sentiment):** Analyzes the confidence, clarity, and tone of your pitch.
   - **Stage 2 (VC Critique):** The Virtual Investor acts as a harsh critic, pointing out flaws in your business model based on the uploaded context.
   - **Stage 3 (Reinforcement Coach):** A supportive agent parses the initial analysis and the VC's critique to offer 3 actionable, constructive steps to improve your pitch.

3. **Global Market Insights (External APIs)**
   - Seamlessly integrates with **OpenRouter's REST APIs** via the Python `openai` client.
   - Allows you to query cloud-based models (e.g., Meta Llama 3) for brainstorming alternatives, simulating public opinion, and performing broad market research.

4. **Co-Founder Matchmaking Database**
   - An intelligent matchmaking backend powered by a local **SQLite** database.
   - Stores profiles of prospective founders (Technical, Business, Design, Operations).
   - Utilizes semantic similarity and local LLM logic to analyze your skills and automatically pair you with the best complementary team member.

## 🛠️ Technology Stack

- **Frontend UI:** Streamlit
- **AI/LLM Orchestration:** LangChain (`langchain-ollama`, `langchain-community`)
- **Local AI Models:** Ollama (Llama 3)
- **Vector Database:** FAISS
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Document Processing:** PyPDF, pytesseract, pdf2image
- **Cloud APIs:** OpenRouter (OpenAI Python Client)
- **Database:** SQLite

## 🏗️ Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Khans2002/AI-Founder-Match-And-Pitch-Coach.git
   cd AI-Founder-Match-And-Pitch-Coach
   ```

2. **Set up a virtual environment (Optional but Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For the OCR features, you also need to install `tesseract` and `poppler` on your host machine (e.g., `brew install tesseract poppler` on macOS).*

4. **Ensure Local Models are Running:**
   - Download and install [Ollama](https://ollama.com/).
   - Pull the required model: `ollama run llama3.2:3b`

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a Pull Request if you'd like to improve the prompt engineering, add new database features, or enhance the AI pipelines.

## 📄 License
This project is open-source and available under the terms of the [MIT License](LICENSE).
