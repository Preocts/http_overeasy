"""Use GET method to pull plain-text from a website."""
import json

from http_overeasy.http_client import HTTPClient

WEBSITE = "https://gist.githubusercontent.com/Preocts/5a56e35d417520136b49b431888c9a03/raw/847cb2c13a2027b37a4ceeb35597ee37f55f3cf9/example.txt"  # noqa: E501


def main() -> int:
    """Get some text from a website."""
    # Create a HTTP client.
    client = HTTPClient()

    # Get the text from the website.
    response = client.get(WEBSITE)

    # Print the response text and other information.
    print(response.text)
    print("---")
    print("Status code:", response.status_code)
    print("Response headers:", json.dumps(response.headers, indent=4))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
