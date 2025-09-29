"""
LaunchDarkly Python SDK Implementation

A comprehensive LaunchDarkly SDK implementation for Python following best practices and workspace rules.
"""

from .config import get_sdk_key, get_ld_config, default_launchdarkly_http_configuration
from .client import (
    initialize_launchdarkly,
    set_ld_client,
    get_ld_client,
    setup_graceful_shutdown
)
from .evaluation import (
    evaluate_boolean_flag,
    evaluate_string_flag,
    evaluate_number_flag,
    evaluate_json_flag,
    evaluate_flag_with_detail,
    evaluate_flags,
    set_local_flag_override,
    remove_local_flag_override,
    clear_all_local_flag_overrides
)
from .context import (
    create_ld_context_for_user,
    create_anonymous_ld_context,
    create_organization_context,
    create_multi_context,
    validate_ld_context,
    sanitize_context_for_logging,
    UserInfo,
    OrganizationInfo
)

__all__ = [
    # Configuration utilities
    'get_sdk_key',
    'get_ld_config',
    'default_launchdarkly_http_configuration',
    
    # Client management utilities
    'initialize_launchdarkly',
    'set_ld_client',
    'get_ld_client',
    'setup_graceful_shutdown',
    
    # Flag evaluation utilities
    'evaluate_boolean_flag',
    'evaluate_string_flag',
    'evaluate_number_flag',
    'evaluate_json_flag',
    'evaluate_flag_with_detail',
    'evaluate_flags',
    'set_local_flag_override',
    'remove_local_flag_override',
    'clear_all_local_flag_overrides',
    
    # Context utilities
    'create_ld_context_for_user',
    'create_anonymous_ld_context',
    'create_organization_context',
    'create_multi_context',
    'validate_ld_context',
    'sanitize_context_for_logging',
    'UserInfo',
    'OrganizationInfo'
]
