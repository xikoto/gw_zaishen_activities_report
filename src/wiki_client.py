import requests


url = "https://wiki.guildwars.com/wiki/Daily_activities"

print("Intentando acceder a:", url)

response = requests.get(
    url,
    timeout=30,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    },
)

print("STATUS:", response.status_code)
print("URL:", response.url)
print("CONTENT TYPE:", response.headers.get("Content-Type"))
print()
print("HEADERS:")
print(response.headers)
print()
print("PRIMEROS 2000 CARACTERES:")
print(response.text[:2000])