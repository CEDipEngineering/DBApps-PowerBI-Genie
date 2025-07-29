# Genie PBI App - Modular Architecture

This application has been refactored into a modular structure for better organization and maintainability.

## File Structure

```
genie-pbi-app/
├── app.py              # Main application entry point
├── config.py           # Configuration constants and settings
├── layout.py           # UI layout components
├── components.py       # Reusable UI component functions
├── callbacks.py        # All Dash callback functions
├── utils.py            # Utility functions
├── genie_room.py       # Genie integration (existing)
├── token_minter.py     # Token management (existing)
└── assets/             # Static assets (CSS, images, etc.)
```

## Module Descriptions

### `app.py`
- Main entry point for the Dash application
- Creates the Dash app instance
- Sets up the layout and registers callbacks
- Minimal and focused on application initialization

### `config.py`
- Contains all configuration constants
- Default welcome messages and suggestions
- Environment variables and settings
- Centralized configuration management

### `layout.py`
- Defines the complete UI layout structure
- Separates layout logic from application logic
- Uses components from `components.py` for reusable elements
- Clean separation of concerns

### `components.py`
- Reusable UI component functions
- Data table creation
- Message components (user, bot, error)
- Modal and form components
- Promotes code reuse and consistency

### `callbacks.py`
- All Dash callback functions
- Organized by functionality (chat, sidebar, feedback, etc.)
- Uses components from `components.py`
- Clean separation of interaction logic

### `utils.py`
- Utility functions for data processing
- SQL formatting utilities
- Helper functions used across modules
- Pure functions with no side effects

## Benefits of This Architecture

1. **Separation of Concerns**: Each file has a specific responsibility
2. **Maintainability**: Easier to find and modify specific functionality
3. **Reusability**: Components can be reused across different parts of the app
4. **Testability**: Individual modules can be tested in isolation
5. **Scalability**: Easy to add new features without affecting existing code
6. **Readability**: Clear organization makes the codebase easier to understand

## Key Improvements

- **Modular Design**: Each aspect of the application is in its own module
- **Component Reuse**: Common UI elements are extracted into reusable functions
- **Configuration Management**: All constants and settings are centralized
- **Clean Callbacks**: All callback logic is organized in one place
- **Utility Functions**: Common operations are extracted into utility functions

## Usage

The application works exactly the same as before, but the code is now much more organized and maintainable. To run the application:

```bash
python app.py
```

All functionality remains intact:
- Chat interface with Genie
- Data table display
- SQL query formatting
- Thumbs up/down feedback
- Chat history management
- Welcome message customization
- Sidebar navigation 