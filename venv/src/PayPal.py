import requests
import json

# paypal_client

class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://sandbox.paypal.com"

    def get_access_token(self):
        auth_url = f"{self.base_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        data = {"grant_type": "client_credentials"}

        response = requests.post(auth_url, data=data, headers=headers, auth=(self.client_id, self.client_secret))

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            return access_token
        else:
            raise Exception("Failed to obtain access token")

    def authorize_paypal_account(self, access_token, email):
        identity_url = f"{self.base_url}/v1/identity/openidconnect/userinfo/?schema=openid"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(identity_url, headers=headers)

        if response.status_code == 200:
            user_info = response.json()
            if user_info.get("email") == email:
                return True # Email matches.
            else:
                return False
        else:
            raise Exception("Failed to fetch user info from PayPal Identity API")

    def get_paypal_balance(self, access_token):
        balance_url = f"{self.base_url}/v2/wallet/balance"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.get(balance_url, headers=headers)

        if response.status_code == 200:
            balance_data = response.json()
            return balance_data
        else:
            raise Exception("Failed to fetch PayPal account balance")
