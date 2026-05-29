import streamlit as st
import pandas as pd

from database import SessionLocal
from models import RequestLog


# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(

    page_title="CommuniSync Dashboard",

    page_icon="🌍",

    layout="wide"
)


# ----------------------------------
# REFRESH
# ----------------------------------

if st.button(

    "🔄 Refresh Dashboard",

    key="refresh"
):

    st.rerun()


# ----------------------------------
# LOAD DATA
# ----------------------------------


def load_requests():

    db = SessionLocal()

    try:

        return (
            db.query(RequestLog)
            .order_by(
                RequestLog.id.desc()
            )
            .all()
        )

    finally:

        db.close()


requests = load_requests()


# ----------------------------------
# HEADER
# ----------------------------------

st.title(
    "🌍 CommuniSync Dashboard"
)

st.caption(
    "AI-Powered Community Coordination"
)

st.divider()


# ----------------------------------
# METRICS
# ----------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Requests",
        len(requests)
    )


with col2:

    st.metric(
        "Pending",
        len([
            x
            for x in requests
            if x.status == "Pending"
        ])
    )


with col3:

    st.metric(
        "Resolved",
        len([
            x
            for x in requests
            if x.status == "Resolved"
        ])
    )


st.divider()


# ----------------------------------
# TABLE
# ----------------------------------

rows = []

for r in requests:

    rows.append({

        "ID": r.id,

        "Category": r.category,

        "Priority": r.priority,

        "Team": r.assigned_team,

        "Status": r.status,

        "Description": r.description
    })


if rows:

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No requests yet"
    )
