import requests
import xml.etree.ElementTree as ET

def get_news(limit=5):
    try:
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            headlines = []
            count = 0
            for item in root.findall('.//item/title'):
                headlines.append(item.text)
                count += 1
                if count >= limit:
                    break
            return headlines
    except Exception as e:
        print(f"News error: {e}")
    return []

if __name__ == "__main__":
    n = get_news()
    print(n)
