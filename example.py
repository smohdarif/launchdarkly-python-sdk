#!/usr/bin/env python3
"""
Example usage of the LaunchDarkly Python SDK implementation.
"""

import asyncio
from src.launchdarkly import (
    initialize_launchdarkly,
    setup_graceful_shutdown,
    evaluate_boolean_flag,
    create_ld_context_for_user,
    UserInfo
)

async def main():
    """Main application function."""
    try:
        # Setup graceful shutdown handlers
        setup_graceful_shutdown()
        print('Graceful shutdown handlers registered')
        
        # Initialize LaunchDarkly client
        print('Initializing LaunchDarkly client...')
        client = await initialize_launchdarkly()
        print('LaunchDarkly client initialized successfully')
        
        # Create a user context
        user_info = UserInfo(
            user_id='user-123',
            name='John Doe',
            email='john.doe@example.com',
            session_id='session-456'
        )
        
        user_context = create_ld_context_for_user(user_info, {
            'betaTester': True,
            'accountType': 'premium'
        })
        
        print('User context created:', user_context.key)
        
        # Example flag evaluations
        print('\n--- Flag Evaluations ---')
        
        # Boolean flag
        feature_enabled = evaluate_boolean_flag('new-feature', user_context, False)
        print('Feature enabled:', feature_enabled)
        
        print('\nApplication running successfully. Press Ctrl+C to exit gracefully.')
        
        # Keep the application running
        while True:
            await asyncio.sleep(30)
            print('Application is running...')
            
    except Exception as error:
        print(f'Error during application startup: {error}')
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
