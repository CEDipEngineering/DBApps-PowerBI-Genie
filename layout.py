from dash import html, dcc
import dash_bootstrap_components as dbc
import os
from config import DEFAULT_WELCOME_TITLE, DEFAULT_WELCOME_DESCRIPTION, DEFAULT_SUGGESTIONS
from components import create_welcome_modal

def create_layout():
    """Create the main application layout"""
    return html.Div([
        # Top navigation bar
        html.Div([
            # Left component containing both nav-left and sidebar
            html.Div([
                # Nav left
                html.Div([
                    html.Button([
                        html.Img(src="assets/menu_icon.svg", className="menu-icon")
                    ], id="sidebar-toggle", className="nav-button"),
                    html.Button([
                        html.Img(src="assets/plus_icon.svg", className="new-chat-icon")
                    ], id="new-chat-button", className="nav-button",disabled=False),
                    html.Button([
                        html.Img(src="assets/plus_icon.svg", className="new-chat-icon"),
                        html.Div("New chat", className="new-chat-text")
                    ], id="sidebar-new-chat-button", className="new-chat-button",disabled=False)
                ], id="nav-left", className="nav-left"),
                
                # Sidebar
                html.Div([
                    html.Div([
                        html.Div("Your conversations with Genie", className="sidebar-header-text"),
                    ], className="sidebar-header"),
                    html.Div([], className="chat-list", id="chat-list")
                ], id="sidebar", className="sidebar")
            ], id="left-component", className="left-component"),
            
            html.Div([
                html.Div("Genie Space", id="logo-container", className="logo-container")
            ], className="nav-center"),
            html.Div([
                html.Div("Y", className="user-avatar"),
                html.A(
                    html.Button(
                        "Logout",
                        id="logout-button",
                        className="logout-button"
                    ),
                    href=f"https://{os.getenv('DATABRICKS_HOST')}/login.html",
                    className="logout-link"
                )
            ], className="nav-right")
        ], className="top-nav"),
        
        # Main content area
        html.Div([
            html.Div([
                # Chat content
                html.Div([
                    # Welcome container
                    html.Div([
                        html.Div([html.Div([
                        html.Div(className="genie-logo")
                    ], className="genie-logo-container")],
                    className="genie-logo-container-header"),
                   
                        # Add settings button with tooltip
                        html.Div([
                            html.Div(id="welcome-title", className="welcome-message", children=DEFAULT_WELCOME_TITLE),
                            html.Button([
                                html.Img(src="assets/settings_icon.svg", className="settings-icon"),
                                html.Div("Customize welcome message", className="button-tooltip")
                            ],
                            id="edit-welcome-button",
                            className="edit-welcome-button",
                            title="Customize welcome message")
                        ], className="welcome-title-container"),
                        
                        html.Div(id="welcome-description", 
                                className="welcome-message-description",
                                children=DEFAULT_WELCOME_DESCRIPTION),
                        
                        # Add modal for editing welcome text
                        create_welcome_modal(),
                        
                        # Suggestion buttons with IDs
                        html.Div([
                            html.Button([
                                html.Div(className="suggestion-icon"),
                                html.Div("What tables are there and how are they connected? Give me a short summary.", 
                                       className="suggestion-text", id="suggestion-1-text")
                            ], id="suggestion-1", className="suggestion-button"),
                            html.Button([
                                html.Div(className="suggestion-icon"),
                                html.Div("Which distribution center has the highest chance of being a bottleneck?",
                                       className="suggestion-text", id="suggestion-2-text")
                            ], id="suggestion-2", className="suggestion-button"),
                            html.Button([
                                html.Div(className="suggestion-icon"),
                                html.Div("Explain the dataset",
                                       className="suggestion-text", id="suggestion-3-text")
                            ], id="suggestion-3", className="suggestion-button"),
                            html.Button([
                                html.Div(className="suggestion-icon"),
                                html.Div("What was the demand for our products by week in 2024?",
                                       className="suggestion-text", id="suggestion-4-text")
                            ], id="suggestion-4", className="suggestion-button")
                        ], className="suggestion-buttons")
                    ], id="welcome-container", className="welcome-container visible"),
                    
                    # Chat messages
                    html.Div([], id="chat-messages", className="chat-messages"),
                ], id="chat-content", className="chat-content"),
                
                # Input area
                html.Div([
                    html.Div([
                        dcc.Input(
                            id="chat-input-fixed",
                            placeholder="Ask your question...",
                            className="chat-input",
                            type="text",
                            disabled=False
                        ),
                        html.Div([
                            html.Button(
                                id="send-button-fixed", 
                                className="input-button send-button",
                                disabled=False
                            )
                        ], className="input-buttons-right"),
                        html.Div("You can only submit one query at a time", 
                                id="query-tooltip", 
                                className="query-tooltip hidden")
                    ], id="fixed-input-container", className="fixed-input-container"),
                    html.Div("Always review the accuracy of responses.", className="disclaimer-fixed")
                ], id="fixed-input-wrapper", className="fixed-input-wrapper"),
            ], id="chat-container", className="chat-container"),
        ], id="main-content", className="main-content"),
        
        html.Div(id='dummy-output'),
        dcc.Store(id="chat-trigger", data={"trigger": False, "message": ""}),
        dcc.Store(id="chat-history-store", data=[]),
        dcc.Store(id="query-running-store", data=False),
        dcc.Store(id="session-store", data={"current_session": None})
    ]) 