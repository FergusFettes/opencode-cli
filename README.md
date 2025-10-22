# opencode-client

Python client for [opencode](https://github.com/sst/opencode) server API.

## Installation

```bash
pip install opencode-client
```

## Usage

```python
from opencode_client import OpencodeClient

# Create client (defaults to http://localhost:36000)
client = OpencodeClient()

# Or specify custom URL
client = OpencodeClient(base_url="http://localhost:8000")

# List sessions
sessions = client.list_sessions()

# Send message to session (by ID or title)
response = client.send_message("headless-1", "hello world")

# Get session info
session = client.get_session("ses_abc123")

# Create new session
new_session = client.create_session(title="My Session")

# List messages
messages = client.list_messages("headless-1")
```

## Environment Variables

- `OPENCODE_SERVER` - Override default server URL (default: `http://localhost:36000`)

## License

MIT
