import customtkinter as ctk
from github_api import clone_repo
from code_parser import CodeParser  # Import CodeParser class
from ia_local import query_ai
from error_handling import handle_error  # Import error handling

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CodeAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Assistente de Código Local")
        self.geometry("1000x700")
        
        # Initialize CodeParser
        self.code_parser = CodeParser()  # Added initialization
        
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
        
        self.project_data = None
    
    def clone_and_analyze(self):
        try:
            repo_url = self.repo_entry.get()
            if repo_url:
                clone_path = clone_repo(repo_url)
                if clone_path:
                    # Use the code_parser instance to analyze the project
                    self.project_data = self.code_parser.analyze_project(clone_path)
                    self.add_message("Sistema", "Projeto analisado com sucesso!")
                else:
                    self.add_message("Sistema", "Falha ao clonar repositório.")
        except Exception as e:
            handle_error("Clone e Análise", e)
    
    def send_question(self):
        try:
            question = self.user_input.get()
            if question and self.project_data:
                context = f"Projeto: {self.project_data}\nPergunta: {question}"
                response = query_ai(context)
                self.add_message("Você", question)
                self.add_message("IA", response)
                self.user_input.delete(0, 'end')  # Clear input after sending
        except Exception as e:
            handle_error("Envio de Pergunta", e)
    
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
        except Exception as e:
            print(f"Error adding message: {e}")

if __name__ == "__main__":
    try:
        app = CodeAssistantApp()
        app.mainloop()
    except Exception as e:
        handle_error("Inicialização da aplicação", e)