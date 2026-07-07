# Contributing to ResearchLens AI

First off, thank you for considering contributing to ResearchLens AI! Contributions make the open-source community an amazing place to learn, inspire, and create.

All types of contributions are welcome:
- Bug reports & feature requests (raised as GitHub Issues).
- Code contributions (submitted as Pull Requests).
- Documentation improvements.

---

## Local Development Setup

To set up a local development environment:

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ResearchLens-AI.git
   cd ResearchLens-AI
   ```

2. **Set up a Virtual Environment**:
   - **On Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.template` to `.env` and fill in your actual API keys:
   ```bash
   # Windows PowerShell
   Copy-Item .env.template .env
   
   # macOS/Linux/Git Bash
   cp .env.template .env
   ```

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## Running Tests

We write unit tests to keep our backend algorithms stable. We use `pytest` for automated testing.

Before submitting code, ensure that all tests pass:
```bash
python -m pytest tests/
```

---

## Submission Process

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with descriptive, concise commit messages.
3. Push your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request targeting the `main` or `master` branch. Ensure that the automated Continuous Integration (CI) checks pass.
