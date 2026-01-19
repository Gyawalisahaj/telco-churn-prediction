"""
Streamlit App Entry Point for Cloud Deployment
This file serves as the main entry point for Streamlit Community Cloud
It properly handles module imports for different deployment environments
"""

import sys
from pathlib import Path

# Add src directory to path so imports work correctly
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now import and run the UI
from ui import *  # noqa: F401, F403
