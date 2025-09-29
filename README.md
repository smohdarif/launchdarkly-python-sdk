# LaunchDarkly Python SDK Implementation

A comprehensive LaunchDarkly SDK implementation for Python following best practices and workspace rules.

## Features

✅ **Singleton Client Pattern** - Proper initialization with timeout and error handling  
✅ **Environment-Aware Configuration** - Supports multiple configuration sources  
✅ **Graceful Shutdown** - Proper cleanup on process termination  
✅ **Centralized Flag Evaluation** - Consistent flag evaluation with instrumentation  
✅ **Context Management** - Rich context objects with custom attributes  
✅ **Local Overrides** - Development/testing support with flag overrides  
✅ **Python Type Hints** - Full type safety with LaunchDarkly types  

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Copy the example environment file and configure your LaunchDarkly SDK key:

```bash
cp env.example .env
```

Required environment variables:
- `LAUNCHDARKLY_SDK_KEY` - Your LaunchDarkly SDK key

Optional environment variables:
- `LD_LOG_LEVEL` - Logging level (debug, info, warn, error, none)
- `BUILD_VERSION` - Build version for deployment tracking
- `COMMIT_SHA` - Git commit SHA for deployment tracking
- `DEVELOPER_ID` - Developer identifier for ephemeral environments

## Usage

### Basic Setup

```python
import asyncio
from src.launchdarkly import (
    initialize_launchdarkly,
    setup_graceful_shutdown,
    evaluate_boolean_flag,
    create_ld_context_for_user,
    UserInfo
)

async def main():
    # Setup graceful shutdown
    setup_graceful_shutdown()
    
    # Initialize LaunchDarkly client
    client = await initialize_launchdarkly()
    
    # Create user context
    user_info = UserInfo(
        user_id='user-123',
        name='John Doe',
        session_id='session-456'
    )
    
    context = create_ld_context_for_user(user_info)
    
    # Evaluate a flag
    feature_enabled = evaluate_boolean_flag(
        'new-feature',
        context,
        False  # fallback value
    )
    
    if feature_enabled:
        print('New feature is enabled!')

if __name__ == '__main__':
    asyncio.run(main())
```

## Rules

This implementation follows the LaunchDarkly Python SDK rules defined in `.cursor/rules/launchdarkly-python.mdc`.

## License

MIT
