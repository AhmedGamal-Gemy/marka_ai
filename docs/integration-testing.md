# Integration Testing Guide

This project uses integration tests to verify the connection between the Marka AI framework and external providers (Google Gemini API via ADK/LiteLLM).

## Running ADK Integration Tests

These tests require a valid `LLM_API_KEY` in your `.env` file and an active internet connection.

### 1. Manual Live Test
We have a dedicated script to verify the end-to-end flow from `LLMService` to the Google Gemini API.

```bash
cd ai
uv run python tests/test_adk_integration.py
```

### 2. What this verifies:
- `LLMService` correctly initializes and sets environment variables.
- `AgentRole` Enum maps to the correct model string.
- The Google ADK `Runner` can successfully authenticate and stream a response from the model.

---
**Note:** These tests incur API token usage. Do not run them in a tight loop during automated CI/CD unless using a mock provider.
