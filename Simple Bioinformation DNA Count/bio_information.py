import pandas as pd
import streamlit as st
import altair as alt

st.header("DNA Count Application")

input_sequence = st.text_area("Enter DNA Sequence", placeholder= "Type or paste your DNA sequence here...")