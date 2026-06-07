"""Main entry point for Streamlit deployment."""

# This file serves as the main entry point for Streamlit Community Cloud
# It imports and runs the basic version of the app for demo purposes

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import the main application
from app_basic import main

if __name__ == "__main__":
    main()