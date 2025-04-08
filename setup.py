import os
import sys
import subprocess
import platform
import shutil
import tempfile
import zipfile
import urllib.request
import ctypes
from pathlib import Path
import time

def is_admin():
    """Verifica se o script está sendo executado como administrador."""
    try:
        if platform.system() == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # No Unix, verificar se UID é 0 (root)
            return os.geteuid() == 0
    except:
        return False

def run_as_admin():
    """Reinicia o script com privilégios de administrador."""
    if platform.system() == 'Windows':
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        args = ['sudo', sys.executable] + sys.argv
        subprocess.call(args)

def is_ollama_installed():
    """Verifica se o Ollama está instalado."""
    try:
        if platform.system() == 'Windows':
            # Verificar se o executável existe no Path
            for path in os.environ["PATH"].split(os.pathsep):
                exe_path = os.path.join(path, "ollama.exe")
                if os.path.isfile(exe_path):
                    return True
            return False
        else:
            # Linux/Mac
            return shutil.which("ollama") is not None
    except:
        return False

def is_ollama_running():
    """Verifica se o Ollama está em execução."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Inicia o serviço Ollama."""
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar até que o serviço esteja ativo
        for _ in range(30):  # Esperar até 30 segundos
            if is_ollama_running():
                return True
            time.sleep(1)
        return False
    except Exception as e:
        print(f"Erro ao iniciar Ollama: {e}")
        return False

def ensure_model_installed(model_name="deepseek-coder"):
    """Verifica se o modelo está instalado, caso contrário instala."""
    try:
        # Verificar se o modelo já está instalado
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if model_name in result.stdout:
            print(f"Modelo {model_name} já está instalado.")
            return True
        
        # Instalar o modelo
        print(f"Instalando modelo {model_name}. Isso pode levar algum tempo...")
        subprocess.run(["ollama", "pull", model_name], check=True)
        return True
    except Exception as e:
        print(f"Erro ao verificar/instalar modelo: {e}")
        return False

def download_ollama():
    """Baixa o Ollama para o sistema operacional atual."""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    download_url = None
    if system == 'windows':
        if 'amd64' in arch or 'x86_64' in arch:
            download_url = "https://ollama.com/download/ollama-windows-amd64.zip"
        elif 'arm64' in arch:
            download_url = "https://ollama.com/download/ollama-windows-arm64.zip"
    elif system == 'darwin':  # macOS
        if 'arm64' in arch:
            download_url = "https://ollama.com/download/ollama-darwin-arm64"
        else:
            download_url = "https://ollama.com/download/ollama-darwin-amd64"
    elif system == 'linux':
        if 'amd64' in arch or 'x86_64' in arch:
            download_url = "https://ollama.com/download/ollama-linux-amd64"
        elif 'arm64' in arch:
            download_url = "https://ollama.com/download/ollama-linux-arm64"
    
    if not download_url:
        print(f"Sistema não suportado: {system} {arch}")
        return False
    
    # Baixar o arquivo
    print(f"Baixando Ollama de {download_url}...")
    temp_dir = tempfile.mkdtemp()
    
    if system == 'windows':
        zip_path = os.path.join(temp_dir, "ollama.zip")
        urllib.request.urlretrieve(download_url, zip_path)
        
        # Extrair o arquivo zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Mover para o diretório do programa
        program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        ollama_dir = os.path.join(program_files, "Ollama")
        
        if not os.path.exists(ollama_dir):
            os.makedirs(ollama_dir)
        
        # Copiar executável
        shutil.copy(os.path.join(temp_dir, "ollama.exe"), ollama_dir)
        
        # Adicionar ao PATH
        path_cmd = f'setx PATH "%PATH%;{ollama_dir}"'
        subprocess.run(path_cmd, shell=True)
        
        # Adicionar ao PATH atual para uso imediato
        os.environ["PATH"] += os.pathsep + ollama_dir
    else:
        # Linux/Mac
        binary_path = os.path.join(temp_dir, "ollama")
        urllib.request.urlretrieve(download_url, binary_path)
        
        # Tornar executável
        os.chmod(binary_path, 0o755)
        
        # Mover para /usr/local/bin
        target_path = "/usr/local/bin/ollama"
        shutil.move(binary_path, target_path)
    
    # Limpar diretório temporário
    shutil.rmtree(temp_dir)
    return True

def check_system_requirements():
    """Verifica se o sistema atende aos requisitos mínimos."""
    # Verificar espaço em disco (pelo menos 10 GB livres)
    try:
        if platform.system() == 'Windows':
            free_space = shutil.disk_usage('C:\\').free
        else:
            free_space = shutil.disk_usage('/').free
        
        # Converter para GB
        free_space_gb = free_space / (1024 ** 3)
        if free_space_gb < 10:
            print(f"Aviso: Espaço em disco limitado ({free_space_gb:.1f} GB). Recomendamos pelo menos 10 GB.")
            return False
    except:
        print("Não foi possível verificar o espaço em disco disponível.")
    
    # Verificar RAM
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        if ram_gb < 8:
            print(f"Aviso: Memória RAM limitada ({ram_gb:.1f} GB). Recomendamos pelo menos 8 GB.")
            return False
    except:
        print("Não foi possível verificar a quantidade de RAM disponível.")
    
    return True

def setup_environment():
    """Configura o ambiente necessário para o programa funcionar."""
    # Verificar se as dependências Python estão instaladas
    try:
        import customtkinter
        import requests
        import git
        from CTkMessagebox import CTkMessagebox
    except ImportError as e:
        print(f"Instalando dependências Python: {e.name}")
        subprocess.run([sys.executable, "-m", "pip", "install", e.name])
    
    # Verificar e instalar Ollama se necessário
    if not is_ollama_installed():
        print("Ollama não está instalado. Iniciando processo de instalação...")
        if not is_admin():
            print("Precisamos de permissões de administrador para instalar o Ollama.")
            run_as_admin()
            sys.exit(0)
        
        if download_ollama():
            print("Ollama foi instalado com sucesso!")
        else:
            print("Falha ao instalar Ollama. Por favor, instale manualmente de https://ollama.com")
            input("Pressione Enter para continuar...")
            return False
    
    # Iniciar Ollama se não estiver em execução
    if not is_ollama_running():
        print("Iniciando servidor Ollama...")
        if not start_ollama():
            print("Não foi possível iniciar o servidor Ollama. Por favor, inicie manualmente.")
            input("Pressione Enter para continuar...")
            return False
    
    # Verificar se o modelo necessário está instalado
    print("Verificando modelos de IA...")
    if not ensure_model_installed():
        print("Não foi possível verificar ou instalar os modelos necessários.")
        input("Pressione Enter para continuar...")
        return False
    
    return True

def main():
    """Função principal para configurar e iniciar o programa."""
    print("=== Assistente de Código Local - Instalação e Configuração ===")
    print("Verificando requisitos do sistema...")
    
    # Verificar requisitos do sistema
    check_system_requirements()
    
    # Configurar ambiente
    if not setup_environment():
        return
    
    print("Configuração concluída! Iniciando aplicação...")
    
    # Iniciar o programa principal
    try:
        # Verificar se está sendo executado como executável ou como script
        if getattr(sys, 'frozen', False):
            # Executando como executável empacotado
            app_dir = os.path.dirname(sys.executable)
            main_script = os.path.join(app_dir, "main.exe")
            if os.path.exists(main_script):
                subprocess.Popen([main_script])
            else:
                print(f"Não foi possível encontrar o executável principal em {main_script}")
        else:
            # Executando como script Python
            main_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
            if os.path.exists(main_script):
                subprocess.Popen([sys.executable, main_script])
            else:
                print(f"Não foi possível encontrar o script main.py em {main_script}")
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()