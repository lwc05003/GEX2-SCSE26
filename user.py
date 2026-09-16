from admin import (
    find_book,
    load_library,
    save_library
)


def books_in_category(books, category):
    cat = category.strip().lower()
    result = []
    for book_id, info in books.items():
        if info["category"].strip().lower() == cat:
            result.append(book_id)
    return result


def search_by_title(books, search_text):
    text = search_text.strip().lower()
    result = []
    for book_id, info in books.items():
        if text in info["title"].lower():
            result.append(book_id)
    return result


def borrow_book(books, loans, search_text, borrower):
    if not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    if not books[book_id]["available"]:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower})
    return "OK"


def return_book(books, loans, book_title, borrower):
    if not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    for i, loan in enumerate(loans):
        if loan["book_id"] == book_id and loan["borrower"] == borrower:
            loans.pop(i)
            books[book_id]["available"] = True
            return "OK"

    return "NOT_ON_LOAN"


def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY USER SYSTEM")
    print("=" * 60)

    while True:
        print("\nMenu:")
        print("1. Search books by category")
        print("2. Search books by title")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            category = input("Enter category: ")
            result = books_in_category(books, category)
            if result:
                print("Books found:", ", ".join(result))
            else:
                print("No books found in this category.")

        elif choice == "2":
            title = input("Enter title or part of title: ")
            result = search_by_title(books, title)
            if result:
                print("Books found:", ", ".join(result))
            else:
                print("No books found matching that title.")

        elif choice == "3":
            search_text = input("Enter book ID or title: ")
            borrower = input("Enter borrower name: ")
            res = borrow_book(books, loans, search_text, borrower)
            if res == "OK":
                print("Book borrowed successfully.")
            elif res == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif res == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif res == "NOT_AVAILABLE":
                print("Book is not available.")

        elif choice == "4":
            book_title = input("Enter book ID or title: ")
            borrower = input("Enter borrower name: ")
            res = return_book(books, loans, book_title, borrower)
            if res == "OK":
                print("Book returned successfully.")
            elif res == "BOOK_NOT_FOUND":
                print("Book not found.")
            elif res == "EMPTY_NAME":
                print("Borrower name cannot be empty.")
            elif res == "NOT_ON_LOAN":
                print("This book is not on loan by that borrower.")

        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()