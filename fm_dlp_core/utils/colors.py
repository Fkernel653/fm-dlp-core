"""
Terminal color utilities for styled console output.

This module provides ANSI color codes and helper functions for colorizing
terminal output. Colors can be globally enabled or disabled via the
`set_colors()` function, allowing consistent behavior across the application
whether running in a color-capable terminal or not.

Constants:
    RESET: Reset all text formatting to default.
    BOLD_WHITE, GRAY, WHITE: White/gray color variations.
    BOLD_RED, BOLD_GREEN, BOLD_YELLOW, BOLD_CYAN: Bold primary colors.

Functions:
    set_colors: Enable or disable color output globally.
    is_colors_enabled: Check if color output is currently enabled.
    styled: Apply ANSI color codes to text conditionally.
    success: Format text as a success message (bold green).
    error: Format text as an error message (bold red).
    info: Format text as an info message (bold cyan).
    hint: Format text as a subtle hint message (gray).

Example:
    >>> from fm_dlp_core.utils.colors import success, error, set_colors
    >>> set_colors(True)
    >>> print(success("Download complete!"))
    >>> print(error("Failed to download"))
"""

RESET = "\033[0m"

BOLD_WHITE = "\033[37m"

GRAY = "\033[90m"

WHITE = "\033[0;37m"

BOLD_RED = "\033[1;31m"
BOLD_GREEN = "\033[1;32m"
BOLD_YELLOW = "\033[1;33m"
BOLD_CYAN = "\033[1;36m"

colors_enabled = True


def set_colors(enabled: bool):
    global colors_enabled
    colors_enabled = enabled


def is_colors_enabled() -> bool:
    return colors_enabled


def styled(text: str, color: str) -> str:
    """
    Apply ANSI color codes to text if color output is enabled.

    Wraps the input text with the specified ANSI color code and reset sequence.
    If color output is disabled (e.g., non-interactive terminal or --no-color flag),
    returns the original text unchanged. This allows the same code to work in
    both color-enabled and color-disabled environments without conditional logic.

    Args:
        text (str): The text string to colorize.
        color (str): ANSI color code string (e.g., BOLD_RED, BOLD_GREEN, BOLD_YELLOW).
                     Must be defined in the module (e.g., from colors import BOLD_RED).

    Returns:
        str: The colorized text with ANSI escape sequences if colors are enabled,
             otherwise the original text unchanged.
    """
    if is_colors_enabled():
        return color + text + RESET
    else:
        return text


def success(text: str, prefix: str = "Success: ") -> str:
    """
    Format text as a success message with bold green coloring.

    Adds a 'Success: ' prefix and applies bold green ANSI color to the entire
    message (both prefix and text) when color output is enabled. The prefix
    is colored as well for visual consistency, while the text remains uncolored
    but the RESET code ensures proper termination.

    Args:
        text (str): The message content to display.
        prefix (str, optional): Custom prefix text. Defaults to "Success: ".

    Returns:
        str: Formatted success message with optional coloring.
    """
    if is_colors_enabled():
        return BOLD_GREEN + prefix + RESET + text
    else:
        return prefix + text


def error(text: str, prefix: str = "Error: ") -> str:
    """
    Format text as an error message with bold red coloring.

    Adds an 'Error: ' prefix and applies bold red ANSI color to the entire
    message when color output is enabled. This provides visual distinction
    for error messages in terminal output, making them easily identifiable.

    Args:
        text (str): The error message content.
        prefix (str, optional): Custom prefix text. Defaults to "Error: ".

    Returns:
        str: Formatted error message with optional coloring.
    """
    if is_colors_enabled():
        return BOLD_RED + prefix + RESET + text
    else:
        return prefix + text


def info(text: str, prefix: str = "Info: ") -> str:
    """
    Format text as an informational message with bold cyan coloring.

    Adds an 'Info: ' prefix and applies bold cyan ANSI color to the entire
    message when color output is enabled. Used for non-critical information
    and status updates that should be visually distinct but not alarming.

    Args:
        text (str): The informational message content.
        prefix (str, optional): Custom prefix text. Defaults to "Info: ".

    Returns:
        str: Formatted info message with optional coloring.
    """
    if is_colors_enabled():
        return BOLD_CYAN + prefix + RESET + text
    else:
        return prefix + text


def hint(text: str, prefix: str = "Hint: ") -> str:
    """
    Format text as a subtle hint message with gray coloring.

    Adds a 'Hint: ' prefix and applies gray ANSI color to the entire message
    when color output is enabled. Used for supplementary tips, suggestions,
    or auxiliary information that shouldn't distract from the main output.

    Args:
        text (str): The hint message content.
        prefix (str, optional): Custom prefix text. Defaults to "Hint: ".

    Returns:
        str: Formatted hint message with optional coloring.
    """
    if is_colors_enabled():
        return GRAY + prefix + RESET + text
    else:
        return prefix + text
