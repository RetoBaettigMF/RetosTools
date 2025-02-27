import requests
import time

BASE_URL = "http://localhost:4321/api"

def measure_latency_get():
    
    start_time = time.time()
    for (i, _) in enumerate(range(100)):
        response =  requests.get(f"{BASE_URL}/hello")
    
    end_time = time.time()
    latency = (end_time - start_time)/100
    print(f"GET /hello: Status Code: {response.status_code}, Latency: {latency:.4f} seconds, Response: {response.json()}")

if __name__ == "__main__":
    measure_latency_get()
