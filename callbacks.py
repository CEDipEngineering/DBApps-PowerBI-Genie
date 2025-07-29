from dash import Input, Output, State, callback, ALL, MATCH, callback_context, no_update, clientside_callback, html, dcc
import dash
import json
import pandas as pd
from genie_room import genie_query
from components import (
    create_user_message, 
    create_thinking_indicator, 
    create_data_table, 
    create_query_section, 
    create_bot_response, 
    create_error_response
)
from config import DEFAULT_WELCOME_TITLE, DEFAULT_WELCOME_DESCRIPTION, DEFAULT_SUGGESTIONS

def register_callbacks(app):
    """Register all callbacks with the Dash app"""
    
    # First callback: Handle inputs and show thinking indicator
    @app.callback(
        [Output("chat-messages", "children", allow_duplicate=True),
         Output("chat-input-fixed", "value", allow_duplicate=True),
         Output("welcome-container", "className", allow_duplicate=True),
         Output("chat-trigger", "data", allow_duplicate=True),
         Output("query-running-store", "data", allow_duplicate=True)],
        [Input("suggestion-1", "n_clicks"),
         Input("suggestion-2", "n_clicks"),
         Input("suggestion-3", "n_clicks"),
         Input("suggestion-4", "n_clicks"),
         Input("send-button-fixed", "n_clicks"),
         Input("chat-input-fixed", "n_submit")],
        [State("suggestion-1-text", "children"),
         State("suggestion-2-text", "children"),
         State("suggestion-3-text", "children"),
         State("suggestion-4-text", "children"),
         State("chat-input-fixed", "value"),
         State("chat-messages", "children"),
         State("welcome-container", "className")],
        prevent_initial_call=True
    )
    def handle_all_inputs(s1_clicks, s2_clicks, s3_clicks, s4_clicks, send_clicks, submit_clicks,
                         s1_text, s2_text, s3_text, s4_text, input_value, current_messages,
                         welcome_class):
        ctx = callback_context
        if not ctx.triggered:
            return [no_update] * 8

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        # Handle suggestion buttons
        suggestion_map = {
            "suggestion-1": s1_text,
            "suggestion-2": s2_text,
            "suggestion-3": s3_text,
            "suggestion-4": s4_text
        }
        
        # Get the user input based on what triggered the callback
        if trigger_id in suggestion_map:
            user_input = suggestion_map[trigger_id]
        else:
            user_input = input_value
        
        if not user_input:
            return [no_update] * 5
        
        # Create user message
        user_message = create_user_message(user_input)
        
        # Add the user message to the chat
        updated_messages = current_messages + [user_message] if current_messages else [user_message]
        
        # Add thinking indicator
        thinking_indicator = create_thinking_indicator()
        updated_messages.append(thinking_indicator)
        
        return (updated_messages, "", "welcome-container hidden",
                {"trigger": True, "message": user_input}, True)

    # Second callback: Make API call and show response
    @app.callback(
        [Output("chat-messages", "children", allow_duplicate=True),
         Output("chat-trigger", "data", allow_duplicate=True),
         Output("query-running-store", "data", allow_duplicate=True)],
        [Input("chat-trigger", "data")],
        [State("chat-messages", "children")],
        prevent_initial_call=True
    )
    def get_model_response(trigger_data, current_messages):
        if not trigger_data or not trigger_data.get("trigger"):
            return dash.no_update, dash.no_update, dash.no_update
        
        user_input = trigger_data.get("message", "")
        if not user_input:
            return dash.no_update, dash.no_update, dash.no_update
        
        try:
            response, query_text = genie_query(user_input)
            
            if isinstance(response, str):
                content = dcc.Markdown(response, className="message-text")
            else:
                # Data table response
                df = pd.DataFrame(response)
                
                # Create the table
                table_id = f"table-{len(chat_history)}"
                data_table = create_data_table(df, table_id)

                # Format SQL query if available
                query_section = None
                if query_text is not None:
                    query_index = f"{len(chat_history)}-{len(current_messages)}"
                    query_section = create_query_section(query_text, query_index)

                # Create content with table and optional SQL section
                content = html.Div([
                    html.Div([data_table], style={
                        'marginBottom': '20px',
                        'paddingRight': '5px'
                    }),
                    query_section if query_section else None,
                ])
            
            # Create bot response
            bot_response = create_bot_response(content, 0)
            
            return current_messages[:-1] + [bot_response], {"trigger": False, "message": ""}, False
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}. Please try again later."
            error_response = create_error_response(error_msg)
            
            return current_messages[:-1] + [error_response], {"trigger": False, "message": ""}, False





    # Modify the new chat button callback to reset session
    @app.callback(
        [Output("welcome-container", "className", allow_duplicate=True),
         Output("chat-messages", "children", allow_duplicate=True),
         Output("chat-trigger", "data", allow_duplicate=True),
         Output("query-running-store", "data", allow_duplicate=True)],
        [Input("new-chat-button", "n_clicks")],
        [State("chat-messages", "children"),
         State("chat-trigger", "data"),
         State("query-running-store", "data")],
        prevent_initial_call=True
    )
    def reset_to_welcome(n_clicks, chat_messages, chat_trigger, query_running):
        # Reset session when starting a new chat
        return ("welcome-container visible", [], {"trigger": False, "message": ""}, False)

    @app.callback(
        [Output("welcome-container", "className", allow_duplicate=True)],
        [Input("chat-messages", "children")],
        prevent_initial_call=True
    )
    def reset_query_running(chat_messages):
        # Return as a single-item list
        if chat_messages:
            return ["welcome-container hidden"]
        else:
            return ["welcome-container visible"]

    # Add callback to disable input while query is running
    @app.callback(
        [Output("chat-input-fixed", "disabled"),
         Output("send-button-fixed", "disabled"),
         Output("new-chat-button", "disabled"),
         Output("query-tooltip", "className")],
        [Input("query-running-store", "data")],
        prevent_initial_call=True
    )
    def toggle_input_disabled(query_running):
        # Show tooltip when query is running, hide it otherwise
        tooltip_class = "query-tooltip visible" if query_running else "query-tooltip hidden"
        
        # Disable input and buttons when query is running
        return query_running, query_running, query_running, tooltip_class

    # Fix the callback for thumbs up/down buttons
    @app.callback(
        [Output({"type": "thumbs-up-button", "index": MATCH}, "className"),
         Output({"type": "thumbs-down-button", "index": MATCH}, "className")],
        [Input({"type": "thumbs-up-button", "index": MATCH}, "n_clicks"),
         Input({"type": "thumbs-down-button", "index": MATCH}, "n_clicks")],
        [State({"type": "thumbs-up-button", "index": MATCH}, "className"),
         State({"type": "thumbs-down-button", "index": MATCH}, "className")],
        prevent_initial_call=True
    )
    def handle_feedback(up_clicks, down_clicks, up_class, down_class):
        ctx = callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update
        
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        button_type = json.loads(trigger_id)["type"]
        
        if button_type == "thumbs-up-button":
            new_up_class = "thumbs-up-button active" if "active" not in up_class else "thumbs-up-button"
            new_down_class = "thumbs-down-button"
        else:
            new_up_class = "thumbs-up-button"
            new_down_class = "thumbs-down-button active" if "active" not in down_class else "thumbs-down-button"
        
        return new_up_class, new_down_class

    # Add callback for toggling SQL query visibility
    @app.callback(
        [Output({"type": "query-code", "index": MATCH}, "className"),
         Output({"type": "toggle-text", "index": MATCH}, "children")],
        [Input({"type": "toggle-query", "index": MATCH}, "n_clicks")],
        prevent_initial_call=True
    )
    def toggle_query_visibility(n_clicks):
        if n_clicks % 2 == 1:
            return "query-code-container visible", "Hide code"
        return "query-code-container hidden", "Show code"

    # Add callbacks for welcome text customization
    @app.callback(
        [Output("edit-welcome-modal", "is_open", allow_duplicate=True),
         Output("welcome-title-input", "value"),
         Output("welcome-description-input", "value"),
         Output("suggestion-1-input", "value"),
         Output("suggestion-2-input", "value"),
         Output("suggestion-3-input", "value"),
         Output("suggestion-4-input", "value")],
        [Input("edit-welcome-button", "n_clicks")],
        [State("welcome-title", "children"),
         State("welcome-description", "children"),
         State("suggestion-1-text", "children"),
         State("suggestion-2-text", "children"),
         State("suggestion-3-text", "children"),
         State("suggestion-4-text", "children")],
        prevent_initial_call=True
    )
    def open_modal(n_clicks, current_title, current_description, s1, s2, s3, s4):
        if not n_clicks:
            return [no_update] * 7
        return True, current_title, current_description, s1, s2, s3, s4

    @app.callback(
        [Output("welcome-title", "children", allow_duplicate=True),
         Output("welcome-description", "children", allow_duplicate=True),
         Output("suggestion-1-text", "children", allow_duplicate=True),
         Output("suggestion-2-text", "children", allow_duplicate=True),
         Output("suggestion-3-text", "children", allow_duplicate=True),
         Output("suggestion-4-text", "children", allow_duplicate=True),
         Output("edit-welcome-modal", "is_open", allow_duplicate=True)],
        [Input("save-welcome-text", "n_clicks"),
         Input("close-modal", "n_clicks")],
        [State("welcome-title-input", "value"),
         State("welcome-description-input", "value"),
         State("suggestion-1-input", "value"),
         State("suggestion-2-input", "value"),
         State("suggestion-3-input", "value"),
         State("suggestion-4-input", "value"),
         State("welcome-title", "children"),
         State("welcome-description", "children"),
         State("suggestion-1-text", "children"),
         State("suggestion-2-text", "children"),
         State("suggestion-3-text", "children"),
         State("suggestion-4-text", "children")],
        prevent_initial_call=True
    )
    def handle_modal_actions(save_clicks, close_clicks,
                            new_title, new_description, s1, s2, s3, s4,
                            current_title, current_description,
                            current_s1, current_s2, current_s3, current_s4):
        ctx = callback_context
        if not ctx.triggered:
            return [no_update] * 7

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "close-modal":
            return [current_title, current_description, 
                    current_s1, current_s2, current_s3, current_s4, False]
        elif trigger_id == "save-welcome-text":
            # Save the changes
            title = new_title if new_title else DEFAULT_WELCOME_TITLE
            description = new_description if new_description else DEFAULT_WELCOME_DESCRIPTION
            suggestions = [
                s1 if s1 else DEFAULT_SUGGESTIONS[0],
                s2 if s2 else DEFAULT_SUGGESTIONS[1],
                s3 if s3 else DEFAULT_SUGGESTIONS[2],
                s4 if s4 else DEFAULT_SUGGESTIONS[3]
            ]
            return [title, description, *suggestions, False]

        return [no_update] * 7

    # Modify the clientside callback to target the chat-container
    app.clientside_callback(
        """
        function(children) {
            var chatMessages = document.getElementById('chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            return '';
        }
        """,
        Output('dummy-output', 'children'),
        Input('chat-messages', 'children'),
        prevent_initial_call=True
    ) 