import requests
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://lake-plankton.streamlit.app/")

def main():
    print(f"Pinging Streamlit app: {STREAMLIT_URL}")

    try:
        # Simple GET request to wake up the app
        response = requests.get(STREAMLIT_URL, timeout=30)
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            print("✅ Successfully pinged the app! It should be awake now.")
        else:
            print(f"⚠️  Received status code {response.status_code}, but request completed.")

        print("Wake script completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        print("Note: The app might still wake up even if we get an error here.")
        # Don't exit with error code - the ping might have still worked
        print("Exiting successfully anyway.")

if __name__ == "__main__":
    main()
