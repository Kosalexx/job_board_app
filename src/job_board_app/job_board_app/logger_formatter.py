"""
Custom logging formatter.
"""

import logging


class ContextFormatter(logging.Formatter):
    """Custom context logging formatter."""

    def format(self, record: logging.LogRecord) -> str:  # noqa
        """Formatted logging data."""
        formatted_message: str = super().format(record=record)
        default_log_record = logging.LogRecord('', 0, "", 0, None, None, None, None, None)
        context_message = 'Context: '
        for key, value in record.__dict__.items():
            if key not in default_log_record.__dict__ and key not in ('message', 'asctime'):
                context_message += f'({key}={value})| '
        if context_message != 'Context: ':
            formatted_message = formatted_message + ' ' + context_message
        return formatted_message
