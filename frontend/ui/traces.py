
import os
import streamlit as st
from langsmith import Client


def render_traces():
    st.title("Agent Traces")
    st.caption(
        "Monitor LangChain agent executions, latency, and failures."
    )

    if not os.getenv("LANGSMITH_API_KEY"):
        st.warning("Configure your LangSmith API key to view traces.")
        return

    try:
        client = Client()

        runs = list(
            client.list_runs(
                project_name=os.getenv(
                    "LANGSMITH_PROJECT",
                    "enterprise-ai-copilot",
                ),
                is_root=True,
                limit=20,
            )
        )

        if not runs:
            st.info(
                "No traces found. Run a request through your agent first."
            )
            return

        rows = []

        for run in runs:
            rows.append({
                "Run": run.name,
                "Status": "Failed" if run.error else "Completed",
                "Started": str(run.start_time),
                "Latency (s)": (
                    round(run.latency, 2)
                    if run.latency is not None
                    else None
                ),
                "Trace ID": str(run.id),
            })

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

    except Exception as exc:
        st.error(f"Unable to retrieve traces: {exc}")
