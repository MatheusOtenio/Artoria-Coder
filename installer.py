import os
import sys
import shutil
import subprocess
from pathlib import Path
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def create_shortcut(target_path, shortcut_path, working_dir='', icon_path=''):
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        if working_dir:
            shortcut.WorkingDirectory = working_dir
        if icon_path:
            shortcut.IconLocation = icon_path
        shortcut.save()
        return True
    except Exception as e:
        print(f"Erro ao criar atalho: {e}")
        return False

def add_to_path(directory):
    try:
        # Abrir chave do registro para PATH
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r'Environment', 
            0, 
            winreg.KEY_ALL_ACCESS
        )
        
        # Obter valor atual do PATH
        current_path, _ = winreg.QueryValueEx(key, 'PATH')
        
        # Adicionar diretório se ainda não estiver no PATH
        if directory not in current_path:
            new_path = current_path + ';' + directory
            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
            
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Erro ao adicionar diretório ao PATH: {e}")
        return False

def install_application():
    print("Iniciando instalação do Assistente de Código...")
    
    # Determinar diretórios
    if getattr(sys, 'frozen', False):
        # Executando como executável
        source_dir = os.path.dirname(sys.executable)
    else:
        # Executando como script
        source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Diretório de instalação
    install_dir = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Assistente de Código')
    
    # Criar diretório de instalação se não existir
    os.makedirs(install_dir, exist_ok=True)
    
    # Copiar arquivos
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(install_dir, item)
        
        if os.path.isfile(s):
            shutil.copy2(s, d)
        elif os.path.isdir(s):
            if item not in ['.git', '__pycache__']:
                shutil.copytree(s, d, dirs_exist_ok=True)
    
    # Criar atalhos
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    start_menu_path = os.path.join(os.environ.get('APPDATA', ''), 
                                 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Assistente de Código')
    
    os.makedirs(start_menu_path, exist_ok=True)
    
    exe_path = os.path.join(install_dir, 'CodeAssistant.exe')
    icon_path = os.path.join(install_dir, 'icon.ico')
    
    create_shortcut(
        exe_path,
        os.path.join(desktop_path, 'Assistente de Código.lnk'),
        working_dir=install_dir,
        icon_path=icon_path
    )
    
    create_shortcut(
        exe_path,
        os.path.join(start_menu_path, 'Assistente de Código.lnk'),
        working_dir=install_dir,
        icon_path=icon_path
    )
    
    # Adicionar ao PATH
    add_to_path(install_dir)
    
    print(f"Instalação concluída em: {install_dir}")
    
    # Executar verificação de dependências
    setup_script = os.path.join(install_dir, 'setup.py')
    if os.path.exists(setup_script):
        print("Verificando dependências...")
        subprocess.run([sys.executable, setup_script])
    
    return True

if __name__ == "__main__":
    # Verificar se está sendo executado como administrador
    if not is_admin():
        print("Esta instalação requer privilégios de administrador.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    
    # Instalar aplicação
    success = install_application()
    
    if success:
        print("Instalação concluída com sucesso!")
    else:
        print("Ocorreram erros durante a instalação.")
    
    input("Pressione Enter para sair...")