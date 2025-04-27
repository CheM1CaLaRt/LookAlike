import requests

url = "https://starmatch-ai.p.rapidapi.com/fetch_celebrities"

# Prepare headers
headers = {
    "x-rapidapi-key": "9f01634ab6msh8678df376b20c2ap1876edjsn997e60a027b9",  # Replace with the key from environment or a secure location
    "x-rapidapi-host": "starmatch-ai.p.rapidapi.com",
    "Content-Type": "application/x-www-form-urlencoded"
}

# If the API expects a file, you can add a file parameter like so:
files = {'file': open('path_to_your_file', 'rb')}  # Replace 'path_to_your_file' with the actual file path

try:
    response = requests.post(url, headers=headers, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}, {response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
finally:
    files['file'].close()  # Ensure the file is closed after the request
