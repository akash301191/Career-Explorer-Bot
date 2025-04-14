# Career Explorer Bot

Career Explorer Bot is a smart Streamlit application that helps you discover personalized career paths based on your education, skills, interests, and goals. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot searches the web for relevant opportunities and generates a tailored, Markdown-formatted career guidance report just for you.

## Folder Structure

```
Career-Explorer-Bot/
├── career-explorer-bot.py
├── README.md
└── requirements.txt
```

- **career-explorer-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Career Preferences Input**  
  Fill out your education level, experience, work style, interest areas, tasks you enjoy, skills you're building, and strengths.

- **AI-Powered Career Research**  
  The Career Researcher agent creates a focused Google search using SerpAPI based on your inputs and fetches relevant resources from the web.

- **Personalized Career Report**  
  The Career Advisor agent reads those resources and generates a career report with paths matched to your profile, including skills, roles, and learning links.

- **Structured Markdown Output**  
  Your report is presented in clean Markdown format with section headers, bullet points, and embedded hyperlinks.

- **Download Option**  
  Download the career report as a `.txt` file for future reference or sharing.

- **Clean Streamlit UI**  
  Built with Streamlit to ensure an intuitive, responsive, and distraction-free user experience.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Career-Explorer-Bot.git
   cd Career-Explorer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run career-explorer-bot.py
   ```

2. **In your browser**:
   - Add your OpenAI and SerpAPI keys in the sidebar.
   - Fill out your background, interests, and preferences.
   - Click **🔍 Explore Career Paths**.
   - View and download your personalized AI-generated career report.

3. **Download Option**  
   Use the **📥 Download Career Report** button to save your guidance as a `.txt` file.

---

## Code Overview

- **`render_career_inputs()`**: Captures user background, preferences, and strengths.
- **`render_sidebar()`**: Stores and manages OpenAI and SerpAPI keys in Streamlit session state.
- **`generate_career_report()`**:  
  - Uses the `Career Researcher` agent to search for career insights via SerpAPI.  
  - Sends results to the `Career Advisor` agent to generate a structured Markdown report.
- **`main()`**: Handles layout, collects inputs, and manages the end-to-end flow for report generation.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your changes are clean, well-tested, and aligned with the app’s purpose.