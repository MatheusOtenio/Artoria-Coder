@echo off
echo Verificando e iniciando o ambiente...

REM Verificar se o Ollama está instalado e em execução
powershell -Command "& {try { $null = Invoke-RestMethod -Uri 'http://localhost:11434/api/version' -TimeoutSec 2; echo 'Ollama esta em execucao.' } catch { echo 'Iniciando Ollama...'; Start-Process 'ollama' -ArgumentList 'serve' -WindowStyle Hidden -ErrorAction SilentlyContinue }}"

REM Aguardar alguns segundos para o Ollama iniciar
timeout /t 5 /nobreak > nul

REM Iniciar o aplicativo principal
echo Iniciando o Assistente de Codigo...
start "" "%~dp0CodeAssistant.exe"