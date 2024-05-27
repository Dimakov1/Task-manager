import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('todo.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name VARCHAR(50) NOT NULL,
                description TEXT,
                due_date TEXT,
                important BOOLEAN NOT NULL CHECK (important IN (0, 1)),
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
            )
        """)

    def create_task(self, user_id, name, description, due_date = ""):
        try:
            self.cursor.execute("INSERT INTO tasks(user_id, name, description, due_date, important, completed) VALUES(?, ?, ?, ?, ?, ?)", (user_id, name, description, due_date, 0, 0))
            self.con.commit()
            created_task = self.cursor.execute("SELECT id, name, description, due_date, important, completed FROM tasks WHERE user_id = ? AND name = ? ORDER BY id DESC", (user_id, name)).fetchone()
            return created_task
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def get_tasks(self, user_id):
        try:
            complete_tasks = self.cursor.execute("SELECT id, name, description, due_date, important FROM tasks WHERE user_id = ? AND completed = 1", (user_id,)).fetchall()
            incomplete_tasks = self.cursor.execute("SELECT id, name, description, due_date, important FROM tasks WHERE user_id = ? AND completed = 0", (user_id,)).fetchall()
            return incomplete_tasks, complete_tasks
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None, None

    def get_favorite_tasks(self, user_id):
        try:
            favorite_tasks = self.cursor.execute("SELECT id, name, description, due_date, important FROM tasks WHERE user_id = ? AND important = 1", (user_id,)).fetchall()

            return favorite_tasks
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None, None



    def mark_task_as_complete(self, user_id, taskid):
        try:
            self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?", (taskid, user_id))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def mark_task_as_incomplete(self, user_id, taskid):
        try:
            self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ? AND user_id = ?", (taskid, user_id))
            self.con.commit()
            task_text = self.cursor.execute("SELECT name, description FROM tasks WHERE id = ? AND user_id = ?", (taskid, user_id)).fetchone()
            return task_text
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def change_task(self, user_id, task_id, tname, tdescription):
        try:
            self.cursor.execute(
                "UPDATE tasks SET name = ?, description = ? WHERE id = ? AND user_id = ?",
                (tname, tdescription, task_id, user_id)
            )
            self.con.commit()
            task_text = self.cursor.execute(
                "SELECT name, description, due_date FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            ).fetchone()
            return task_text
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def mark_task_as_important(self, user_id, taskid):
        try:
            self.cursor.execute("UPDATE tasks SET important = 1 WHERE id = ? AND user_id = ?", (taskid, user_id))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def mark_task_as_unimportant(self, user_id, taskid):
        try:
            self.cursor.execute("UPDATE tasks SET important = 0 WHERE id = ? AND user_id = ?", (taskid, user_id))
            self.con.commit()
            task_text = self.cursor.execute("SELECT name, description FROM tasks WHERE id = ? AND user_id = ?", (taskid, user_id)).fetchone()
            return task_text
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def delete_task(self, user_id, taskid):
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (taskid, user_id))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close_db_connection(self):
        self.con.close()
