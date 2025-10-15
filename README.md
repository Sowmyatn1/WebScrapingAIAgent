# 🧠 GenAI SQL Chatbot using webscraping ,LangChain, SQLite, and Streamlit

This project is an intelligent chatbot that connects to a **SQLite database** and answers natural language questions using **LangChain**, **LLMs**, and **SQL agents**.  
It can reason over SQL query results to provide concise and accurate answers.

---

## 🚀 Features

- 💬 **Natural Language to SQL**: Ask questions like  
  *"Is Dr. B. L. Avinash available on 2025-10-15 at 1:00 PM?"*  
  The agent automatically converts this into SQL and fetches the answer.

- 🧩 **RAG-like Reasoning**: SQL output is passed to another LLM for reasoning to generate human-like responses.

- 🗃️ **SQLite Database**: Stores doctor details, availability, and appointment slots.

- 🧠 **LangChain Integration**: Uses LangChain’s `SQLDatabaseToolkit` and `create_sql_agent` for intelligent query execution.

- 🖥️ **Streamlit UI**: Simple web interface to interact with the chatbot.

---

## 🏗️ Project Structure

📂 genai-sql-chatbot
│
├── sqlagent.py # Core logic – handles SQL agent + reasoning LLM
├── app.py # Streamlit UI
├── doctors.db # SQLite database
├── requirements.txt # Dependencies
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation

### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/genai-sql-chatbot.git
cd genai-sql-chatbot



### 2️⃣ Create a virtual environment

python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows


### 3️⃣ Install dependencies

pip install -r requirements.txt
Example requirements.txt:


streamlit
langchain
langchain-community
langchain-openai
openai
sqlite3
python-dotenv


### 4️⃣ Add your OpenAI API key
Create a .env file in your root folder:


OPENAI_API_KEY=your_api_key_here


## 🧠 How It Works
The user asks a natural question via the Streamlit interface.

LangChain’s SQL Agent converts it to a structured SQL query.

The query is executed against the SQLite database.

The SQL result is passed to a reasoning LLM, which forms a natural-language response.

The chatbot displays the final answer in the UI.

## 💻 Running the App
Run the Streamlit app:

streamlit run app.py
Then open the URL shown in the terminal (usually http://localhost:8501).

