import json


def load_library(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_library(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def find_book(books, search_text):
    search = search_text.strip().lower()

    for book_id, info in books.items():
        if book_id.lower() == search:
            return book_id

    for book_id, info in books.items():
        if info["title"].lower() == search:
            return book_id

    for book_id, info in books.items():
        if info["author"].lower() == search:
            return book_id

    return None


def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, info in books.items():
        status = "AVAILABLE" if info["available"] else "ON LOAN"
        print(f"{book_id} | {info['title']} | {info['category']} | {status}")


def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan["book_id"]
        borrower = loan["borrower"]
        if book_id in books:
            title = books[book_id]["title"]
            print(f"{book_id} | {title} | Borrower: {borrower}")
        else:
            print(f"{book_id} | Unknown | Borrower: {borrower}")


def library_statistics(books):
    total = len(books)
    available = sum(1 for b in books.values() if b["available"])
    borrowed = total - available
    return (total, available, borrowed)


def main():
    data = load_library("library.json")
    lib_info = data["library"]
    categories = data["categories"]
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {lib_info['name']}")
    print(f"Branch: {lib_info['branch']}")
    print(f"Year: {lib_info['year']}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()
    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)
    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()