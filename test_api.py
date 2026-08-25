import requests

# URL de ton serveur Flask (généralement localhost:5000)
BASE_URL = "http://127.0.0.1:5000"

def test_connection():
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend en ligne et opérationnel !")
        else:
            print(f"⚠️ Backend répond, mais avec le code : {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur : Impossible de contacter le backend. Il est peut-être éteint. Détail : {e}")

if __name__ == "__main__":
    test_connection()