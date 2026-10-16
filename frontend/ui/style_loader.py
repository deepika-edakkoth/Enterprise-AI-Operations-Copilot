
from pathlib import Path
import streamlit as st


FRONTEND_DIR = Path(__file__).resolve().parents[1]
STYLES_DIR = FRONTEND_DIR / "styles"


def load_css(filename: str) -> None:
    css_path = STYLES_DIR / filename
    css = css_path.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
