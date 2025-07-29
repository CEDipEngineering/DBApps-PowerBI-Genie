import os

# Default welcome text that can be customized
DEFAULT_WELCOME_TITLE = "Power BI Dashboard Assistant"
DEFAULT_WELCOME_DESCRIPTION = "Ask questions about your Power BI dashboard data and get AI-powered insights. The Genie assistant can help you understand trends, analyze metrics, and explore your data."

# Default suggestion questions
DEFAULT_SUGGESTIONS = [
    "What are the key insights from this dashboard?",
    "Can you explain the trends shown in the charts?",
    "What are the main metrics being displayed?",
    "How can I interpret the data visualizations?"
]

# Databricks configuration
DATABRICKS_HOST = os.getenv('DATABRICKS_HOST')

# Power BI configuration
POWERBI_EMBED_URL = os.getenv('POWERBI_EMBED_URL', 'https://app.powerbi.com/reportEmbed?reportId=25baf2c4-2cc6-434d-94c1-157650590c23&autoAuth=true&ctid=9f37a392-f0ae-4280-9796-f1864a10effc') 