import json
import websockets
import asyncio

async def receive_loop(websocket):
    async for message in websocket:
        print(f"Received: {message}")

async def main():
    uri = "ws://localhost:8000"
    
    async with websockets.connect(uri) as websocket:
        send_task = asyncio.create_task(send_loop(websocket))
        receive_task = asyncio.create_task(receive_loop(websocket))
        
        # Run both tasks concurrently
        await asyncio.gather(send_task, receive_task)

async def send_loop(websocket):
    while True:
        message = input('Enter Message: ')
        if message.lower() == 'exit':
            break
        await websocket.send(message)

if __name__ == "__main__":
    asyncio.run(main())
