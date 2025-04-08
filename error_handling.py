from CTkMessagebox import CTkMessagebox
import traceback

def handle_error(context, error):
    error_msg = f"""
    Erro em: {context}
    Tipo: {type(error).__name__}
    Mensagem: {str(error)}
    Traceback: {traceback.format_exc()}
    """
    CTkMessagebox(
        title="Erro",
        message=f"Ocorreu um erro: {context}\n{str(error)}",
        icon="cancel"
    )
    # Logar erro em arquivo
    with open("error_log.txt", "a") as f:
        f.write(error_msg)