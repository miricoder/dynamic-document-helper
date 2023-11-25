import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    try:
        # Add headers to the request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Send a GET request to the specified URL with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text content from the page
            text_content = soup.get_text()

            return text_content
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    # Prompt the user to input a website URL
    website_url = input("Enter the URL of the website: ")

    # Call the scrape_website function with the provided URL
    scraped_data = scrape_website(website_url)

    # Print the scraped data
    print("\nScraped Data:")
    print(scraped_data)


if __name__ == "__main__":
    main()
