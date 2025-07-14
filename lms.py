import tkinter as tk
from tkinter import messagebox, simpledialog

library = {"books": []}
users = {"admin": "admin"}
current_user = None


def add_book(title, author, isbn):
    if not (title and author and isbn):
        messagebox.showerror("Error", "All fields are required.")
        return
    library["books"].append(
        {"Title": title, "Author": author, "ISBN": isbn, "available": True}
    )
    messagebox.showinfo("Success", f"Book '{title}' added.")


def display_books():
    available = [
        f"{b['Title']} by {b['Author']} (ISBN: {b['ISBN']})"
        for b in library["books"]
        if b["available"]
    ]
    messagebox.showinfo(
        "Available Books", "\n".join(available) if available else "No books available."
    )


def borrow_book(isbn):
    for b in library["books"]:
        if b["ISBN"] == isbn and b["available"]:
            b["available"] = False
            messagebox.showinfo("Success", f"You borrowed '{b['Title']}'.")
            return
    messagebox.showwarning("Unavailable", "Book not available.")


def return_book(isbn):
    for b in library["books"]:
        if b["ISBN"] == isbn and not b["available"]:
            b["available"] = True
            messagebox.showinfo("Success", f"Returned '{b['Title']}'.")
            return
    messagebox.showwarning("Error", "Invalid ISBN or book not borrowed.")


def search_book(query):
    matches = [
        f"{b['Title']} by {b['Author']} (ISBN: {b['ISBN']}) – "
        f"{'Available' if b['available'] else 'Borrowed'}"
        for b in library["books"]
        if query.lower() in b["Title"].lower() or query.lower() in b["Author"].lower()
    ]
    messagebox.showinfo(
        "Search Results", "\n".join(matches) if matches else "No matching books."
    )


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        tk.Button(root, text="Add Book", width=25, command=self.add_book_gui).pack(pady=4)
        tk.Button(root, text="Search Book", width=25, command=self.search_book_gui).pack(
            pady=4
        )
        tk.Button(root, text="Borrow Book", width=25, command=self.borrow_book_gui).pack(
            pady=4
        )
        tk.Button(root, text="Return Book", width=25, command=self.return_book_gui).pack(
            pady=4
        )
        tk.Button(
            root, text="Display Available Books", width=25, command=display_books
        ).pack(pady=4)

        if current_user == "admin":
            tk.Button(root, text="Add User", width=25, command=self.add_user_gui).pack(
                pady=4
            )

        tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=10)

    # ---------- dialogs ----------
    def add_book_gui(self):
        w = tk.Toplevel(self.root)
        w.title("Add Book")
        entries = {}
        for idx, field in enumerate(("Title", "Author", "ISBN")):  # fixed loop
            tk.Label(w, text=field).grid(row=idx, column=0, pady=2, padx=4, sticky="e")
            e = tk.Entry(w, width=32)
            e.grid(row=idx, column=1, pady=2)
            entries[field] = e

        tk.Button(
            w,
            text="Add",
            command=lambda: (
                add_book(
                    entries["Title"].get(),
                    entries["Author"].get(),
                    entries["ISBN"].get(),
                ),
                w.destroy(),
            ),
        ).grid(row=3, column=0, columnspan=2, pady=6)

    def search_book_gui(self):
        query = simpledialog.askstring("Search Book", "Enter book title or author:")
        if query:
            search_book(query)

    def borrow_book_gui(self):
        isbn = simpledialog.askstring("Borrow Book", "Enter ISBN:")
        if isbn:
            borrow_book(isbn)

    def return_book_gui(self):
        isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
        if isbn:
            return_book(isbn)

    def add_user_gui(self):
        username = simpledialog.askstring("Add User", "Username:")
        if not username:
            return
        if username in users:
            messagebox.showwarning("Exists", "User already exists.")
            return
        password = simpledialog.askstring("Add User", "Password:", show="*")
        if password:
            users[username] = password
            messagebox.showinfo("Success", "User added.")


def login():
    for _ in range(3):
        u = simpledialog.askstring("Login", "Username:")
        p = simpledialog.askstring("Login", "Password:", show="*")
        if users.get(u) == p:
            return u
        messagebox.showerror("Error", "Invalid credentials.")
    return None


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()  # hide until login succeeds
    current_user = login()
    if current_user:
        app.deiconify()
        LibraryGUI(app)
        app.mainloop()
