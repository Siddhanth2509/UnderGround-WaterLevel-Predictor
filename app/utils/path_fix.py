import sys
import os

def fix_path():
    """
    Adds project root directory to sys.path
    Required for Streamlit multipage apps
    """
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
