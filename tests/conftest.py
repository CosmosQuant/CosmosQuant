"""Test configuration file."""

import sys
from pathlib import Path

# Add the cosmosquant package to the Python path for testing
cosmosquant_path = Path(__file__).parent.parent / "cosmosquant"
sys.path.insert(0, str(cosmosquant_path))