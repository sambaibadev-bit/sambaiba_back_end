from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login with email + password; response includes basic user fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop(self.username_field, None)
        self.fields.pop("password")
        self.fields["email"] = serializers.EmailField(write_only=True)
        # Novo PasswordField: reutilizar o instanciado no pai quebra o bind ao reordenar.
        self.fields["password"] = PasswordField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        return token

    def validate(self, attrs):
        email = (attrs.pop("email", "") or "").strip()
        qs = User.objects.filter(email__iexact=email)
        if qs.count() != 1:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        attrs[self.username_field] = getattr(qs.get(), self.username_field)
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["role"] = self.user.role
        return data
