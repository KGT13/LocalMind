!macro customInstall
  DetailPrint "Installing Ollama (AI Engine)..."
  ExecWait '"winget" install --id Ollama.Ollama -e --silent --accept-package-agreements --accept-source-agreements'
!macroend
