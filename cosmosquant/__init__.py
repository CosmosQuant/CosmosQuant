"""
CosmosQuant - A comprehensive quantitative trading framework.
"""

__version__ = "0.1.0"
__author__ = "CosmosQuant"
__description__ = "A comprehensive quantitative trading framework"

# Import the core modules from the nested package
from cosmosquant.cosmosquant import engine, brokers, datasources, strategies, utils

__all__ = [
    "engine",
    "brokers", 
    "datasources",
    "strategies",
    "utils"
]