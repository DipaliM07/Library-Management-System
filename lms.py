import sqlite3
import tkinter as tk
from tkinter import messagebox


class LibraryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("500x450")
        self.root.config(bg="#f0f2f5")

        
        self.setup_database()

        # Container Frame
        self.container = tk.Frame(self.root, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def setup_database(self):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # users
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """
        )

        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            default_users = [
                ("admin", "lib123", "Main Librarian"),
                ("staff1", "staff123", "Staff"),
                ("student1", "pass123", "Student"),
            ]
            cursor.executemany(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                default_users,
            )

        conn.commit()
        conn.close()

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- Main Menu Interface ---
    def show_main_menu(self):
        self.clear_frame()

        title_label = tk.Label(
            self.container,
            text="Library Management System",
            font=("Arial", 18, "bold"),
            bg="#f0f2f5",
            fg="#1a73e8",
        )
        title_label.pack(pady=30)

        select_label = tk.Label(
            self.container,
            text="Please Select Your Role To Sign In:",
            font=("Arial", 12),
            bg="#f0f2f5",
        )
        select_label.pack(pady=10)

        # 3 Main Buttons
        btn_librarian = tk.Button(
            self.container,
            text="Main Librarian Sign In",
            font=("Arial", 11, "bold"),
            bg="#1a73e8",
            fg="white",
            width=25,
            height=2,
            command=lambda: self.show_login_page("Main Librarian"),
        )
        btn_librarian.pack(pady=10)

        btn_staff = tk.Button(
            self.container,
            text="Staff Sign In",
            font=("Arial", 11, "bold"),
            bg="#34a853",
            fg="white",
            width=25,
            height=2,
            command=lambda: self.show_login_page("Staff"),
        )
        btn_staff.pack(pady=10)

        btn_student = tk.Button(
            self.container,
            text="Student Sign In",
            font=("Arial", 11, "bold"),
            bg="#fbbc05",
            fg="black",
            width=25,
            height=2,
            command=lambda: self.show_login_page("Student"),
        )
        btn_student.pack(pady=10)

    # --- Login Interface for Different Roles ---
    def show_login_page(self, role):
        self.clear_frame()

        role_label = tk.Label(
            self.container,
            text=f"{role} Sign In",
            font=("Arial", 16, "bold"),
            bg="#f0f2f5",
            fg="#333333",
        )
        role_label.pack(pady=20)

        # Username Field
        lbl_user = tk.Label(
            self.container,
            text="Username / ID:",
            font=("Arial", 10),
            bg="#f0f2f5",
        )
        lbl_user.pack(anchor="w", padx=120)
        entry_user = tk.Entry(self.container, font=("Arial", 11), width=30)
        entry_user.pack(pady=5)

        # Password Field
        lbl_pass = tk.Label(
            self.container, text="Password:", font=("Arial", 10), bg="#f0f2f5"
        )
        lbl_pass.pack(anchor="w", padx=120)
        entry_pass = tk.Entry(
            self.container, font=("Arial", 11), show="*", width=30
        )
        entry_pass.pack(pady=5)

       
        def handle_login():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password FROM users WHERE username = ? AND role = ?",
                (username, role),
            )
            result = cursor.fetchone()
            conn.close()

            if result is None:
                messagebox.showerror(
                    "Error", "Invalid Username for this role!"
                )
            elif result[0] == password:
                messagebox.showinfo(
                    "Login Success",
                    f"Welcome {username}! Logged in as {role}.",
                )
            else:
                messagebox.showerror("Error", "Incorrect Password!")

        # Sign In Button
        btn_login = tk.Button(
            self.container,
            text="Sign In",
            font=("Arial", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            width=15,
            command=handle_login,
        )
        btn_login.pack(pady=15)

        # Back Button
        btn_back = tk.Button(
            self.container,
            text="<- Back to Main Menu",
            font=("Arial", 9),
            bg="#e0e0e0",
            command=self.show_main_menu,
        )
        btn_back.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()