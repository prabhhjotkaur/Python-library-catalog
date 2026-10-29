"""
app.py — Production Web Application for Library Catalog
======================================================
"""

from flask import Flask, render_template, request, jsonify
from library import LibraryCatalog, FictionBook, NonFictionBook, ReferenceBook

app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-catalog-prod-key-2026'

catalog = LibraryCatalog()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/books", methods=["GET"])
def get_books():
    books_data = []
    for b in catalog.books.values():
        category = "General"
        extra = ""
        if isinstance(b, FictionBook):
            category = "Fiction"
            extra = b.sub_genre
        elif isinstance(b, NonFictionBook):
            category = "Non-Fiction"
            extra = b.subject
        elif isinstance(b, ReferenceBook):
            category = "Reference"
            extra = b.edition

        books_data.append({
            "book_id": b.book_id,
            "title": b.title,
            "author": b.author,
            "is_available": b.is_available(),
            "category": category,
            "extra_info": extra,
            "is_reference": isinstance(b, ReferenceBook),
            "cover_url": b.cover_url
        })
    return jsonify({"success": True, "books": books_data, "total": len(books_data)})

@app.route("/api/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json() or {}
    book_id = str(data.get("book_id", "")).strip().upper()
    success, message = catalog.borrow_book(book_id)
    return jsonify({"success": success, "message": message})

@app.route("/api/return", methods=["POST"])
def return_book():
    data = request.get_json() or {}
    book_id = str(data.get("book_id", "")).strip().upper()
    success, message = catalog.return_book(book_id)
    return jsonify({"success": success, "message": message})

@app.route("/api/add", methods=["POST"])
def add_book():
    data = request.get_json() or {}
    book_id = str(data.get("book_id", "")).strip().upper()
    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    book_type = str(data.get("type", "fiction")).strip().lower()
    detail = str(data.get("detail", "")).strip()
    cover_url = str(data.get("cover_url", "")).strip()

    if not book_id or not title or not author:
        return jsonify({"success": False, "message": "Book ID, Title, and Author are required."}), 400

    if book_id in catalog.books:
        return jsonify({"success": False, "message": f"Book with ID '{book_id}' already exists."}), 400

    if book_type == "fiction":
        book = FictionBook(book_id, title, author, detail or "General Fiction", cover_url)
    elif book_type == "non_fiction":
        book = NonFictionBook(book_id, title, author, detail or "General Non-Fiction", cover_url)
    elif book_type == "reference":
        book = ReferenceBook(book_id, title, author, detail or "Standard Reference", cover_url)
    else:
        return jsonify({"success": False, "message": "Invalid book category."}), 400

    catalog.add_book(book)
    return jsonify({"success": True, "message": f"Book '{title}' added to catalog successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
