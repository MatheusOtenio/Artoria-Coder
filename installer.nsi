; Definir nome e versão do produto
!define PRODUCT_NAME "Assistente de Código Local"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Seu Nome"
!define PRODUCT_WEB_SITE "http://www.seusite.com/"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\CodeAssistant.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; Incluir bibliotecas NSIS
!include "MUI2.nsh"
!include "LogicLib.nsh"

; Interface MUI (Modern UI)
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

; Páginas do instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas do desinstalador
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Idiomas suportados
!insertmacro MUI_LANGUAGE "Portuguese"

; Arquivo de saída do instalador
OutFile "AssistenteCodigo_Setup.exe"

; Diretório de instalação padrão
InstallDir "$PROGRAMFILES\Assistente de Código"

; Mostra detalhes da instalação
ShowInstDetails show

Section "Principal" SEC01
  SetOutPath "$INSTDIR"
  
  ; Adicionar arquivos ao instalador
  File "dist\CodeAssistant.exe"
  File "dist\setup.exe"
  File "icon.ico"
  File /r "dist\vendors"
  File "settings.json"
  
  ; Criar atalhos
  CreateDirectory "$SMPROGRAMS\Assistente de Código"
  CreateShortCut "$SMPROGRAMS\Assistente de Código\Assistente de Código.lnk" "$INSTDIR\CodeAssistant.exe"
  CreateShortCut "$DESKTOP\Assistente de Código.lnk" "$INSTDIR\CodeAssistant.exe"
  
  ; Registrar aplicativo
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\CodeAssistant.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  
  ; Criar desinstalador
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  ; Executar script de setup para verificar dependências
  ExecWait '"$INSTDIR\setup.exe"'
SectionEnd

Section "Uninstall"
  ; Remover arquivos e diretórios
  Delete "$INSTDIR\CodeAssistant.exe"
  Delete "$INSTDIR\setup.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\settings.json"
  RMDir /r "$INSTDIR\vendors"
  
  ; Remover atalhos
  Delete "$SMPROGRAMS\Assistente de Código\Assistente de Código.lnk"
  Delete "$DESKTOP\Assistente de Código.lnk"
  RMDir "$SMPROGRAMS\Assistente de Código"
  
  ; Remover registros
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_DIR_REGKEY}"
  
  ; Perguntar se deseja remover Ollama
  MessageBox MB_YESNO "Deseja remover o Ollama também?" IDNO SkipOllamaUninstall
    ExecWait 'taskkill /f /im ollama.exe'
    Delete "$PROGRAMFILES\Ollama\ollama.exe"
    RMDir "$PROGRAMFILES\Ollama"
  SkipOllamaUninstall:
  
  ; Remover diretório de instalação
  RMDir "$INSTDIR"
SectionEnd