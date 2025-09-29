"""
LaunchDarkly Client Management

Singleton pattern implementation for the LaunchDarkly Python SDK.
"""

import asyncio
import signal
import sys
import time
from typing import Optional
from ldclient import LDClient, set_config, get as get_client
from .config import get_sdk_key, get_ld_config


_client_instance: Optional[LDClient] = None
_initialization_promise: Optional[asyncio.Task] = None


async def initialize_launchdarkly(config=None, timeout: int = 5) -> LDClient:
    """
    Initializes LaunchDarkly client with timeout and error handling.
    
    Args:
        config: LaunchDarkly Config object (defaults to get_ld_config())
        timeout: Initialization timeout in seconds (default: 5)
        
    Returns:
        LDClient: Initialized LaunchDarkly client
        
    Raises:
        TimeoutError: If initialization times out
        Exception: If initialization fails
    """
    global _client_instance, _initialization_promise
    
    # Return existing client if already initialized
    if _client_instance:
        return _client_instance
    
    # Return existing initialization promise if already in progress
    if _initialization_promise:
        return await _initialization_promise
    
    if config is None:
        config = get_ld_config()
    
    async def _initialize():
        nonlocal _client_instance
        
        # Set the configuration
        set_config(config)
        
        # Get the client (this will initialize it)
        client = get_client()
        
        # Wait for initialization with timeout
        start_time = time.time()
        while not client.is_initialized():
            if time.time() - start_time > timeout:
                raise TimeoutError(f'LaunchDarkly client initialization timed out after {timeout} seconds')
            await asyncio.sleep(0.1)
        
        initialization_time = time.time() - start_time
        print(f'LaunchDarkly client initialized successfully in {initialization_time:.2f}s')
        
        _client_instance = client
        return client
    
    _initialization_promise = asyncio.create_task(_initialize())
    return await _initialization_promise


def set_ld_client(ld_client: LDClient) -> None:
    """
    Sets the singleton instance that will be returned by get_ld_client().
    
    Args:
        ld_client: The LaunchDarkly client instance to set
    """
    global _client_instance
    _client_instance = ld_client


def get_ld_client() -> LDClient:
    """
    Gets the instance of the singleton client.
    
    Returns:
        LDClient: The LaunchDarkly client instance
        
    Raises:
        RuntimeError: If client has not been initialized
    """
    if _client_instance is None:
        raise RuntimeError('LaunchDarkly client not initialized. Call set_ld_client() first.')
        # Alternative implementation that initializes with default config:
        # return get_client()
    
    return _client_instance


def setup_graceful_shutdown() -> None:
    """
    Sets up graceful shutdown handlers for the LaunchDarkly client.
    """
    def shutdown_handler(signum, frame):
        print(f'Received signal {signum}, shutting down gracefully...')
        
        if _client_instance:
            try:
                # Flush pending events
                _client_instance.flush()
                print('LaunchDarkly events flushed successfully')
                
                # Close the client
                _client_instance.close()
                print('LaunchDarkly client closed successfully')
            except Exception as error:
                print(f'Error during LaunchDarkly shutdown: {error}')
        
        sys.exit(0)
    
    # Handle various shutdown signals
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGQUIT, shutdown_handler)
    
    # Handle uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        print(f'Uncaught Exception: {exc_type.__name__}: {exc_value}')
        shutdown_handler(signal.SIGTERM, None)
    
    sys.excepthook = handle_exception
