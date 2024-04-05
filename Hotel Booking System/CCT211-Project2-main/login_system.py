import tkinter as tk
from tkinter import messagebox


class Login:
    def __init__(self, root, on_login_success):
        self.root = root

        self.title_label = tk.Label(self.root, text="Z Hotel Reservation Management System",
                                    font=("Courier New", 15, "bold"), fg="#274b6c")
        self.title_label.pack(side=tk.TOP, padx=10, pady=15)

        self.on_login_success = on_login_success #check if user entered correct username and password

        tk.Label(self.root, text="Username:", font=("Courier New", 10, "bold"), fg="#274b6c").pack()
        self.username_entry = tk.Entry(self.root, width=20)
        self.username_entry.pack(padx=5, pady=5)

        tk.Label(self.root, text="Password:", font=("Courier New", 10, "bold"), fg="#274b6c").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=20)
        self.password_entry.pack(padx=5, pady=5)

        tk.Button(self.root, text="Login", command=self.check_login, font=("Courier New", 10, "bold"), bg="#274b6c",
                  fg="white").pack(padx=10, pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "211" and password == "211":
            if self.on_login_success:
                self.root.destroy() #Close the login window
                self.on_login_success()
        else:
            messagebox.showerror("Login Fail", "Username or Password wrong")

