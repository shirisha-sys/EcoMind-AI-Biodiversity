🌿 EcoMind – AI Biodiversity Intelligence System

No life exists alone. No signal stands apart.

EcoMind is an AI-powered biodiversity intelligence system that connects soil health, climate, water, land use, and biodiversity data to generate actionable, science-backed environmental recommendations.

🌍 Key Features

- AI Biodiversity Chatbot: Ask environmental questions and receive contextual insights.
- Environmental Analysis Dashboard: Analyze soil, climate, land use, and biodiversity indicators.
- Retrieval-Augmented Generation (RAG): Retrieve relevant knowledge from a structured biodiversity knowledge base.
- Actionable Recommendations: Get suggested actions, reasons, affected metrics, and time horizons.
- Scientific Grounding: Uses environmental knowledge and references to support recommendations.

🏗️ Tech Stack

- Python
- FastAPI
- HTML, CSS, JavaScript
- JSON-based biodiversity knowledge base
- Retrieval-Augmented Generation (RAG)

📁 Project Structure

EcoMind/
├── backend/
│   └── main.py
├── data/
│   └── biodiversity_knowledge.json
├── frontend/
│   ├── index.html
│   ├── analysis.html
│   ├── chat.html
│   └── login.html
├── rag/
│   └── retriever.py
├── tests/
├── .gitignore
└── README.md

⚙️ Run Locally

1. Clone the repository:

git clone https://github.com/shirisha-sys/EcoMind-AI-Biodiversity.git
cd EcoMind-AI-Biodiversity

2. Create and activate a virtual environment (Windows):

python -m venv venv
venv\Scripts\activate

3. Install dependencies:

pip install fastapi uvicorn python-dotenv

4. Start the application:

python -m uvicorn backend.main:app --reload

5. Open the application:

- Homepage: http://127.0.0.1:8000/
- Environmental Analysis: http://127.0.0.1:8000/analysis.html
- AI Chat: http://127.0.0.1:8000/chat.html
- API Health: http://127.0.0.1:8000/api/health

🧠 Knowledge Base

EcoMind uses a structured JSON knowledge base containing environmental topics, keywords, conditions, evidence, recommendations, affected metrics, and scientific source references.

The RAG retriever matches user queries with relevant knowledge entries to support grounded environmental insights.

🔬 Project Purpose

EcoMind aims to make environmental intelligence more accessible by connecting ecosystem indicators and translating environmental knowledge into practical recommendations.

🚧 Project Status

Developed as a hackathon project for the Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge.

👩‍💻 Author

Sivanna gari shirisha

GitHub: "shirisha-sys" (https://github.com/shirisha-sys)
