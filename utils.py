import sqlparse

def format_sql_query(sql_query):
    """Format SQL query using sqlparse library"""
    formatted_sql = sqlparse.format(
        sql_query,
        keyword_case='upper',  # Makes keywords uppercase
        identifier_case=None,  # Preserves identifier case
        reindent=True,         # Adds proper indentation
        indent_width=2,        # Indentation width
        strip_comments=False,  # Preserves comments
        comma_first=False      # Commas at the end of line, not beginning
    )
    return formatted_sql 