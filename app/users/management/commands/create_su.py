import maskpass
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.validators import validate_email

from users.models import User


class Command(BaseCommand):
    """
    Custom management command for creating a superuser with admin
    privileges.
    """
    help = 'Create a superuser with admin privileges.'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.

        This function guides the user through the process of creating a
        superuser with admin privileges. It prompts for an email
        address, first name, last name, and password. The email address
        is validated using the `validate_email_address` function. If
        the email address is valid and passwords match, a superuser
        is created with the provided information.

        Args:
            *args: Additional command arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            None

        Example:
            To create a superuser with admin privileges, run:
            $ python manage.py create_su
        """
        while True:
            email = input('Enter admin e-mail (required): ')
            if email.lower() == 'exit':
                return
            try:
                validate_email(email)
                break
            except ValidationError:
                self.stderr.write(
                    self.style.ERROR(
                        f'Email "{email}" is not a valid email address. '
                        f'Enter valid Email or type "EXIT" to cancel operation'
                    )
                )

        first_name = input('Enter your first name: ')
        last_name = input('Enter your last name: ')
        password1 = maskpass.askpass(
            prompt='Enter your password (required): ',
            mask=""
        )
        password2 = maskpass.askpass(
            prompt='Repeat your password (required): ',
            mask=""
        )

        if password1 != password2:
            self.stderr.write(
                self.style.ERROR(
                    'Passwords do not match. Superuser creation failed.'
                )
            )
            return

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(password2)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Your superuser {user.email} created\n'
                f'{first_name if first_name else email} '
                f'{last_name if last_name else ""}'
            )
        )
