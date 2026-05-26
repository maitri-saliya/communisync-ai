import os

import streamlit as st
import pandas as pd

from database import SessionLocal
from models import Issue


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

    key="dashboard_refresh"

):

    st.rerun()


# ----------------------------------
# LOAD DATA
# ----------------------------------

def load_issues():

    db = SessionLocal()

    try:

        return (

            db
            .query(Issue)
            .order_by(
                Issue.id.desc()
            )
            .all()

        )

    finally:

        db.close()


issues = load_issues()


def to_dataframe(data):

    rows = []

    for i in data:

        rows.append({

            "ID": i.id,

            "Message": i.message,

            "Category": i.category,

            "Priority": i.priority,

            "Assigned Team": i.assigned_team,

            "Suggested Action": i.suggested_action,

            "Status": i.status

        })

    return pd.DataFrame(rows)


df = to_dataframe(
    issues
)


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

total = len(
    issues
)

pending = len([

    x

    for x in issues

    if x.status == "Pending"

])

resolved = len([

    x

    for x in issues

    if x.status == "Resolved"

])


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "Total Requests",

        total
    )


with col2:

    st.metric(

        "Pending",

        pending
    )


with col3:

    st.metric(

        "Resolved",

        resolved
    )


st.divider()


# ----------------------------------
# ANALYTICS
# ----------------------------------

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Request Categories"
        )

        st.bar_chart(

            df["Category"]
            .value_counts()

        )

    with col2:

        st.subheader(
            "Priority Distribution"
        )

        st.bar_chart(

            df["Priority"]
            .value_counts()

        )

else:

    st.info(
        "No requests yet"
    )


st.divider()


# ----------------------------------
# REQUESTS
# ----------------------------------

st.header(
    "Community Requests"
)


for issue in issues:

    with st.expander(

        f"Request #{issue.id} • {issue.priority}"

    ):

        st.markdown(

            f"""
**Issue**

{issue.message}
"""
        )

        st.write(

            f"Category: {issue.category}"

        )

        st.write(

            f"Assigned Team: {issue.assigned_team}"

        )

        st.write(

            f"Suggested Action: {issue.suggested_action}"

        )

        status = st.selectbox(

            "Update Status",

            [

                "Pending",

                "In Progress",

                "Resolved"

            ],

            index=[

                "Pending",

                "In Progress",

                "Resolved"

            ].index(

                issue.status

            ),

            key=f"status_{issue.id}"

        )

        if status != issue.status:

            db = SessionLocal()

            try:

                row = (

                    db
                    .query(Issue)
                    .filter(
                        Issue.id == issue.id
                    )
                    .first()

                )

                row.status = status

                db.commit()

                st.success(
                    "Updated"
                )

                st.rerun()

            finally:

                db.close()


st.divider()


# ----------------------------------
# TABLE
# ----------------------------------

st.subheader(
    "Full Issue Table"
)

if not df.empty:

    st.dataframe(

        df,

        use_container_width=True

    )


# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.caption(

"""
CommuniSync

Making getting help as easy as texting a friend.
"""

)


print(

    "DATABASE_URL:",

    os.getenv(
        "DATABASE_URL"
    )

)