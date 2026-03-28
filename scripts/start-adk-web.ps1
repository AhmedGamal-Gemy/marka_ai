# scripts/start-adk-web.ps1
Set-Location -Path "ai"
# Add current directory to PYTHONPATH so "app" module is discoverable
$env:PYTHONPATH = "."
# Point ADK to the app/agents folder for discovery
uv run adk web app/agents --reload
