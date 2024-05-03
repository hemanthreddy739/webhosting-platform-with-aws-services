import boto3
from django.conf import settings
import requests
import jwt


def get_users_fullname_from_user_pool(username):
    # Initialize Cognito client
    client = boto3.client('cognito-idp', region_name = settings.COGNITO_REGION_NAME)

    try:
        # Retrieve user details from user pool
        response = client.admin_get_user(
            UserPoolId = settings.COGNITO_USER_POOL_ID,
            Username = username
        )

        # Extract user name
        for attr in response['UserAttributes']:
            if attr['Name'] == 'name':
                return attr['Value']
        
        # If name attribute not found
        return None

    except client.exceptions.UserNotFoundException:
        # Handle the case where the user is not found
        return None


def getIhsUserDetails(code):
    # Exchange the authorization code for tokens
    token_url = 'https://ihs.auth.ap-south-1.amazoncognito.com/oauth2/token'

    client_id = settings.COGNITO_APP_CLIENT_ID
    redirect_uri = 'http://localhost:8000/hostproject'  # This should match the redirect URI configured in Cognito

    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(token_url, data=token_payload)
    tokens = response.json()

    # Decode the ID token to extract user information
    id_token = tokens.get('id_token')
    
    if id_token:
        decoded_token = jwt.decode(id_token, verify=False)  # You might need to verify the token signature in a production environment
        username = decoded_token.get('cognito:username')
        email = decoded_token.get('email')
    
        user_details = {
            'username': username,
            'email': email
        }

        # Get user's name from user pool using username
        name = get_users_fullname_from_user_pool(username)

        user_details['name'] = name

        return user_details
        
