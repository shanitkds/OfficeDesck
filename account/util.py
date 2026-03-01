from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ResetTokenGenerator(PasswordResetTokenGenerator):
    pass

reset_token = ResetTokenGenerator()