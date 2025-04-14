import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_career_inputs():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Background & Education
    with col1:
        st.subheader("🎓 Education & Experience")
        education = st.selectbox(
            "Current Education Level*",
            ["Middle School", "High School", "Undergraduate", "Graduate", "Postgraduate", "Other"]
        )
        work_experience = st.selectbox(
            "Work Experience*",
            ["No experience", "Internship(s)", "1–2 years", "3–5 years", "5+ years"]
        )
        work_environment = st.selectbox(
            "Preferred Work Environment*",
            ["Office-based", "Remote/Flexible", "Field-based", "Lab/Studio", "No preference"]
        )

    # Column 2: Interests & Tasks
    with col2:
        st.subheader("💡 Interests & Tasks")
        interest_areas = st.multiselect(
            "Which areas interest you most?*",
            ["Technology", "Design & Creativity", "Business & Finance", "Science & Research", 
             "Health & Medicine", "Education", "Law & Public Policy", 
             "Environment & Sustainability", "Social Impact / NGOs"]
        )
        preferred_tasks = st.multiselect(
            "What kind of tasks do you enjoy? (Pick top 3)",
            ["Solving problems", "Building things", "Analyzing data", "Writing/storytelling",
             "Designing visuals", "Teaching/explaining", "Organizing/planning", "Helping others", "Leading teams"]
        )
        learning_goals = st.text_input("Skills you’re learning or want to learn (optional)", placeholder="e.g., Python, UI design, Data Analysis")

    # Column 3: Strengths & Preferences
    with col3:
        st.subheader("🚀 Strengths & Priorities")
        strengths = st.multiselect(
            "What are your current strengths? (Pick top 3–5)",
            ["Coding/Programming", "Communication", "Logical Reasoning", "Public Speaking",
             "Creativity", "Attention to Detail", "Research/Writing", 
             "Project Management", "Leadership", "Empathy"]
        )
        career_goals = st.radio(
            "Do you prefer specialization or variety?",
            ["Deep specialization", "Generalist (multiple domains)", "Not sure yet"]
        )
        regions = st.text_input("Preferred countries/regions to work in (optional)", placeholder="e.g., USA, Germany, Remote")

    # Assemble user career profile
    career_profile = f"""
    **Education & Background:**
    - Education Level: {education}
    - Experience: {work_experience}
    - Work Environment Preference: {work_environment}

    **Interests & Goals:**
    - Interest Areas: {', '.join(interest_areas) if interest_areas else 'Not specified'}
    - Tasks Enjoyed: {', '.join(preferred_tasks) if preferred_tasks else 'Not specified'}
    - Skills to Learn: {learning_goals if learning_goals.strip() else 'Not specified'}

    **Skills & Strengths:**
    - Strengths: {', '.join(strengths) if strengths else 'Not specified'}
    - Career Preference: {career_goals}
    - Work Regions: {regions if regions.strip() else 'Not specified'}
    """

    return career_profile

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def generate_career_report(user_career_profile: str) -> str:
    # Step 1: Run Career Researcher Agent
    research_agent = Agent(
        name="Career Researcher",
        role="Finds career paths, job roles, and skill-based opportunities based on user interests and strengths.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a career research expert. Given a detailed user profile including their education, experience, strengths, and preferences,
            your job is to suggest potential career paths that match their inputs.
            You will generate a focused, real-world search query, search the web, and extract the 10 most relevant career-related links.
        """),
        instructions=[
            "Carefully read the user's career profile to understand their interests, skills, values, and goals.",
            "Based on this, generate ONE concise and targeted search term (e.g., 'creative career options for design enthusiasts with strong writing skills' or 'best careers for analytical thinkers with a science background').",
            "Avoid overly broad or vague queries. Keep the term focused on the most important aspects of the user's input.",
            "Use `search_google` with this search term.",
            "From the search results, extract the top 10 most relevant links or summaries that provide useful and actionable career information.",
            "Prioritize links that contain specific roles, required skills, career paths, growth outlooks, or success stories aligned with the user profile.",
            "Do not fabricate or invent information. Only use what’s found in the search results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = research_agent.run(user_career_profile)
    research_results = research_response.content

    # Step 2: Run Career Advisor Agent
    advisor_agent = Agent(
        name="Career Advisor",
        role="Creates a personalized career guidance report based on user preferences and curated career resources.",
        model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a professional career advisor. Your task is to generate a comprehensive career exploration report.
            
            You are given:
            1. A structured summary of the user's education, experience, strengths, and preferences.
            2. A list of URLs or summaries extracted from online research on suitable career options.
            
            Your job is to match career paths to the user’s interests, goals, and strengths.
        """),
        instructions=[
            "Carefully analyze the user's career profile. Pay attention to:",
            "- Education level and work experience.",
            "- Key interest areas and preferred work environment.",
            "- Tasks they enjoy doing and skills they want to learn.",
            "- Personal strengths and career preferences (e.g., remote work, generalist/specialist).",
            "- Any geographic or practical constraints mentioned.",

            "Now review the research links provided. Use only insights from those resources to suggest:",
            "- Suitable career paths with short, clear descriptions.",
            "- Key skills required for each path.",
            "- Typical job titles or roles under each career.",
            "- Notes on job growth, flexibility, remote-friendliness, or regional demand.",
            "- Real-world examples, platforms, or training resources (if available).",

            "Format the final career report using clean, structured Markdown.",
            "Use this format exactly:",

            "## Recommended Career Paths",
            "",
            "### [Career Title]",
            "- **Summary:** Short overview of the career path.",
            "- **Key Skills:** Bullet list of required or helpful skills.",
            "- **Typical Roles:** Job titles or entry points.",
            "- **Learning Resources:** Use proper Markdown format for links, e.g., [LinkedIn Career Guide](https://linkedin.com/...).",
            "- **Notes from Research:** Trends, regional relevance, or flexibility from the sources.",

            "Do not fabricate or assume any information. Only use what is present in the research results.",
            "Ensure the tone is helpful, the structure is clear, and the advice is actionable and aligned with the user's goals.",
        ],
        add_datetime_to_instructions=True,
    )

    advisor_input = f"""
    User's Career Profile:
    {user_career_profile}

    Research Results:
    {research_results}

    Use these details to generate a personalized career guidance report.
    """

    advisor_response = advisor_agent.run(advisor_input)
    career_report = advisor_response.content

    return career_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Career Explorer Bot", page_icon="🎯", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🎯 Career Explorer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Career Explorer Bot — a smart Streamlit application that uses your strengths, passions, and preferences, as well as current market conditions to recommend personalized career options.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_career_profile = render_career_inputs()

    st.markdown("---")

    if st.button("🔍 Explore Career Paths"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Generating your personalized career guidance report..."):
                career_report = generate_career_report(user_career_profile=user_career_profile)
                st.session_state.career_report = career_report

    if "career_report" in st.session_state:
        st.markdown(st.session_state.career_report, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Career Report",
            data=st.session_state.career_report,
            file_name="career_guidance_report.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()