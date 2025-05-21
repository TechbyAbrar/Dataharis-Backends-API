import requests
def validate_facebook_token(access_token):
    try:
        url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        response = requests.get(url)
        data = response.json()
        print("Facebook response:", data)  # Ensure this is being printed
        if "error" in data:
            return None
        return data
    except Exception as e:
        print("Facebook token validation failed:", str(e))
        return None
    

def validate_google_token(id_token):
    try:
        response = requests.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={id_token}"
        )
        data = response.json()
        print("Google response:", data)
        if "error_description" in data or "email" not in data:
            return None
        return data
    except Exception as e:
        print("Google token validation failed:", str(e))
        return None
