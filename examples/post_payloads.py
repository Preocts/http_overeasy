"""Use POST method to push various payloads to a website."""
import json

from http_overeasy.http_client import HTTPClient

# Get a webhook url from this website: https://webhook.site/
# It's a free service that allows you to send messages to a webhook and get a response.
# Paste the webhook url here (not the url in the browser bar):
WEBHOOK_URL = ""


def send_json_payload() -> None:
    """Send a JSON payload to a webhook."""
    headers = {"Content-Type": "application/json"}

    # Create a HTTP client.
    client = HTTPClient(headers=headers)

    # NOTE: Headers defined in the client are used for all requests
    # unless overridden by providing a headers argument for the request.

    # Create a JSON payload.
    payload = {
        "text": "Hello, world!",
        "username": "Egg",
        "icon_emoji": ":robot_face:",
        "attachments": [
            {
                "text": "This is an attachment.",
                "color": "#36a64f",
            },
        ],
    }

    # Send the payload to the webhook.
    response = client.post(WEBHOOK_URL, json=payload)

    # Print the response text and other information.
    print(response.text)
    print("---")
    print("Status code:", response.status_code)
    print("Response headers:", json.dumps(response.headers, indent=4))


def send_urlencoded_payload() -> None:
    """Send a URL-encoded payload to a webhook."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Create a HTTP client.
    client = HTTPClient(headers=headers)

    # NOTE: Headers defined in the client are used for all requests
    # unless overridden by providing a headers argument for the request.

    # Create a URL-encoded payload.
    payload = {
        "text": "Hello, world!",
        "username": "Egg",
        "icon_emoji": ":robot_face:",
        "attachments": [
            {
                "text": "This is an attachment.",
                "color": "#36a64f",
            },
        ],
    }

    # Send the payload to the webhook.
    response = client.post(WEBHOOK_URL, json=payload)

    # Print the response text and other information.
    print(response.text)
    print("---")
    print("Status code:", response.status_code)
    print("Response headers:", json.dumps(response.headers, indent=4))


if __name__ == "__main__":
    print("Sending JSON payload...")
    send_json_payload()
    print("Sending URL-encoded payload...")
    send_urlencoded_payload()
    print("Done.")
    raise SystemExit(0)
