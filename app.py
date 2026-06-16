import streamlit as st
import pandas as pd
from visuals import create_analysis_dashboard
from file1 import run_data_mining
from comment_generation import generate_human_like_comment


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Blog Intelligence System",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "keyword" not in st.session_state:
    st.session_state.keyword = ""

if "df" not in st.session_state:
    st.session_state.df = None


# =========================================================
# GLOBAL STYLE
# =========================================================
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #1f4e79;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 20px;
}

.card {
    padding: 18px;
    border-radius: 14px;
    background-color: #1e293b;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    margin-bottom: 10px;
}

.comment-box {
    padding: 18px;
    border-radius: 12px;
    background-color: #1e293b;
    font-size: 16px;
    border-left: 5px solid #1f4e79;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HOME PAGE (SAAS LANDING STYLE)
# =========================================================
if st.session_state.page == "home":

    st.markdown('<div class="main-title">🧠 AI Blog Intelligence System</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Scrape • Analyze • Understand • Generate AI Insights</div>',
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
        use_container_width=True
    )

    st.markdown("### 🚀 Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        🔍 <b>Smart Scraping</b><br>
        Extract blogs dynamically from the web
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        📊 <b>NLP Engine</b><br>
        Sentiment, topic modeling, keyword extraction
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        🤖 <b>AI Comments</b><br>
        Generate human-like responses using LLM
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🚀 Start Analysis", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()


# =========================================================
# INPUT PAGE
# =========================================================
elif st.session_state.page == "input":

    st.title("🔎 Enter Keyword")

    keyword = st.text_input("Enter keyword (e.g. AI, Python, Blockchain)")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Pipeline", use_container_width=True):

            if keyword.strip() == "":
                st.warning("Please enter a keyword.")
            else:
                st.session_state.keyword = keyword
                st.session_state.page = "processing"
                st.rerun()

    with col2:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


# =========================================================
# PROCESSING PAGE (RUN ONCE ONLY)
# =========================================================
elif st.session_state.page == "processing":

    st.title("⚙️ AI Processing Pipeline")

    keyword = st.session_state.keyword

    st.info(f"Processing keyword: **{keyword}**")

    progress = st.progress(0)
    log_box = st.empty()

    def progress_callback(step, message, percent):
        log_box.write(message)
        progress.progress(percent)

    with st.status("Running AI Pipeline...", expanded=True):

        run_data_mining(keyword, progress_callback)

    # Load CSV ONCE
    try:
        df = pd.read_csv("analyzed_blogs.csv")
        st.session_state.df = df
    except:
        st.error("❌ CSV not generated.")
        st.stop()

    st.success("✅ Pipeline Completed")

    st.session_state.page = "results"
    st.rerun()


# =========================================================
# RESULTS PAGE (FULL PROFESSIONAL DASHBOARD)
# =========================================================
elif st.session_state.page == "results":

    st.markdown('<div class="main-title">📊 AI Insights Dashboard</div>', unsafe_allow_html=True)

    df = st.session_state.df

    if df is None or df.empty:
        st.error("No data available")
        st.stop()

    # ---------------- BLOG LIST ----------------
    st.subheader("📄 Analyzed Blogs")

    for _, row in df.iterrows():

        with st.expander(f"📌 {row['title']}"):

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.write("🔗 URL:", row["url"])
            st.write("👤 Author:", row["author"])
            st.write("📅 Date:", row["date"])
            st.write("🧠 Summary:", row["summary"])
            st.write("🎯 Motive:", row["motive"])
            st.write("🎭 Tone:", row["tone"])
            st.write("💬 Comments:", row["comment_count"])
            st.write("😊 Sentiment:", row["sentiment"])
            st.write("🏷 Topic:", row["topic_theme"])

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Visual Analytics")
    create_analysis_dashboard(df.to_dict("records"))

    st.markdown("---")

    # =====================================================
    # AI COMMENT GENERATION (FIXED + PROFESSIONAL)
    # =====================================================
    st.subheader("🤖 AI Comment Generator")

    col1, col2 = st.columns([1, 3])

    with col1:
        generate = st.button("💬 Generate Comment", use_container_width=True)

    with col2:
        st.info("Generates a human-like comment from your analyzed blogs")

    if generate:

        with st.spinner("🧠 AI is generating comment..."):

            comment, meta = generate_human_like_comment(df)

            if comment == "":
                st.error(meta.get("error", "Generation failed"))
            else:
                st.success("Generated Comment")

                st.markdown(
                    f"""
                    <div class="comment-box">
                        {comment}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.info(f"📌 Blog: {meta.get('title','Unknown')}")

    st.markdown("---")

    # ---------------- NAVIGATION ----------------
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()