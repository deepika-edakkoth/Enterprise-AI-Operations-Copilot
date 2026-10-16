import streamlit as st
from components.layout import render_page
from config import configure_langsmith

configure_langsmith()
render_page()