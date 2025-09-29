"""
LaunchDarkly Configuration Utilities

Environment-aware configuration management for the LaunchDarkly Python SDK.
"""

import os
import logging
from typing import Optional, Dict, Any
from ldclient.config import Config
from ldclient import basic_logger


def get_sdk_key() -> str:
    """
    Retrieves the LaunchDarkly SDK key from environment variables.
    
    Returns:
        str: The SDK key for the current environment
        
    Raises:
        ValueError: If no SDK key is found in environment variables
    """
    sdk_key = os.environ.get('LAUNCHDARKLY_SDK_KEY') or os.environ.get('LD_SDK_KEY')
    if not sdk_key:
        raise ValueError(
            'LaunchDarkly SDK key is required. Set LAUNCHDARKLY_SDK_KEY or LD_SDK_KEY environment variable.'
        )
    return sdk_key


def default_launchdarkly_http_configuration() -> Dict[str, Any]:
    """
    Creates default HTTP configuration with proxy support based on environment variables.
    
    Returns:
        Dict[str, Any]: HTTP configuration dictionary
    """
    http_config = {}
    
    # Parse proxy settings from environment variables
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    
    if https_proxy or http_proxy:
        # Python's urllib will automatically use these environment variables
        # No additional configuration needed for the LaunchDarkly SDK
        pass
    
    return http_config


def get_ld_config() -> Config:
    """
    Returns a pre-configured Config object with environment-specific defaults.
    
    Returns:
        Config: Configured LaunchDarkly Config object
    """
    # Get logging level from environment
    log_level = os.environ.get('LD_LOG_LEVEL', 'info').upper()
    
    # Map string levels to logging constants
    level_mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'NONE': logging.CRITICAL
    }
    
    log_level_value = level_mapping.get(log_level, logging.INFO)
    
    config = Config(
        sdk_key=get_sdk_key(),
        logger=basic_logger(level=log_level_value)
    )
    
    # Service endpoint configuration for relay proxy
    service_endpoints = os.environ.get('LD_RELAY_PROXY_BASE_URL') or os.environ.get('LAUNCHDARKLY_BASE_URL')
    if service_endpoints:
        config.service_endpoints = {
            'streaming': f'{service_endpoints}/all',
            'polling': f'{service_endpoints}/sdk/latest-all',
            'events': f'{service_endpoints}/bulk'
        }
    
    return config
