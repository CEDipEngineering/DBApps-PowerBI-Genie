from dash import html, dcc
import dash_bootstrap_components as dbc
import os
from config import DEFAULT_WELCOME_TITLE, DEFAULT_WELCOME_DESCRIPTION, DEFAULT_SUGGESTIONS, POWERBI_EMBED_URL
from components import create_welcome_modal

def create_layout():
    """Create the main application layout with Power BI embed and sidebar chat"""
    return html.Div([
        # Top navigation bar
        html.Div([
            # Left component containing sidebar toggle and logo
            html.Div([
                html.Button([
                    html.Img(src="assets/menu_icon.svg", className="menu-icon")
                ], id="sidebar-toggle", className="nav-button"),
                html.Div("Power BI Assistant", id="logo-container", className="logo-container")
            ], className="nav-left"),
            
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
        
        # Main content area with Power BI embed and sidebar
        html.Div([
            # Power BI Dashboard Area (Main Stage)
            html.Div([
                html.Div([
                    html.H3("Power BI Dashboard", className="dashboard-title"),
                    html.Iframe(
                        src=POWERBI_EMBED_URL,
                        width="100%",
                        height="800",
                        frameBorder="0",
                        allowFullScreen="true",
                        className="powerbi-iframe"
                    )
                ], className="dashboard-container")
            ], id="dashboard-area", className="dashboard-area"),
            
            # Sidebar Chat Area
            html.Div([
                html.Div([
                    html.Div([
                        html.Div("Genie Assistant", className="sidebar-header-text"),
                        html.Button([
                            html.Img(src="assets/plus_icon.svg", className="new-chat-icon")
                        ], id="new-chat-button", className="new-chat-button", disabled=False)
                    ], className="sidebar-header"),
                    
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
                                    html.Div("What are the key insights from this dashboard?", 
                                           className="suggestion-text", id="suggestion-1-text")
                                ], id="suggestion-1", className="suggestion-button"),
                                html.Button([
                                    html.Div(className="suggestion-icon"),
                                    html.Div("Can you explain the trends shown in the charts?",
                                           className="suggestion-text", id="suggestion-2-text")
                                ], id="suggestion-2", className="suggestion-button"),
                                html.Button([
                                    html.Div(className="suggestion-icon"),
                                    html.Div("What are the main metrics being displayed?",
                                           className="suggestion-text", id="suggestion-3-text")
                                ], id="suggestion-3", className="suggestion-button"),
                                html.Button([
                                    html.Div(className="suggestion-icon"),
                                    html.Div("How can I interpret the data visualizations?",
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
                                placeholder="Ask about your dashboard...",
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
                ], className="sidebar-content")
            ], id="sidebar", className="sidebar"),
        ], id="main-content", className="main-content"),
        
        html.Div(id='dummy-output'),
        dcc.Store(id="chat-trigger", data={"trigger": False, "message": ""}),
        dcc.Store(id="query-running-store", data=False)
    ]) 