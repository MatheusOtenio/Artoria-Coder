import customtkinter as ctk
import os
from tkinter import ttk
from error_handling import handle_error  # Added import

class ProjectTreeView(ctk.CTkFrame):
    def __init__(self, parent, select_callback):
        super().__init__(parent)
        self.select_callback = select_callback
        
        self.tree = ttk.Treeview(self, style="Custom.Treeview")
        self.tree.pack(expand=True, fill='both')
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#2b2b2b", foreground="white")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def build_tree(self, project_path):
        try:
            self.tree.delete(*self.tree.get_children())
            root_node = self.tree.insert('', 'end', text=project_path.name, open=True)
            self._populate_tree(root_node, project_path)
        except Exception as e:
            handle_error("Construção da Árvore de Projeto", e)

    def _populate_tree(self, parent, path):
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    node = self.tree.insert(parent, 'end', text=item, tags=('dir',))
                    self._populate_tree(node, full_path)
                else:
                    self.tree.insert(parent, 'end', text=item, tags=('file',))
        except Exception as e:
            pass

    def on_select(self, event):
        try:
            item = self.tree.selection()[0]
            path = self._get_full_path(item)
            self.select_callback(path)
        except Exception as e:
            handle_error("Seleção de Arquivo", e)

    def _get_full_path(self, item):
        path = []
        while item:
            path.append(self.tree.item(item, 'text'))
            item = self.tree.parent(item)
        return os.path.join(*reversed(path))