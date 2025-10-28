#!/usr/bin/env python3
"""
GUI Password Generator - Main Entry Point

Launch the graphical user interface for the password generator.
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui import main

if __name__ == "__main__":
    main()
