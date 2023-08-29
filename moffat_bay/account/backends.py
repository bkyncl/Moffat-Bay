from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)

        try:
            case_insensitve_email_field = '{}__iexact'.format(UserModel.EMAIL_FIELD)
            user = UserModel._default_manager.get(**{case_insensitve_email_field:email})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else: 
            if user.check_password(password) and self.user_can_authenticate(user):
                return user