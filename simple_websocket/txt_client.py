#!/usr/bin/env python

import asyncio

from websockets.asyncio.client import connect

async def hello():
    uri = "ws://localhost:8765"
    async with connect(uri) as websocket:
        name = input("What's your name?: ")

        await websocket.send(name)
        print(f"\nClient sent: {name}")

        greeting = await websocket.recv()
        print(f"Client received: {greeting}")

        food = input("\nWhat's your favorite food?: ")

        await websocket.send(food)
        print(f"\nClient sent: {food}")

        mesage = await websocket.recv()
        print(f"Client received: {mesage}")

if __name__ == "__main__":
    asyncio.run(hello())