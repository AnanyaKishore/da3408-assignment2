import time
import requests

URL = "http://localhost:5000/predict"
texts = ["WIN a FREE iPhone now! Click here: bit.ly/xyz123", "Congrats! So happy for you!"]

def call(text):
    t0 = time.perf_counter()
    resp = requests.post(URL, json={"text": text})
    t1 = time.perf_counter()
    return (t1 - t0) * 1000, resp.json()

for text in texts:
    print(f"Calling API with text: {text}")
    for i in range(1, 6):
        ms, resp = call(text)
        print(f"Call {i}:  {ms:.2f} ms -> {resp}")
    print()