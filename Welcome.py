# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 15:01:26 2022

@author: Huzihu
"""

import streamlit as st

st.set_page_config(
    page_title="Welcome to Our Tennis Analytics Tool",
    page_icon="👋",
)

st.title("Welcome to Our Tennis Analytics Tool! 👋")

st.markdown(
    """
    Tennis Analytics Tool is an app framework built specifically for
    Tennis Coaches and Players.
    **👈 Select a tab from the sidebar** to use our three main functions!
    ### Table of Contents:
    - Tab 1: General Statistics
    - Tab 2: Player Scheduling Optimization
    - Tab 3: Match Analysis
"""
)
    
# streamlit run Welcome.py