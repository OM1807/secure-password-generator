#!/usr/bin/env python3
"""
Password Generator - Main Entry Point

A simple yet powerful command-line tool for generating secure random passwords.
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import main

if __name__ == "__main__":
    main()
