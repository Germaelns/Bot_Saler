class DatabaseGetPost:

    def __init__(self, session):
        self.session = session

    def get_user_data(self):
        print(self.session)


if __name__ == "__main__":

    db = DatabaseGetPost("Hello")
    db.get_user_data()

    del db
