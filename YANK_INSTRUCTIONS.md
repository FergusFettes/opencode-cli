# Yanking Old PyPI Package

The old `opencode-sdk` package should be yanked from PyPI since it's redundant with the official `opencode-ai` SDK.

Note: `opencode-client` is not ours (different author).

## Yank via PyPI Web UI

Yanking must be done through the PyPI website (no CLI command available).

1. Go to: https://pypi.org/manage/project/opencode-sdk/releases/
2. For each version (0.1.0, 0.2.0):
   - Click "Options" button
   - Click "Yank"
   - Add reason: "Deprecated: use official opencode-ai package instead"
   - Confirm

## What yanking does

- Hides packages from `pip install` (won't show up in searches)
- Existing pinned versions still work (doesn't break anyone)
- Package can't be deleted from PyPI (permanent record)

## New package

The CLI tool has been refactored as `opencode-cli` which wraps the official SDK.

Publish when ready:
```bash
cd ~/opencode-cli
uv build
twine upload dist/*
```
