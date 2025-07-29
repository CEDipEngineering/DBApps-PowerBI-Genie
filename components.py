from dash import html, dcc, dash_table
import pandas as pd
from config import DEFAULT_WELCOME_TITLE, DEFAULT_WELCOME_DESCRIPTION, DEFAULT_SUGGESTIONS
from utils import format_sql_query

def create_user_message(user_input):
    """Create a user message component"""
    return html.Div([
        html.Div([
            html.Div("Y", className="user-avatar"),
            html.Span("You", className="model-name")
        ], className="user-info"),
        html.Div(user_input, className="message-text")
    ], className="user-message message")

def create_thinking_indicator():
    """Create a thinking indicator component"""
    return html.Div([
        html.Div([
            html.Span(className="spinner"),
            html.Span("Thinking...")
        ], className="thinking-indicator")
    ], className="bot-message message")

def create_data_table(df, table_id):
    """Create a data table component"""
    return dash_table.DataTable(
        id=table_id,
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        
        # Other table properties
        page_size=10,
        style_table={
            'display': 'inline-block',
            'overflowX': 'auto',
            'width': '95%',
            'marginRight': '20px'
        },
        style_cell={
            'textAlign': 'left',
            'fontSize': '12px',
            'padding': '4px 10px',
            'fontFamily': '-apple-system, BlinkMacSystemFont,Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif',
            'backgroundColor': 'transparent',
            'maxWidth': 'fit-content',
            'minWidth': '100px'
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'fontWeight': '600',
            'borderBottom': '1px solid #eaecef'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        fill_width=False,
        page_current=0,
        page_action='native'
    )

def create_query_section(query_text, query_index):
    """Create a query section component"""
    if query_text is None:
        return None
    
    formatted_sql = format_sql_query(query_text)
    
    return html.Div([
        html.Div([
            html.Button([
                html.Span("Show code", id={"type": "toggle-text", "index": query_index})
            ], 
            id={"type": "toggle-query", "index": query_index}, 
            className="toggle-query-button",
            n_clicks=0)
        ], className="toggle-query-container"),
        html.Div([
            html.Pre([
                html.Code(formatted_sql, className="sql-code")
            ], className="sql-pre")
        ], 
        id={"type": "query-code", "index": query_index}, 
        className="query-code-container hidden")
    ], id={"type": "query-section", "index": query_index}, className="query-section")

def create_bot_response(content, chat_history_index):
    """Create a bot response component"""
    return html.Div([
        html.Div([
            html.Div(className="model-avatar"),
            html.Span("Genie", className="model-name")
        ], className="model-info"),
        html.Div([
            content,
            html.Div([
                html.Div([
                    html.Button(
                        id={"type": "thumbs-up-button", "index": chat_history_index},
                        className="thumbs-up-button"
                    ),
                    html.Button(
                        id={"type": "thumbs-down-button", "index": chat_history_index},
                        className="thumbs-down-button"
                    )
                ], className="message-actions")
            ], className="message-footer")
        ], className="message-content")
    ], className="bot-message message")

def create_error_response(error_msg):
    """Create an error response component"""
    return html.Div([
        html.Div([
            html.Div(className="model-avatar"),
            html.Span("Genie", className="model-name")
        ], className="model-info"),
        html.Div([
            html.Div(error_msg, className="message-text")
        ], className="message-content")
    ], className="bot-message message")

def create_welcome_modal():
    """Create the welcome customization modal"""
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Customize Welcome Message")),
        dbc.ModalBody([
            html.Div([
                html.Label("Welcome Title", className="modal-label"),
                dbc.Input(
                    id="welcome-title-input",
                    type="text",
                    placeholder="Enter a title for your welcome message",
                    className="modal-input"
                ),
                html.Small(
                    "This title appears at the top of your welcome screen",
                    className="text-muted d-block mt-1"
                )
            ], className="modal-input-group"),
            html.Div([
                html.Label("Welcome Description", className="modal-label"),
                dbc.Textarea(
                    id="welcome-description-input",
                    placeholder="Enter a description that helps users understand the purpose of your application",
                    className="modal-input",
                    style={"height": "80px"}
                ),
                html.Small(
                    "This description appears below the title and helps guide your users",
                    className="text-muted d-block mt-1"
                )
            ], className="modal-input-group"),
            html.Div([
                html.Label("Suggestion Questions", className="modal-label"),
                html.Small(
                    "Customize the four suggestion questions that appear on the welcome screen",
                    className="text-muted d-block mb-3"
                ),
                dbc.Input(
                    id="suggestion-1-input",
                    type="text",
                    placeholder="First suggestion question",
                    className="modal-input mb-2"
                ),
                dbc.Input(
                    id="suggestion-2-input",
                    type="text",
                    placeholder="Second suggestion question",
                    className="modal-input mb-2"
                ),
                dbc.Input(
                    id="suggestion-3-input",
                    type="text",
                    placeholder="Third suggestion question",
                    className="modal-input mb-2"
                ),
                dbc.Input(
                    id="suggestion-4-input",
                    type="text",
                    placeholder="Fourth suggestion question",
                    className="modal-input"
                )
            ], className="modal-input-group")
        ]),
        dbc.ModalFooter([
            dbc.Button(
                "Cancel",
                id="close-modal",
                className="modal-button",
                color="light"
            ),
            dbc.Button(
                "Save Changes",
                id="save-welcome-text",
                className="modal-button-primary",
                color="primary"
            )
        ])
    ], id="edit-welcome-modal", is_open=False, size="lg", backdrop="static") 