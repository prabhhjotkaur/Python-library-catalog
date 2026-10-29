"""
cli.py — Command-Line Interface for Library Catalog (Unit-1 Syllabus)
=====================================================================
Simple CLI to interact with the Library Catalog using functions,
while loops, if-else statements, and basic print/input operations.
"""

from library import LibraryCatalog, FictionBook, NonFictionBook, ReferenceBook

def main():
    catalog = LibraryCatalog()

    while True:
        print("\n" + "=" * 50)
        print("    LIBRARY CATALOG SYSTEM (CLI)")
        print("=" * 50)
        print("1. Display All Books")
        print("2. Display Available Books")
        print("3. Search Book by Title or Author")
        print("4. Borrow a Book")
        print("5. Return a Book")
        print("6. Add a New Book")
        print("7. Exit")
        print("-" * 50)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            print("\n--- ALL BOOKS IN CATALOG ---")
            for b in catalog.books.values():
                print(b.display_details())

        elif choice == "2":
            print("\n--- CURRENTLY AVAILABLE BOOKS ---")
            avail = catalog.get_available_books()
            if not avail:
                print("No books available.")
            for b in avail:
                print(b.display_details())

        elif choice == "3":
            term = input("Enter title or author keyword: ").strip()
            results = catalog.search_by_title(term) + catalog.search_by_author(term)
            seen = set()
            found = False
            print(f"\n--- SEARCH RESULTS FOR '{term}' ---")
            for b in results:
                if b.book_id not in seen:
                    seen.add(b.book_id)
                    print(b.display_details())
                    found = True
            if not found:
                print("No matching books found.")

        elif choice == "4":
            b_id = input("Enter Book ID to borrow: ").strip().upper()
            success, msg = catalog.borrow_book(b_id)
            print("Status:", msg)

        elif choice == "5":
            b_id = input("Enter Book ID to return: ").strip().upper()
            success, msg = catalog.return_book(b_id)
            print("Status:", msg)

        elif choice == "6":
            print("\nSelect Book Type: 1. Fiction | 2. Non-Fiction | 3. Reference")
            b_type = input("Choice (1-3): ").strip()
            b_id = input("Book ID: ").strip().upper()
            title = input("Title: ").strip()
            author = input("Author: ").strip()

            if b_type == "1":
                genre = input("Fiction Genre (e.g. Fantasy): ").strip()
                book = FictionBook(b_id, title, author, genre)
            elif b_type == "2":
                sub = input("Subject (e.g. Science): ").strip()
                book = NonFictionBook(b_id, title, author, sub)
            else:
                ed = input("Edition (e.g. 2nd Ed): ").strip()
                book = ReferenceBook(b_id, title, author, ed)

            catalog.add_book(book)
            print(f"Book '{title}' added successfully!")

        elif choice == "7":
            print("Thank you for using the Library Catalog System!")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    main()
