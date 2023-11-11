### Installation

1. clone https://github.com/iko4akov/secrets.git
2. Rename '.env.example' to '.env' and fill in the required fields.
3. run command `docker compose up`


# Secret Manager
This Django application provides a simple secret management system with time-limited secrets. Each secret has a specified lifespan and can only be viewed once.

### Models Secret
#### owner: 
`ForeignKey to the user who owns the secret.`
#### name_secret: 
`CharField with a maximum length of 20, representing the name of the secret.`
#### secret: 
`TextField, holding the content of the secret.`
#### life_days: 
`IntegerField, indicating the number of days the secret will be valid.`
#### is_reader: 
`BooleanField, defaulting to False, used to track whether the secret has been viewed.`
#### word_code: 
`CharField with a maximum length of 50, representing a code word associated with the secret.`
#### secret_key: 
`CharField with a maximum length of 100, representing a unique URL for the secret.`
#### date_of_burning: 
`DateTimeField, indicating the date and time when the secret will expire (nullable).`
#### date_created: 
`DateTimeField, automatically set to the creation date and time.`

### SecretSerializer
`A serializer for the Secret model, allowing easy conversion between JSON representations and Secret instances. It includes a custom create method to handle secret creation, associating it with the current user, generating a unique secret key, and setting the expiration date based on the specified lifespan.`

### Service Functions
### format_date_time
`def format_date_time(day: int or str) -> str:
    """
    Takes an integer or string 'day' as an offset and
    returns a formatted string representing a future date and
    time based on the current date and time.
    Parameters:
        - day (int or str): The number of days to add to
        the current date. Can be an integer or a string.
    Returns:
    - str: A string representing the formatted future date and
    time in the format 'YYYY-MM-DD HH:MM'.
    """
    # ...implementation details...` <p>
This function takes an offset (in days) and returns a formatted string representing a future date and time.

### Celery Task
#### burning_secret
<p> A Celery task that deletes secrets with a 'date_of_burning' earlier than the current date and time. This task queries the 'Secret' model for secrets with a 'date_of_burning' earlier than the current date and deletes them.

`from datetime import datetime
from celery import shared_task
from secret.models import Secret

@shared_task
def burning_secret():
    """
    Celery task that deletes secrets with a 'date_of_burning'
    earlier than the current date and time.
    This task queries the 'Secret' model for secrets with a
    'date_of_burning' earlier than the current date
    and deletes them.
    """
    # ...implementation details...` <p>

### API Views
#### SecretListView
`A view that returns a list of secrets owned by the authenticated user.`

#### SecretGenerateView
`A view that allows the authenticated user to create a new secret. The generated secret_key`

### SecretRetrieveView
`A view that retrieves details of a specific secret owned by the authenticated user.`

### SecretDestroyView
`A view that allows the authenticated user to delete a specific secret owned by them.`

### ReadSecretRetrieveView
`A view that retrieves the content of a secret using its secret_key. The secret is marked as read and deleted after retrieval.` <p>

Note: Ensure that you have appropriate authentication and authorization mechanisms in place to secure these views.




