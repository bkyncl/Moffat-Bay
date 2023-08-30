from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

#custom backend for handling logins. Uses case insensitive email with the user acount model password to authenticate out custom user account model
class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


#   This authentication method does not handle errors properly. this is the case insensitive version, but it creates an error 
# if authentication does not validate. 
#---work this out later on----
#    def authenticate(self, request, email=None, password=None, **kwargs):
#        UserModel = get_user_model()
#        if email is None:
#            email = kwargs.get(UserModel.EMAIL_FIELD)
#
#        try:
#            case_insensitve_email_field = '{}__iexact'.format(UserModel.EMAIL_FIELD)
#            user = UserModel._default_manager.get(**{case_insensitve_email_field:email})
#        except UserModel.DoesNotExist:
#            UserModel().set_password(password)
#        else: 
#            if user.check_password(password) and self.user_can_authenticate(user):
#                return user