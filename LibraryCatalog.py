import sys
import argparse

from tools.book import Book
from tools.user import User


class LibraryCatalog:

    def __init__(self):
        self.book = Book()
        self.user = User()

    def add_user(self, name):
        print(self.user.create(name))

    def get_users(self):
        print(self.user.users())

    def remove_user(self, user_id):
        print(self.user.remove(user_id))

    def add_book(self, book_props):
        print(self.book.add(book_props))

    def checkout_book(self, isbn, user_id):
        print(self.book.checkout(isbn, user_id))

    def return_book(self, isbn, user_id):
        print(self.book.return_book(isbn, user_id))

    def remove_book(self, isbn_number):
        print(self.book.remove(isbn_number))


def get_book_props():

    book_info = {'isbn': input("Please enter book ISBN number: "),
                 'title': input("Please enter book title: "),
                 'pages': input("Please enter book pages' count: "),
                 'copies': input("Please enter book copies' count: ")}
    return book_info


def main():



    # Populate command parser
    parser = argparse.ArgumentParser(description="Manage library catalog.", prog="LibraryCatalog")
    command_subparser = parser.add_subparsers(help="Perform book or user commands", dest="command")
    command_subparser.required = True

    user_cmd_parser = command_subparser.add_parser("user")
    # parser.parse_args(["user"])
    book_cmd_parser = command_subparser.add_parser("book")

    # Prepare action parser
    user_action_subparser = user_cmd_parser.add_subparsers(help="User actions", dest="action")
    user_action_subparser.required = True
    book_action_subparser = book_cmd_parser.add_subparsers(help="Book actions", dest="action")
    book_action_subparser.required = True

    user_add = user_action_subparser.add_parser("add")
    user_list = user_action_subparser.add_parser("list")
    user_remove = user_action_subparser.add_parser("remove")

    book_add = book_action_subparser.add_parser("add")
    book_checkout = book_action_subparser.add_parser("checkout")
    book_return = book_action_subparser.add_parser("return")
    book_remove = book_action_subparser.add_parser("remove")

    # Prepare action argument parser
    user_add.add_argument("name", metavar="<name>", type=str, help="The name of the user")
    user_remove.add_argument("id", metavar="<userID>", type=int, help="The ID of the user")
    book_checkout.add_argument("isbn", metavar="<isbn>", type=int, help="The ISBN of the book")
    book_checkout.add_argument("--user", required=True, metavar="<userID>", type=int, help="The ID of the user")
    book_return.add_argument("isbn", metavar="<isbn>", type=int, help="The ISBN of the book")
    book_return.add_argument("--user", required=True, metavar="<userID>", type=int, help="The ID of the user")
    book_remove.add_argument("isbn", metavar="<isbn>", type=int, help="The ISBN of the book")

    args = parser.parse_args()

    library = LibraryCatalog()

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    if "user" == args.command:

        if "add" == args.action:
            library.add_user(args.name)

        if "list" == args.action:
            library.get_users()

        if "remove" == args.action:
            library.remove_user(args.id)

    if "book" == args.command:

        if "add" == args.action:
            library.add_book(get_book_props())

        if "checkout" == args.action:
            library.checkout_book(args.isbn, args.user)

        if "return" == args.action:
            library.return_book(args.isbn, args.user)

        if "remove" == args.action:
            library.remove_book(args.isbn)


if __name__ == "__main__":
    main()
