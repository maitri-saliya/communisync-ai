import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client

from database import SessionLocal
from models import Issue
from ai_engine import classify_issue

from teams import (
    TEAM_NUMBERS,
    DEFAULT_TEAM,
    DEFAULT_NUMBER
)

# --------------------
# LOAD ENV
# --------------------

load_dotenv()

# --------------------
# PAGE
# --------------------

st.set_page_config(
    page_title="CommuniSync",
    page_icon="🌍",
    layout="wide"
)

# --------------------
# DB
# --------------------

db = SessionLocal()

# --------------------
# TWILIO
# --------------------

twilio = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# --------------------
# PARSER
# --------------------

def extract(text, field):

    for line in text.splitlines():

        line = line.strip()

        if line.lower().startswith(
            field.lower()
        ):

            return (
                line
                .split(
                    ":",
                    1
                )[1]
                .strip()
            )

    return None


# --------------------
# SEND MESSAGE
# --------------------

def notify(
    request_id,
    team,
    issue,
    priority,
    action
):

    phone = TEAM_NUMBERS.get(
        team,
        DEFAULT_NUMBER
    )

    actual_team = (
        team
        if team in TEAM_NUMBERS
        else DEFAULT_TEAM
    )

    try:

        twilio.messages.create(

            from_=os.getenv(
                "TWILIO_WHATSAPP_NUMBER"
            ),

            to=phone,

            body=f"""
🚨 CommuniSync

Request:
{request_id}

Assigned:
{actual_team}

Issue:
{issue}

Priority:
{priority}

Suggested:
{action}
"""
        )

    except Exception as e:

        print(
            "Twilio:",
            e
        )

    return actual_team


# --------------------
# LOAD DATA
# --------------------

issues = (
    db.query(
        Issue
    )
    .all()
)


# --------------------
# HEADER
# --------------------

st.title(
    "🌍 CommuniSync Command Center"
)

st.caption(
    "Making getting help as easy as texting a friend"
)

st.divider()


# --------------------
# METRICS
# --------------------

total = len(issues)

pending = len(
    [
        x
        for x in issues
        if x.status == "Pending"
    ]
)

active = len(
    [
        x
        for x in issues
        if x.status == "In Progress"
    ]
)

resolved = len(
    [
        x
        for x in issues
        if x.status == "Resolved"
    ]
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📨 Total",
    total
)

c2.metric(
    "🟡 Pending",
    pending
)

c3.metric(
    "🔵 Active",
    active
)

c4.metric(
    "🟢 Resolved",
    resolved
)

st.divider()


# --------------------
# SUBMIT REQUEST
# --------------------

st.subheader(
    "💬 Submit Community Request"
)

with st.form(
    "submit_request"
):

    message = st.text_area(
        "Describe issue",
        placeholder="Streetlight broken near gate..."
    )

    send = st.form_submit_button(
        "🚀 Send Request"
    )


if send and message:

    result = classify_issue(
        message
    )

    category = (
        extract(
            result,
            "Category"
        )
        or
        "General"
    )

    priority = (
        extract(
            result,
            "Priority"
        )
        or
        "Medium"
    )

    team = (
        extract(
            result,
            "Assigned Team"
        )
        or
        DEFAULT_TEAM
    )

    action = (
        extract(
            result,
            "Suggested Action"
        )
        or
        "Manual review"
    )

    issue = Issue(

        message=message,

        category=category,

        priority=priority,

        assigned_team=team,

        suggested_action=action,

        status="Pending"
    )

    db.add(
        issue
    )

    db.commit()

    db.refresh(
        issue
    )

    request_id = (
        f"CS-{issue.id}"
    )

    routed = notify(

        request_id,

        team,

        message,

        priority,

        action
    )

    st.success(
f"""
Request Submitted ✓

Request ID:
{request_id}

Category:
{category}

Priority:
{priority}

Directed To:
{routed}

Suggested Action:
{action}
"""
    )

    st.rerun()


st.divider()


# --------------------
# LIVE REQUESTS
# --------------------

st.subheader(
    "🚨 Live Requests"
)

if issues:

    latest = issues[-1]

    st.markdown(
        "### 🔴 Latest Request"
    )

    with st.container():

        col1, col2 = st.columns(2)

        col1.write(
            f"**Issue**\n\n{latest.message}"
        )

        col1.write(
            f"Category: {latest.category}"
        )

        col1.write(
            f"Priority: {latest.priority}"
        )

        col2.write(
            f"Assigned Team: {latest.assigned_team}"
        )

        col2.write(
            f"Suggested Action: {latest.suggested_action}"
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
                latest.status
            )
        )

        if st.button(
            "Save Status"
        ):

            latest.status = status

            db.commit()

            st.success(
                "Updated"
            )

    st.divider()

    st.markdown(
        "### 📋 Previous Requests"
    )

    for i in reversed(
        issues[:-1]
    ):

        with st.expander(
            f"CS-{i.id} • {i.priority}"
        ):

            st.write(
                f"Issue: {i.message}"
            )

            st.write(
                f"Category: {i.category}"
            )

            st.write(
                f"Assigned: {i.assigned_team}"
            )

            st.write(
                f"Action: {i.suggested_action}"
            )


else:

    st.info(
        "No requests yet"
    )


# --------------------
# TABLE
# --------------------

st.divider()

st.subheader(
    "📊 Request Registry"
)

rows = []

for i in issues:

    rows.append({

        "Request":
        f"CS-{i.id}",

        "Issue":
        i.message,

        "Category":
        i.category,

        "Priority":
        i.priority,

        "Team":
        i.assigned_team,

        "Status":
        i.status
    })


if rows:

    st.dataframe(

        pd.DataFrame(
            rows
        ),

        use_container_width=True
    )


db.close()