import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List Application")
        self.geometry("500x600")
        self.resizable(0, 0)

        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        self.task_entry = tk.Entry(self, width=50)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.add_button = tk.Button(self, text="Add Task", command=self.add_task, width=20, bg="lightgreen")
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.tasks_listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=50, height=20)
        self.tasks_listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=2, sticky='ns')
        self.tasks_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tasks_listbox.yview)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task, width=20, bg="red")
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self, text="Update Task", command=self.update_task, width=20, bg="lightblue")
        self.update_button.grid(row=2, column=1, padx=10, pady=10)

        self.complete_button = tk.Button(self, text="Mark as Complete", command=self.complete_task, width=20, bg="lightyellow")
        self.complete_button.grid(row=2, column=2, padx=10, pady=10)

        self.priority_button = tk.Button(self, text="Set Priority", command=self.set_priority, width=20, bg="orange")
        self.priority_button.grid(row=3, column=0, padx=10, pady=10)

        self.filter_button = tk.Button(self, text="Filter Tasks", command=self.filter_tasks, width=20, bg="lightgrey")
        self.filter_button.grid(row=3, column=1, padx=10, pady=10)

        self.view_all_button = tk.Button(self, text="View All Tasks", command=self.view_tasks, width=20, bg="lightblue")
        self.view_all_button.grid(row=3, column=2, padx=10, pady=10)

        self.filter_entry = tk.Entry(self, width=50)
        self.filter_entry.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

    def create_database(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT,
                priority INTEGER,
                completed BOOLEAN
            )
        ''')
        self.conn.commit()
        self.view_tasks()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.cursor.execute('INSERT INTO tasks (task, priority, completed) VALUES (?, ?, ?)', (task, 0, 0))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.view_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty")

    def delete_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split('.')[0]
            self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            self.conn.commit()
            self.view_tasks()
        except:
            messagebox.showwarning("Warning", "Please select a task to delete")

    def update_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split('.')[0]
            new_task = self.task_entry.get()
            self.cursor.execute('UPDATE tasks SET task=? WHERE id=?', (new_task, task_id))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.view_tasks()
        except:
            messagebox.showwarning("Warning", "Please select a task to update")

    def complete_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split('.')[0]
            self.cursor.execute('UPDATE tasks SET completed=? WHERE id=?', (1, task_id))
            self.conn.commit()
            self.view_tasks()
        except:
            messagebox.showwarning("Warning", "Please select a task to mark as complete")

    def set_priority(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split('.')[0]
            priority = int(self.task_entry.get())
            self.cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (priority, task_id))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.view_tasks()
        except ValueError:
            messagebox.showwarning("Warning", "Priority must be an integer")
        except:
            messagebox.showwarning("Warning", "Please select a task to set priority")

    def filter_tasks(self):
        filter_text = self.filter_entry.get()
        self.cursor.execute('SELECT * FROM tasks WHERE task LIKE ?', ('%' + filter_text + '%',))
        tasks = self.cursor.fetchall()
        self.display_tasks(tasks)

    def view_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()
        self.display_tasks(tasks)

    def display_tasks(self, tasks):
        self.tasks_listbox.delete(0, tk.END)
        for task in tasks:
            task_text = f"{task[0]}. {task[1]} - Priority: {task[2]} - {'Completed' if task[3] else 'Not Completed'}"
            self.tasks_listbox.insert(tk.END, task_text)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
