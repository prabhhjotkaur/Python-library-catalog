"""
gui.py — Simple Tkinter Interface for Library Catalog (Unit-3 Syllabus)
=======================================================================
Directly addresses:
  - Tkinter Window and standard Widgets (Label, Entry, Button, Text, Combobox)
  - Experiment 6: Demonstrates PACK, GRID, and PLACE geometry managers
"""

import tkinter as tk
from tkinter import ttk, messagebox
from library import LibraryCatalog, FictionBook, NonFictionBook, ReferenceBook

class LibraryGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Library Catalog System")
        self.root.geometry("700x560")
        self.root.configure(bg="#f8f9fa")

        self.catalog = LibraryCatalog()

        # 1. HEADER using PACK geometry manager
        self.header_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        self.title_lbl = tk.Label(
            self.header_frame,
            text="📚 Library Catalog Management System",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        self.title_lbl.pack()

        # 2. CONTROLS using GRID geometry manager
        self.grid_frame = tk.LabelFrame(
            self.root,
            text=" Search & Transaction Controls (GRID Layout) ",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=12,
            pady=10
        )
        self.grid_frame.pack(fill=tk.X, padx=12, pady=8)

        # Row 0: Search
        tk.Label(self.grid_frame, text="Search Book:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.search_entry = tk.Entry(self.grid_frame, width=28)
        self.search_entry.grid(row=0, column=1, padx=8, pady=4)

        self.btn_search = tk.Button(self.grid_frame, text="Search Title/Author", command=self.search_books, bg="#3498db", fg="white")
        self.btn_search.grid(row=0, column=2, padx=5, pady=4)

        self.btn_show_all = tk.Button(self.grid_frame, text="Show All Books", command=self.display_all, bg="#7f8c8d", fg="white")
        self.btn_show_all.grid(row=0, column=3, padx=5, pady=4)

        # Row 1: Borrow / Return by ID
        tk.Label(self.grid_frame, text="Book ID:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.id_entry = tk.Entry(self.grid_frame, width=28)
        self.id_entry.grid(row=1, column=1, padx=8, pady=4)

        self.btn_borrow = tk.Button(self.grid_frame, text="Borrow Book", command=self.borrow_book, bg="#27ae60", fg="white")
        self.btn_borrow.grid(row=1, column=2, padx=5, pady=4)

        self.btn_return = tk.Button(self.grid_frame, text="Return Book", command=self.return_book, bg="#e67e22", fg="white")
        self.btn_return.grid(row=1, column=3, padx=5, pady=4)

        # 3. DISPLAY AREA using PACK geometry manager
        self.display_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=5)

        self.text_area = tk.Text(self.display_frame, font=("Courier", 10), bg="#ffffff", relief=tk.SOLID, bd=1)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 4. FOOTER BUTTONS using PLACE geometry manager (Experiment 6 demo)
        self.footer_frame = tk.Frame(self.root, bg="#ecf0f1", height=50)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        demo_label = tk.Label(self.footer_frame, text="Geometry Demo: Header=Pack | Inputs=Grid | Buttons Below=Place", font=("Arial", 8, "italic"), bg="#ecf0f1", fg="#7f8c8d")
        demo_label.place(x=10, y=14)

        # Place buttons specifically at x, y coordinates
        btn_avail = tk.Button(self.footer_frame, text="View Available", command=self.show_available, bg="#2980b9", fg="white")
        btn_avail.place(x=480, y=10, width=110, height=30)

        btn_exit = tk.Button(self.footer_frame, text="Exit", command=self.root.quit, bg="#c0392b", fg="white")
        btn_exit.place(x=600, y=10, width=80, height=30)

        self.display_all()

    def display_all(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "=== COMPLETE LIBRARY CATALOG ===\n\n")
        for book in self.catalog.books.values():
            self.text_area.insert(tk.END, book.display_details() + "\n")

    def show_available(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "=== CURRENTLY AVAILABLE BOOKS ===\n\n")
        available = self.catalog.get_available_books()
        if not available:
            self.text_area.insert(tk.END, "No books currently available.\n")
        for b in available:
            self.text_area.insert(tk.END, b.display_details() + "\n")

    def search_books(self):
        query = self.search_entry.get().strip()
        if not query:
            self.display_all()
            return
        results = self.catalog.search_by_title(query) + self.catalog.search_by_author(query)
        # Deduplicate results using a list
        seen_ids = set()
        unique = []
        for b in results:
            if b.book_id not in seen_ids:
                seen_ids.add(b.book_id)
                unique.append(b)

        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, f"=== SEARCH RESULTS FOR '{query}' ===\n\n")
        if not unique:
            self.text_area.insert(tk.END, "No matching books found.\n")
        for b in unique:
            self.text_area.insert(tk.END, b.display_details() + "\n")

    def borrow_book(self):
        b_id = self.id_entry.get().strip().upper()
        if not b_id:
            messagebox.showwarning("Input Required", "Please enter a Book ID.")
            return
        success, msg = self.catalog.borrow_book(b_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.display_all()
        else:
            messagebox.showerror("Notice", msg)

    def return_book(self):
        b_id = self.id_entry.get().strip().upper()
        if not b_id:
            messagebox.showwarning("Input Required", "Please enter a Book ID.")
            return
        success, msg = self.catalog.return_book(b_id)
        if success:
            messagebox.showinfo("Success", msg)
            self.display_all()
        else:
            messagebox.showerror("Notice", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
