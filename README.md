# opencode-cli

CLI tool for [opencode](https://github.com/sst/opencode) server API. Built on top of the official [opencode-ai](https://pypi.org/project/opencode-ai/) Python SDK.

## Installation

```bash
pip install opencode-cli
```

## Usage

The `oc` command provides easy access to opencode server operations:

```bash
# List all sessions
oc sessions

# List sessions as JSON
oc sessions --json

# Get session info (by ID or title)
oc info headless-1
oc info ses_abc123

# List messages in a session
oc messages headless-1

# Send a message to a session
oc send headless-1 "hello world"

# Create a new session
oc create --title "My Session"
```

## Features

- **Title resolution**: Use session titles instead of IDs (e.g., `headless-1` instead of `ses_abc123`)
- **Rich formatting**: Beautiful tables and colored output
- **JSON output**: Use `--json` flag for machine-readable output
- **Built on official SDK**: Uses the official `opencode-ai` package under the hood

## Environment Variables

- `OPENCODE_SERVER` - Override default server URL (default: `http://localhost:36000`)

## For Python SDK

If you need the full Python SDK (not just CLI), use the official package:

```bash
pip install opencode-ai
```

See [official SDK docs](https://github.com/sst/opencode-sdk-python) for Python API usage.

## License

MIT
