import configparser
import os
import datetime


class Book:

    def __init__(self):
        self.book_data_parser = configparser.ConfigParser()
        self.user_data_parser = configparser.ConfigParser()
        self.history_data_parser = configparser.ConfigParser()
        self.reserve_data_parser = configparser.ConfigParser()
        self.config_parser = configparser.ConfigParser()
        self.book_data_file_path = os.path.abspath("data/book.ini")
        self.user_data_file_path = os.path.abspath("data/user.ini")
        self.config_file_path = os.path.abspath("config/config.ini")
        self.checkout_history_file_path = os.path.abspath("data/checkout_history.ini")
        self.reserve_history_file_path = os.path.abspath("data/reserve_history.ini")

    def add(self, book_props):
        data = self.book_data_parser
        data[book_props.get('isbn')] = {'title': book_props.get('title'), 'pages': book_props.get('pages'),
                                        'copies': book_props.get('copies'),
                                        'available_copies': book_props.get('copies')}
        # Add Book
        with open(self.book_data_file_path, 'a') as book_data_file:
            data.write(book_data_file)
        return "\nThe book has been created successfully!"

    def checkout(self, book_isbn, user_id):

        history_data = self.history_data_parser

        book_data = self.book_data_parser
        book_data.read(self.book_data_file_path)
        if str(book_isbn) not in book_data.sections():
            return "\n Incorrect book ISBN: " + str(book_isbn)

        user_data = self.user_data_parser
        user_data.read(self.user_data_file_path)
        if str(user_id) not in user_data.sections():
            return "\n Incorrect user ID: " + str(user_id)

        action_file = self.checkout_history_file_path
        action_time = "checkout_time"
        msg = "The book with ISBN: " + str(book_isbn) + " has been checkout successfully!"

        # Put on reserve
        book = book_data[str(book_isbn)]
        book_avaliable_copies = book['available_copies']
        if 1 > int(book_avaliable_copies):
            action_file = self.reserve_history_file_path
            action_time = "reserve_time"
            msg = "The book with ISBN: " + str(book_isbn) + " has been reserved as there were no available copies!"
        else:
            # Reduce book available count
            book = book_data[str(book_isbn)]
            book['available_copies'] = str(int(book_avaliable_copies) - 1)
            with open(self.book_data_file_path, 'w') as book_data_file:
                book_data.write(book_data_file)

        # Get last history ID for auto increment
        config = self.config_parser
        config.read(self.config_file_path)
        history_config = config['history']
        new_checkout_id = int(history_config['last_history_id']) + 1
        # Prepare history data
        history_data[new_checkout_id] = {'book_isbn': book_isbn, 'user_id': user_id,
                                action_time: datetime.datetime.now()}

        # Add checkout to library history
        with open(action_file, 'a') as history_data_file:
            history_data.write(history_data_file)

        # Update config
        history_config['last_history_id'] = str(new_checkout_id)
        with open(self.config_file_path, 'w') as user_config_file:
            config.write(user_config_file)
        return "\n" + msg

    def return_book(self, book_isbn, user_id):
        history_data = self.history_data_parser
        history_data.read(self.checkout_history_file_path)

        book_data = self.book_data_parser
        book_data.read(self.book_data_file_path)
        if str(book_isbn) not in book_data.sections():
            return "\n Incorrect book ISBN: " + str(book_isbn)

        user_data = self.user_data_parser
        user_data.read(self.user_data_file_path)
        if str(user_id) not in user_data.sections():
            return "\n Incorrect user ID: " + str(user_id)

        for section in history_data.sections():
            history = history_data[str(section)]
            if str(book_isbn) == history['book_isbn'] and str(user_id) == history['user_id']:
                history_data.remove_section(section)
                with open(self.checkout_history_file_path, 'w') as history_data_file:
                    history_data.write(history_data_file)

                # Increase book available count
                book = book_data[str(book_isbn)]
                book['available_copies'] = str(int(book['available_copies']) + 1)
                with open(self.book_data_file_path, 'w') as book_data_file:
                    book_data.write(book_data_file)
                return "\nThe book has been returned successfully!"

    def remove(self, isbn):

        data = self.book_data_parser
        data.read(self.book_data_file_path)
        if str(isbn) not in data.sections():
            return "\nBook does not exist!"
        data.remove_section(isbn)
        with open(self.book_data_file_path, 'w') as book_data_file:
            data.write(book_data_file)
        return "\nThe book has been removed successfully!"
