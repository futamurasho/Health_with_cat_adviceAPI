import httpx
url = "http://127.0.0.1:8000/"


response = httpx.post(url, json={}, timeout=120.0)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
