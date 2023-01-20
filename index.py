from datetime import datetime, timedelta
import json
from PIL import Image
from random import randint
import requests


apiKey = 'DEMO_KEY'


def randomDate(daysAgo: int):
    currentDate = datetime.now()
    randomDate = currentDate - timedelta(days=randint(1, daysAgo))
    formattedDate = randomDate.strftime("%Y-%m-%d")
    return formattedDate


url = 'https://api.nasa.gov/planetary/apod'
numberOfImagesToRetrieve = 5
opacity = 0.3

finalImage = Image.new("RGB", (1000, 1000), (255, 255, 255))

for i in range(numberOfImagesToRetrieve):
    date = randomDate(3652)
    params = {
        'api_key': apiKey,
        'date': date
    }

    try:
        response = requests.get(url, params)
        print(f"🌌 Retrieving Astronomy Photo of the Day from: {date}")
    except requests.exceptions.HTTPError as error:
        print(f'HTTP error occurred: {error}')
    except requests.exceptions.ConnectionError as error:
        print(f'Connection error occurred: {error}')
    except requests.exceptions.Timeout as error:
        print(f'Timeout error occurred: {error}')
    except requests.exceptions.RequestException as error:
        print(f'Something went wrong: {error}')

    data = response.json()
    imageUrl = data['url']
    image = Image.open(requests.get(imageUrl, stream=True).raw)
    image = image.resize((1000, 1000))

    finalImage = Image.blend(finalImage, image, opacity)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
finalImage.save(f"{timestamp}.jpg")
