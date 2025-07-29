import os

# Default welcome text that can be customized
DEFAULT_WELCOME_TITLE = "Supply Chain Optimization"
DEFAULT_WELCOME_DESCRIPTION = "Analyze your Supply Chain Performance leveraging AI/BI Dashboard. Deep dive into your data and metrics."

# Default suggestion questions
DEFAULT_SUGGESTIONS = [
    "What tables are there and how are they connected? Give me a short summary.",
    "Which distribution center has the highest chance of being a bottleneck?",
    "Explain the dataset",
    "What was the demand for our products by week in 2024?"
]

# Databricks configuration
DATABRICKS_HOST = os.getenv('DATABRICKS_HOST') 