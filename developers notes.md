AI IDE:

1. What is the AI Pitch Coach Project? 🚀
It is a Web Application built entirely in Python. The Use Case: Imagine a startup founder who wants to pitch their idea to a strict investor. They are nervous and need practice. They can open our website, upload their "Pitch Deck" (PDF), and then speak their pitch into the microphone. The AI acts as a "Virtual Investor" by analyzing their sentiment (how confident they sound) and the actual logic of their idea. It gives them instant feedback, brainstorms improvements, and can even match them with other founders in the database!

2. How are we going to build it? (The Tech Stack) ⚙️
Python: The core coding language (perfect for your Prompt Engineering skills).
Streamlit: A magic framework that turns Python scripts into beautiful, interactive websites almost instantly, without needing complex React or Javascript!
LangChain & Ollama: The "Brain". LangChain is the logic that connects your code to Ollama (which runs local, offline LLMs natively on your Mac).
Speech-to-Text (STT) & Text-to-Speech (TTS): To make it easy and open-source, we will use Python's SpeechRecognition library (to hear the user) and pyttsx3 or Google TTS (to make the AI talk back).
3. What is RAG? (Teaching Moment) 📚
RAG stands for Retrieval-Augmented Generation. Normally, if you ask an AI about your specific startup, it hallucinates because your startup wasn't in its training data. With RAG, when a user uploads their Pitch Deck PDF, we run OCR/Extraction to get the text, slice it into paragraphs, and store them in a local "Vector Database". When the user asks the AI a question, we first Search the database for the relevant paragraph, physically paste that paragraph into the Prompt unseen by the user, and then ask the LLM to generate the answer. You are "Retrieving" facts to "Augment" the "Generation"!

4. Your First "Test" Question! 🧠
Before you give me permission to start generating the code in your /Volumes/Dr.Khans/Developer/LLM RAG based project workspace, let me test your Prompt Engineering intuition!

If a user speaks to the AI Coach and says: "I want to build an app for tracking dogs, but I have absolutely no money to start."

As an expert Prompt Engineer, how would you write the System Prompt instructing the LLM to act as a harsh but helpful virtual investor to review this specific sentence? What rules and constraints would you write to make the AI sound realistic?

(P.S. I checked your HindIDE macOS build.sh. It is heavily compiling the dense VSCodium C++ Electron layers. It is completely normal for a scratch build native to Apple Silicon to take 2-3 hours depending on thermal limits. We will leave it safely running while we conquer this AI project!)

Blueprint for the upcoming AI Pitch Coach and Founder Matchmaking application.



----------------------------------------------------------------------


prompt engineering:

You are a brutally honest but experienced startup investor and venture capitalist.

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