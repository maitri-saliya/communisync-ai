import streamlit as st

from streamlit_autorefresh import st_autorefresh

from database import SessionLocal
from models import Issue

# -------------------------------------
# PAGE CONFIG
# -------------------------------------

st.set_page_config(
    page_title="CommuniSync AI",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------------
# AUTO REFRESH
# -------------------------------------

st_autorefresh(interval=3000, key="refresh")

# -------------------------------------
# STYLING
# -------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------
# DATABASE
# -------------------------------------

db = SessionLocal()

issues = db.query(Issue).all()

# -------------------------------------
# HEADER
# -------------------------------------

st.title("🌍 CommuniSync AI")

st.subheader(
    "AI-Powered Hyperlocal Community Coordination Platform"
)

st.markdown("""
### Making community help as easy as texting a friend.
""")

st.divider()

# -------------------------------------
# METRICS
# -------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Issues", len(issues))

with col2:

    resolved = len([
        i for i in issues
        if i.status == "Resolved"
    ])

    st.metric("Resolved", resolved)

with col3:
    st.metric("Avg Response Time", "3 mins")

with col4:
    st.metric("Community Engagement", "87%")

st.divider()

# -------------------------------------
# LIVE DASHBOARD
# -------------------------------------

st.header("📊 Live Community Dashboard")

if len(issues) == 0:

    st.info("No active community issues.")

else:

    for issue in reversed(issues):

        st.markdown(f"""
### 📝 Request #{issue.id}

**Message:**  
{issue.message}

**Category:** {issue.category}

**Priority:** {issue.priority}

**Assigned Team:** {issue.assigned_team}

**Status:** {issue.status}
""")

        st.divider()

# -------------------------------------
# IMPACT SECTION
# -------------------------------------

st.header("📈 Community Impact")

left, right = st.columns(2)

with left:

    st.markdown("""
### Before CommuniSync AI

- Delayed issue reporting
- Manual routing
- No visibility
- Slow response cycles
- Disconnected communities
""")

with right:

    st.markdown("""
### After CommuniSync AI

- Instant AI routing
- Faster issue resolution
- Real-time tracking
- Better community engagement
- Hyperlocal collaboration
""")

st.divider()

# -------------------------------------
# AI SUMMARY
# -------------------------------------

st.header("🧠 AI Community Summary")

if st.button("Generate Daily AI Summary"):

    total = len(issues)

    resolved_count = len([
        i for i in issues
        if i.status == "Resolved"
    ])

    pending_count = len([
        i for i in issues
        if i.status == "Pending"
    ])

    st.success(f"""
Today, CommuniSync AI processed {total} community requests.

✅ {resolved_count} issues resolved
⏳ {pending_count} issues pending

AI-powered routing improved community response efficiency.
""")

# -------------------------------------
# RESPONSIBLE AI
# -------------------------------------

st.divider()

st.header("🔒 Responsible AI & Privacy")

st.markdown("""
- No personal data selling
- Privacy-aware routing
- Human-controlled issue resolution
- AI used for assistance only
- Mock/synthetic data for prototype
""")

# -------------------------------------
# FOOTER
# -------------------------------------

st.divider()

st.caption("""
CommuniSync AI • Smart Communities Through Human-Centered AI
""")

db.close()