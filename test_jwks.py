import requests

base_url = 'http://localhost:8080'  # Replace with your server's base URL

def get_public_keys():
    response = requests.get(f'{base_url}/jwks')
    if response.status_code == 200:
        jwks = response.json()
        return jwks['keys']
    else:
        print(f"Failed to fetch JWKS. Status code: {response.status_code}")
        return None

def test_public_keys():
    public_keys = get_public_keys()
    if public_keys:
        for key in public_keys:
            print("Key ID:", key['kid'])
            print("Public Key:", key['n'])
    else:
        print("No public keys found.")

if __name__ == "__main__":
    test_public_keys()
