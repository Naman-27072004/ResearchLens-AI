# ResearchLens AI

AI-Powered Research Paper Analysis using Gemini + RAG.

## Features
- **PDF Upload**: Parse and extract text from research papers.
- **AI Analysis**: Get structured executive summaries, key findings, gaps, and more.
- **RAG Chat**: Interact and chat with the uploaded papers.
- **Multi-Paper Comparison**: Compare multiple papers side-by-side.
- **Research Gap Detection**: Identify potential areas for new research.
- **Citation Analytics**: Extract and analyze citations.

## Setup and Running

Follow these steps to run the application locally on Windows:

### 1. Activate the Virtual Environment
Open your terminal in the project directory and run:

- **PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Command Prompt (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```

### 2. Install Dependencies
Ensure you have the virtual environment activated, then install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key
Copy the template environment file to `.env`:
- **PowerShell**:
  ```powershell
  Copy-Item .env.template .env
  ```
- **CMD**:
  ```cmd
  copy .env.template .env
  ```

Open the newly created `.env` file and replace `"your_gemini_api_key_here"` with your actual Google Gemini API Key:
```env
GEMINI_API_KEY="AIzaSy..."
```

### 4. Run the Application
Start the Streamlit server:
```bash
streamlit run app.py
```

The app will open automatically in your default browser (usually at `http://localhost:8501`).

## Running Tests

Automated tests are set up inside the `tests/` directory. You can run them using `pytest` inside the activated virtual environment:
```bash
python -m pytest tests/
```
