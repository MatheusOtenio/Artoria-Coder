import customtkinter as ctk
import threading
from github_api import clone_repo
from code_parser import CodeParser
from ia_local import query_ai, wait_for_ollama
from error_handling import handle_error

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CodeAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Assistente de Código Local")
        self.geometry("1000x700")
        
        # Initialize CodeParser
        self.code_parser = CodeParser()
        
        # Configurar layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Controles superiores
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.repo_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="URL do repositório GitHub...",
            width=400
        )
        self.repo_entry.pack(side="left", padx=5)
        
        self.clone_btn = ctk.CTkButton(
            self.top_frame,
            text="Clonar e Analisar",
            command=self.clone_and_analyze
        )
        self.clone_btn.pack(side="left", padx=5)
        
        # Área de chat
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Entrada do usuário
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.user_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Digite sua pergunta...",
        )
        self.user_input.pack(side="left", expand=True, fill="x", padx=5)
        
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Enviar",
            command=self.send_question
        )
        self.send_btn.pack(side="left", padx=5)
        
        # Indicador de progresso
        self.progress_bar = ctk.CTkProgressBar(self.input_frame)
        self.progress_bar.pack(side="left", padx=5)
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()  # Esconde inicialmente
        
        self.project_data = None
        self.active_tasks = {}  # Para controlar threads ativas
        
        # Adicionar mensagem sobre status do Ollama na inicialização
        threading.Thread(target=self._check_ollama_startup, daemon=True).start()
    
    def _check_ollama_startup(self):
        if not wait_for_ollama(max_retries=1):  # Verificação rápida
            self.after(0, lambda: self.add_message("Sistema", "Aviso: Servidor Ollama não detectado. Verifique se o Ollama está em execução."))
    
    def clone_and_analyze(self):
        try:
            repo_url = self.repo_entry.get()
            if repo_url:
                # Desabilitar botão durante processamento
                self.clone_btn.configure(state="disabled", text="Processando...")
                self._show_progress()
                
                # Mostrar mensagem de processamento
                self.add_message("Sistema", "Clonando e analisando repositório. Por favor aguarde...")
                
                # Executar em uma thread separada
                task_id = "clone_analyze"
                self.active_tasks[task_id] = True
                threading.Thread(
                    target=self._clone_and_analyze_thread, 
                    args=(repo_url, task_id),
                    daemon=True
                ).start()
        except Exception as e:
            self._hide_progress()
            self.clone_btn.configure(state="normal", text="Clonar e Analisar")
            handle_error("Clone e Análise", e)
    
    def _clone_and_analyze_thread(self, repo_url, task_id):
        try:
            # Etapa 1: Clonagem
            self.after(0, lambda: self._update_progress(0.3))
            clone_path = clone_repo(repo_url)
            
            if clone_path:
                # Etapa 2: Análise
                self.after(0, lambda: self._update_progress(0.6))
                self.project_data = self.code_parser.analyze_project(clone_path)
                
                # Atualização final
                self.after(0, lambda: self._update_progress(1.0))
                self.after(0, lambda: self.add_message("Sistema", "Projeto analisado com sucesso!"))
            else:
                self.after(0, lambda: self.add_message("Sistema", "Falha ao clonar repositório."))
        except Exception as e:
            self.after(0, lambda: handle_error("Clone e Análise (Thread)", e))
        finally:
            # Restabelecer UI
            self.after(0, lambda: self._reset_ui_after_task())
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
    
    def _reset_ui_after_task(self):
        self.clone_btn.configure(state="normal", text="Clonar e Analisar")
        self._hide_progress()
    
    def send_question(self):
        try:
            question = self.user_input.get()
            if question and self.project_data:
                # Mostrar pergunta e indicador de processamento
                self.add_message("Você", question)
                self.add_message("IA", "Processando resposta...")
                
                # Mostrar barra de progresso
                self._show_progress()
                
                # Limpar input após envio
                self.user_input.delete(0, 'end')
                
                # Desabilitar botão durante processamento
                self.send_btn.configure(state="disabled", text="Aguarde...")
                
                # Executar em uma thread separada
                task_id = "query_ai"
                self.active_tasks[task_id] = True
                threading.Thread(
                    target=self._process_question_thread, 
                    args=(question, task_id),
                    daemon=True
                ).start()
        except Exception as e:
            self._hide_progress()
            self.send_btn.configure(state="normal", text="Enviar")
            handle_error("Envio de Pergunta", e)
    
    def _process_question_thread(self, question, task_id):
        try:
            # Simular progresso
            self.after(0, lambda: self._update_progress(0.3))
            
            context = f"Projeto: {self.project_data}\nPergunta: {question}"
            response = query_ai(context)
            
            # Atualizar progresso
            self.after(0, lambda: self._update_progress(1.0))
            
            # Atualizar a resposta na thread principal
            self.after(0, lambda: self._update_last_message("IA", response))
        except Exception as e:
            self.after(0, lambda: handle_error("Processamento de Pergunta (Thread)", e))
        finally:
            # Restabelecer UI
            self.after(0, lambda: self.send_btn.configure(state="normal", text="Enviar"))
            self.after(0, lambda: self._hide_progress())
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
    
    def _show_progress(self):
        """Mostra e inicializa a barra de progresso"""
        self.progress_bar.set(0)
        self.progress_bar.grid()
    
    def _hide_progress(self):
        """Esconde a barra de progresso"""
        self.progress_bar.grid_remove()
    
    def _update_progress(self, value):
        """Atualiza o valor da barra de progresso"""
        self.progress_bar.set(value)
    
    def _update_last_message(self, sender, message):
        """Atualiza a última mensagem com o conteúdo completo"""
        try:
            # Remover a mensagem de "Processando..." e adicionar a resposta real
            for widget in self.chat_frame.winfo_children():
                if widget == self.chat_frame.winfo_children()[-1]:  # Último widget
                    widget.destroy()
            self.add_message(sender, message)
        except Exception as e:
            print(f"Error updating message: {e}")
    
    def add_message(self, sender, message):
        try:
            frame = ctk.CTkFrame(self.chat_frame)
            label = ctk.CTkLabel(
                frame,
                text=f"{sender}: {message}",
                wraplength=800,
                justify="left"
            )
            label.pack(padx=5, pady=2)
            frame.pack(fill="x")
            
            # Rolar para mostrar a mensagem mais recente
            self.update_idletasks()
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except Exception as e:
            print(f"Error adding message: {e}")

if __name__ == "__main__":
    try:
        # Verificação do Ollama movida para dentro da classe
        app = CodeAssistantApp()
        app.mainloop()
    except Exception as e:
        handle_error("Inicialização da aplicação", e)