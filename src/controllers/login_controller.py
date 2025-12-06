class LoginController:
    def login(self, username, password):
        if not username and not password:
            return True
        else:
            return False
