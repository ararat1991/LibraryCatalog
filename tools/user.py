import configparser
import os


class User:

    def __init__(self):
        self.user_data = configparser.ConfigParser()
        self.user_config = configparser.ConfigParser()
        self.data_file_path = os.path.abspath("data/user.ini")
        self.config_file_path = os.path.abspath("config/config.ini")

    def create(self, name):

        config = self.user_config
        data = self.user_data

        config.read(self.config_file_path)
        user_config = config['user']

        new_user_id = int(user_config['last_user_id']) + 1
        data[new_user_id] = {'name': name}

        # Add User
        with open(self.data_file_path, 'a') as user_data_file:
            data.write(user_data_file)

        # Update config
        user_config['last_user_id'] = str(new_user_id)
        with open(self.config_file_path, 'w') as user_config_file:
            config.write(user_config_file)
        return '\nUser has been created successfully!'

    def users(self):

        data = self.user_data
        data.read(self.data_file_path)
        sections = reversed(data.sections())
        users = "----USER LIST----\n\nID\tName\n\n"
        for section in sections:
            users += section + "\t" + data.items(section)[0][1] + "\n"
        return users.strip()

    def remove(self, user_id):

        data = self.user_data
        data.read(self.data_file_path)
        if str(user_id) not in data.sections():
            return "\nUser does not exist!"
        # Delete User
        data.remove_section(str(user_id))
        with open(self.data_file_path, 'w') as user_data_file:
            data.write(user_data_file)
        return "\nUser has been removed successfully!"
