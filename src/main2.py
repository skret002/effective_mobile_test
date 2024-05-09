import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.models.model import WalletAction


class WalletGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wallet GUI @by Tarasenko A.V ")

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # Баланс
        self.balance_frame = ttk.LabelFrame(self.master, text="Баланс")
        self.balance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.balance_label = ttk.Label(self.balance_frame, text="")
        self.balance_label.grid(row=0, column=0, padx=10, pady=10)

        self.income_label = ttk.Label(self.balance_frame, text="")
        self.income_label.grid(row=1, column=0, padx=10, pady=10)

        self.consumption_label = ttk.Label(self.balance_frame, text="")
        self.consumption_label.grid(row=2, column=0, padx=10, pady=10)

        # Добавление записи
        self.add_frame = ttk.LabelFrame(self.master, text="Добавить запись")
        self.add_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.category_label = ttk.Label(self.add_frame, text="Категория:")
        self.category_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.category_combobox = ttk.Combobox(self.add_frame, values=["Доход", "Расход"])
        self.category_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.value_label = ttk.Label(self.add_frame, text="Сумма:")
        self.value_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.value_entry = ttk.Entry(self.add_frame)
        self.value_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.description_label = ttk.Label(self.add_frame, text="Описание:")
        self.description_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = ttk.Entry(self.add_frame)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.note_label = ttk.Label(self.add_frame, text="Примечание:")
        self.note_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.note_entry = ttk.Entry(self.add_frame)
        self.note_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.add_button = ttk.Button(self.add_frame, text="Добавить", command=self.add_entry)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Поиск
        self.search_frame = ttk.LabelFrame(self.master, text="Поиск")
        self.search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.search_label = ttk.Label(self.search_frame, text="Ключевое слово:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.search_button = ttk.Button(self.search_frame, text="Поиск", command=self.search)
        self.search_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.results_listbox = tk.Listbox(self.search_frame, width=50)
        self.results_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Последние записи
        self.last_frame = ttk.LabelFrame(self.master, text="Последние записи")
        self.last_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.last_listbox = tk.Listbox(self.last_frame, width=50)
        self.last_listbox.grid(row=0, column=0, padx=10, pady=10)

        self.delete_button = ttk.Button(self.last_frame, text="Удалить", command=self.delete_post)
        self.delete_button.grid(row=1, column=0, padx=10, pady=10)

        self.update_balance()
        self.update_last_posts()

    def update_balance(self):
        result = WalletAction.check_balance()
        if result:
            self.balance_label.configure(text=f"Баланс: {result['balance']}")
            self.income_label.configure(text=f"Доходы: {result['income']}")
            self.consumption_label.configure(text=f"Расходы: {result['consumption']}")
        else:
            self.balance_label.configure(text="Нет данных для отображения.")

    def update_last_posts(self):
        results = WalletAction.get_some_last_post(0)
        self.last_listbox.delete(0, tk.END)
        if results:
            for result in results:
                self.last_listbox.insert(tk.END, result[0])

    def add_entry(self):
        category = self.category_combobox.get()
        value = self.value_entry.get()
        description = self.description_entry.get()
        note = self.note_entry.get()

        if not category or not value or not description or not note:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            value = float(value)
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом.")
            return

        new_data = {
            "category": category,
            "value": value,
            "description": description,
            "note": note,
        }
        result = WalletAction.write_data(new_data)
        messagebox.showinfo("Успех", result)
        self.update_balance()
        self.update_last_posts()
        self.clear_add_form()

    def clear_add_form(self):
        self.category_combobox.set("")
        self.value_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

    def search(self):
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showerror("Ошибка", "Пожалуйста, введите ключевое слово.")
            return

        results = WalletAction.search_data(keyword)
        self.results_listbox.delete(0, tk.END)
        if results:
            for result in results:
                self.results_listbox.insert(tk.END, result[0])
        else:
            messagebox.info("Результат", "Ничего не найдено по вашему запросу.")

    def delete_post(self):
        # Запрос ID записи или команды на удаление всех записей
        post_id = simpledialog.askstring(
            "Удаление записи",
            "Введите Id записи для ее удаления или введите 'YES' для удаления всех записей",
        )

        if post_id is not None:
            if post_id.strip().upper() == "YES":
                # Удаление всех записей
                result = WalletAction.delete_post(None)
                messagebox.showinfo("Успех", "Все записи удалены.")
            else:
                # Удаление одной записи по ID
                result = WalletAction.delete_post(int(post_id))
                if result:
                    messagebox.showinfo("Успех", f"Запись с ID {post_id} удалена.")
                else:
                    messagebox.showerror(
                        "Ошибка", f"Не удалось найти запись с ID {post_id}."
                    )

            self.update_balance()
            self.update_last_posts()


def main():
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()