"""
Logging configuration for mmo_board project.
"""
import logging
from pathlib import Path
from django.conf import settings

# Create logs directory if it doesn't exist
logs_dir = Path(settings.BASE_DIR) / 'logs'
logs_dir.mkdir(exist_ok=True)

# This module is for custom logging utilities if needed
logger = logging.getLogger(__name__)

