import tkinter as tk
from tkinter import messagebox


class BPlusTree:
    def __init__(self, degree):
        self.degree = degree
        self.keys = []
        self.children = []

    def insert(self, value):
        if value in self.keys:
            messagebox.showinfo("Inserção", f"Valor '{value}' já existe na árvore B+.")
            return

        self._insert(value)

    def _insert(self, value):
        if len(self.keys) == 0:
            self.keys.append(value)
            return

        for i in range(len(self.keys)):
            if value < self.keys[i]:
                if isinstance(self.children[i], BPlusTree):
                    self.children[i].insert(value)
                    if len(self.children[i].keys) > self.degree:
                        self._split_child(i)
                else:
                    self.keys.insert(i, value)
                    return
        else:
            if isinstance(self.children[-1], BPlusTree):
                self.children[-1].insert(value)
                if len(self.children[-1].keys) > self.degree:
                    self._split_child(len(self.children) - 1)
            else:
                self.keys.append(value)

    def _split_child(self, child_index):
        child = self.children[child_index]
        mid_index = self.degree // 2

        new_child1 = BPlusTree(self.degree)
        new_child2 = BPlusTree(self.degree)

        new_child1.keys = child.keys[:mid_index]
        new_child1.children = child.children[:mid_index + 1]
        new_child2.keys = child.keys[mid_index + 1:]
        new_child2.children = child.children[mid_index + 1:]

        self.children[child_index] = new_child1
        self.children.insert(child_index + 1, new_child2)
        self.keys.insert(child_index, child.keys[mid_index])

    def delete(self, value):
        if value not in self.keys:
            messagebox.showinfo("Exclusão", f"Valor '{value}' não existe na árvore B+.")
            return

        self._delete(value)

    def _delete(self, value):
        for i in range(len(self.keys)):
            if value < self.keys[i]:
                if isinstance(self.children[i], BPlusTree):
                    self.children[i].delete(value)
                    if len(self.children[i].keys) < self.degree // 2:
                        self._borrow_or_merge_child(i)
                else:
                    self.keys.remove(value)
                return
        else:
            if isinstance(self.children[-1], BPlusTree):
                self.children[-1].delete(value)
                if len(self.children[-1].keys) < self.degree // 2:
                    self._borrow_or_merge_child(len(self.children) - 1)
            else:
                self.keys.remove(value)

    def _borrow_or_merge_child(self, child_index):
        if child_index > 0 and len(self.children[child_index - 1].keys) > self.degree // 2:
            self._borrow_from_left(child_index)
        elif child_index < len(self.children) - 1 and len(self.children[child_index + 1].keys) > self.degree // 2:
            self._borrow_from_right(child_index)
        elif child_index > 0:
            self._merge_with_left(child_index)
        else:
            self._merge_with_right(child_index)

    def _borrow_from_left(self, child_index):
        child = self.children[child_index]
        left_sibling = self.children[child_index - 1]

        child.keys.insert(0, self.keys[child_index - 1])
        self.keys[child_index - 1] = left_sibling.keys.pop()
        if isinstance(left_sibling.children[-1], BPlusTree):
            child.children.insert(0, left_sibling.children.pop())

    def _borrow_from_right(self, child_index):
        child = self.children[child_index]
        right_sibling = self.children[child_index + 1]

        child.keys.append(self.keys[child_index])
        self.keys[child_index] = right_sibling.keys.pop(0)
        if isinstance(right_sibling.children[0], BPlusTree):
            child.children.append(right_sibling.children.pop(0))

    def _merge_with_left(self, child_index):
        child = self.children[child_index]
        left_sibling = self.children[child_index - 1]

        left_sibling.keys.append(self.keys.pop(child_index - 1))
        left_sibling.keys.extend(child.keys)
        left_sibling.children.extend(child.children)
        self.children.pop(child_index)

    def _merge_with_right(self, child_index):
        child = self.children[child_index]
        right_sibling = self.children[child_index + 1]

        child.keys.append(self.keys.pop(child_index))
        child.keys.extend(right_sibling.keys)
        child.children.extend(right_sibling.children)
        self.children.pop(child_index + 1)

    def __str__(self):
        return self.get_tree_string()

    def get_tree_string(self, level=0):
        tree_str = ""
        if level == 0:
            tree_str += "Raiz: "
        tree_str += f"({', '.join(map(str, self.keys))})\n"

        for child in self.children:
            if isinstance(child, BPlusTree):
                tree_str += "  " * (level + 1)
                tree_str += child.get_tree_string(level + 1)
            else:
                tree_str += "  " * (level + 1)
                tree_str += f"Folha: {', '.join(map(str, child))}\n"

        return tree_str


class BPlusTreeGUI:
    def __init__(self):
        self.tree = None

        self.root = tk.Tk()
        self.root.title("Árvore B+")

        self.degree_label = tk.Label(self.root, text="Grau de Saída (3-10):")
        self.degree_label.pack()

        self.degree_entry = tk.Entry(self.root)
        self.degree_entry.pack()

        self.create_button = tk.Button(self.root, text="Criar Árvore", command=self.create_tree)
        self.create_button.pack()

        self.value_label = tk.Label(self.root, text="Valor:")
        self.value_label.pack()

        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack()

        self.insert_button = tk.Button(self.root, text="Inserir", command=self.insert_value)
        self.insert_button.pack()

        self.delete_button = tk.Button(self.root, text="Excluir", command=self.delete_value)
        self.delete_button.pack()

        self.view_button = tk.Button(self.root, text="Visualizar", command=self.view_tree)
        self.view_button.pack()

        self.tree_label = tk.Label(self.root, text="Árvore B+")
        self.tree_label.pack()

        self.tree_text = tk.Text(self.root, width=50, height=20)
        self.tree_text.pack()

    def create_tree(self):
        degree = self.degree_entry.get()
        if degree.isdigit() and 3 <= int(degree) <= 10:
            self.tree = BPlusTree(int(degree))
            messagebox.showinfo("Árvore B+", f"Árvore B+ com grau de saída {degree} criada com sucesso.")
        else:
            messagebox.showerror("Erro", "Insira um valor válido para o grau de saída (3-10).")

    def insert_value(self):
        value = self.value_entry.get()
        if self.tree is not None and value:
            self.tree.insert(value)
            messagebox.showinfo("Inserção", f"Valor '{value}' inserido com sucesso na árvore B+.")
        else:
            messagebox.showerror("Erro", "Crie a árvore B+ e insira um valor válido.")

    def delete_value(self):
        value = self.value_entry.get()
        if self.tree is not None and value:
            self.tree.delete(value)
            messagebox.showinfo("Exclusão", f"Valor '{value}' excluído com sucesso da árvore B+.")
        else:
            messagebox.showerror("Erro", "Crie a árvore B+ e insira um valor válido.")

    def view_tree(self):
        if self.tree is not None:
            tree_str = self.tree.get_tree_string()
            self.tree_text.delete("1.0", tk.END)
            self.tree_text.insert(tk.END, tree_str)
        else:
            messagebox.showerror("Erro", "Crie a árvore B+ antes de visualizá-la.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = BPlusTreeGUI()
    gui.run()
