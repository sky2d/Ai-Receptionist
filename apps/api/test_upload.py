import requests
import traceback

try:
    with open("test.txt", "w") as f:
        f.write("Hello world, this is a test document.")
        
    url = "http://127.0.0.1:8000/api/v1/knowledge/upload"
    with open("test.txt", "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        res = requests.post(url, files=files)
        
    print("Status code:", res.status_code)
    print("Response text:", res.text)
except Exception as e:
    traceback.print_exc()
