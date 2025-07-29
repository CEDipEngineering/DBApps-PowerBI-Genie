# Power BI Dashboard Assistant with Databricks Genie

> **Note**: This code is based on the excellent work by [Vivian Xie](https://github.com/vivian-xie-db) and the original [genie_space repository](https://github.com/vivian-xie-db/genie_space/tree/main). We extend our gratitude to Vivian for creating this foundational implementation that demonstrates Databricks Genie API integration.

This repository demonstrates how to create a Power BI dashboard assistant that integrates Databricks' AI/BI Genie Conversation APIs, allowing users to interact with their Power BI dashboards using natural language queries.

## Overview

This app is a modern Dash application featuring a Power BI dashboard embed with an intuitive chat interface powered by Databricks Genie Conversation APIs. The application runs as a Databricks App and provides a seamless experience where users can view their Power BI dashboards while having an AI assistant available to help them understand and analyze the data.

The Databricks Genie Conversation APIs enable you to embed AI/BI Genie capabilities into any application, allowing users to:
- Ask questions about their Power BI dashboard data in natural language
- Get SQL-powered insights without writing code
- Follow up with contextual questions in a conversation thread
- View generated SQL queries and results in an interactive format

## Key Features

- **Power BI Dashboard Embed**: Your Power BI dashboard is embedded as the main content area
- **Sidebar Chat Interface**: Genie assistant is in a collapsible sidebar for easy access
- **Modern Responsive Design**: Clean, responsive design that works on desktop and mobile
- **Powered by Databricks Apps**: Deploy and run directly from your Databricks workspace with built-in security and scaling
- **Zero Infrastructure Management**: Leverage Databricks Apps to handle hosting, scaling, and security
- **Workspace Integration**: Access your data assets and models directly from your Databricks workspace
- **Natural Language Data Queries**: Ask questions about your dashboard data in plain English
- **Stateful Conversations**: Maintain context for follow-up questions
- **Interactive SQL Display**: View and toggle generated SQL queries with syntax highlighting
- **Conversation Management**: Start new chats and navigate between conversation history
- **Customizable Welcome Experience**: Edit welcome messages and suggestion prompts
- **Real-time Feedback**: Thumbs up/down buttons for response quality feedback

## Example Use Case

This demo shows how to create an interactive interface that connects to the Genie API, allowing users to:
1. View their Power BI dashboard in the main area
2. Open the sidebar chat to ask questions about the dashboard data
3. Get AI-powered insights about trends, metrics, and visualizations
4. Ask follow-up questions that maintain context
5. Start new conversations to explore different aspects of the data

## Deploying to Databricks Apps

### Prerequisites
- Set up your Python environment and the [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- Ensure you have access to a Databricks workspace with Genie Spaces enabled
- Have a Power BI dashboard with embed URL ready

### Local Development Setup

1. **Edit in your IDE**
   - Set up your Python environment and the Databricks CLI

2. **Clone this repo locally**
   ```bash
   git clone git@github.com:CEDipEngineering/pbi_genie_app.git
   ```
3. **Sync future edits back to Databricks**
   Remember to edit this path to match your context. I suggest starting with your personal Workspace folder for development, but saving it to a non-personal folder in production.
   ```bash
   databricks sync --watch . /Workspace/Users/carlos.dip@databricks.com/pbi_genie_app
   ```

### Deploy to Databricks Apps

1. **Create the app** (first time only):
   This may take a few minutes, we're creating and starting some compute to be used by the app's frontend.
   ```bash
   databricks apps create powerbi-genie-assistant --description "Power BI Dashboard Assistant with Genie"
   ```

2. **Update the environment variables** in the app.yaml file:
   ```yaml
   command:
   - "python"
   - "app.py"

   env:
   - name: "SPACE_ID"
     value: "your_space_id_here"
   - name: "POWERBI_EMBED_URL"
     value: "your_powerbi_embed_url_here"
   ```

3. **Deploy the app**:
   Remember to edit the path here to match where you synced your code to.
   ```bash
   databricks apps deploy powerbi-genie-assistant --source-code-path /Workspace/Users/carlos.dip@databricks.com/pbi_genie_app
   ```
   You can leave out the full path for subsequent deploys.

4. **Configure permissions**:
   - Grant the service principal `can_run` permission to the Genie space
   - Grant the service principal `can_use` permission to the SQL warehouse that powers Genie
   - Grant the service principal appropriate privileges to the underlying resources (catalog, schema, tables)

   **Note**: For demo purposes, ALL PRIVILEGES are used, but you can be more restrictive with `USE CATALOG` on catalog, `USE SCHEMA` on schema, and `SELECT` on tables for production environments.

5. **Open your app in the browser**. If it doesn't work, check out the logs.

## Power BI Integration

### Setting Up Power BI Embed URL

1. **Get your Power BI embed URL**:
   - Open your Power BI report in the Power BI service
   - Go to **File** > **Embed report** > **Website or portal**
   - Copy the embed URL from the dialog

2. **Configure the embed URL**:
   - Update the `POWERBI_EMBED_URL` environment variable in `app.yaml`
   - The URL should look like: `https://app.powerbi.com/reportEmbed?reportId=xxx&autoAuth=true&ctid=xxx`

3. **Power BI Embed Features**:
   - **Secure Embedding**: Uses Power BI's secure embed option for internal portals
   - **Authentication**: Users need to sign in to view the embedded report
   - **Responsive Design**: The dashboard adapts to different screen sizes
   - **Full Screen Support**: Users can expand the dashboard to full screen

For more information about Power BI embedding, see the [official Microsoft documentation](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure).

### Using the Application

1. **View Dashboard**: The Power BI dashboard is displayed in the main area
2. **Access Assistant**: Click the menu button (☰) to open the Genie chat sidebar
3. **Ask Questions**: Use the chat to ask about your dashboard data
4. **New Chat**: Click the "+" button to start a fresh conversation
5. **Customize**: Edit the welcome message and suggestions via the settings button

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing package or wrong package version | Add to requirements.txt |
| Permissions issue | Give access `app-{app-id}` to the resource |
| Missing environment variable | Add to the env section of app.yaml |
| Running the wrong command line at startup | Add to the command section of app.yaml |
| Power BI embed not loading | Check the embed URL and ensure users have proper Power BI permissions |
| Chat sidebar not working | Verify Genie space permissions and API connectivity |

For additional troubleshooting, navigate to the Genie space monitoring page and check if the query has been sent successfully to the Genie space via the API. Click open the query and check if there is any error or any permission issues.

## Resources

- [Databricks Genie Documentation](https://docs.databricks.com/aws/en/genie)
- [Conversation APIs Documentation](https://docs.databricks.com/api/workspace/genie)
- [Databricks Apps Documentation](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/)
- [Power BI Secure Embed Documentation](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure)