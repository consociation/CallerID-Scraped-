import requests
from bs4 import BeautifulSoup
import json

def request(url):
    headers = { // request headers
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        //parses html code 
        soup = BeautifulSoup(res.text, 'html.parser')

        phone = {}

        area = soup.find('h6', class_='details_text')
        if area:
            phone['Area Code'] = area.get_text(strip=True)

        details = soup.find_all('div', class_='details_wrapper')

        for d in details:
            title = d.find('div', class_='title')
            text = d.find('div', class_='text')

            if title and text:
                phone[title.get_text(strip=True)] = text.get_text(strip=True)

        location = {}
        loc = soup.find('div', class_='location_body_wrapper')

        if loc:
            loc_details = loc.find_all('div', class_='details_wrapper')

            for l in loc_details:
                title = l.find('div', class_='title')
                text = l.find('div', class_='text')

                if title and text:
                    location[title.get_text(strip=True)] = text.get_text(strip=True)
        //prints the data it parsed
        result = {
            "Phone Info": phone,
            "Location Info": location
        }
        //prints data like a json format
        print(json.dumps(result, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    number = input("Phone number (US): ")
    url = f"https://onlinereverselookup.com/phone-info/?number={number}"
    request(url)
