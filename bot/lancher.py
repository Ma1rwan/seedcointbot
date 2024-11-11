import nest_asyncio
from pyrogram import Client
from bot.logger import Logger
from bot.tapper import Tapper
import threading
import keyboard
import time
import os
import aiohttp
import asyncio
import json


def launcher():
    nest_asyncio.apply()

    logger = Logger()

    async def get_inventory(query_id):
        """
        Retrieves the user's inventory from the SeedDAO API.

        Parameters:
        query_id (str): The query string containing user identification and authorization data.

        Returns:
        dict: The JSON response from the API, or an error message if the request fails.
        """
        url = "https://alb.seeddao.org/api/v1/worms/me"
        # Convert the dictionary to a JSON string
        params = {"page": 1}
        payload = json.dumps(params)

        # Calculate the byte length of the JSON string
        payload_length = len(payload.encode('utf-8'))
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-length": f"{payload_length}",  # Adjust this value to match your payload length
            "content-type": "application/json",
            "origin": "https://cf.seeddao.org",
            "referer": "https://cf.seeddao.org/",
            "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99", "Microsoft Edge WebView2";v="130"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "telegram-data": query_id,
            # Replace with your specific data
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        }

        async with aiohttp.ClientSession() as session:
            try:
                # Make the GET request to fetch inventory data
                async with session.get(url, headers=headers, data=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        return response_data
                    else:
                        error_message = await response.json()
                        return None
            except aiohttp.ClientError as e:
                return None


    async def buy_worm(market_id, query_id, logger: Logger, worm_type, session_name):
        try:
            url = "https://alb.seeddao.org/api/v1/market-item/buy"
            params = {"market_id": market_id}
            payload = json.dumps(params)

            # Calculate the byte length of the JSON string
            payload_length = len(payload.encode('utf-8'))
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9",
                "content-length": f"{payload_length}",  # Adjust this value to match your payload length
                "content-type": "application/json",
                "origin": "https://cf.seeddao.org",
                "referer": "https://cf.seeddao.org/",
                "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99", "Microsoft Edge WebView2";v="130"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "telegram-data": query_id,
                # Replace with your specific data
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status == 404:
                        return await response.json()
                    response.raise_for_status()
                    logger.success(session_name, f"{worm_type} Worm bought successfully")

                    return await response.json()
        except KeyboardInterrupt:
            raise
        except aiohttp.ClientError as e:
            if "Internal Server Error" not in str(e) and "Bad Request" not in str(e):
                logger.error(session_name, f"Error buying {worm_type} worm.")

            return None

    async def sell_worm(worm_id, price, query_id, logger: Logger, worm_type, session_name):
        try:
            url = "https://alb.seeddao.org/api/v1/market-item/add"
            price = int(price * 1000000000)

            params = {
                "worm_id": worm_id,
                "price": price,
            }
            payload = json.dumps(params)

            # Calculate the byte length of the JSON string
            payload_length = len(payload.encode('utf-8'))

            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9",
                "content-length": f"{payload_length}",  # Adjust this value to match your payload length
                "content-type": "application/json",
                "origin": "https://cf.seeddao.org",
                "referer": "https://cf.seeddao.org/",
                "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99", "Microsoft Edge WebView2";v="130"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "telegram-data": query_id,
                # Replace with your specific data
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    response.raise_for_status()
                    if response.status == 200:
                        logger.success(session_name, f"{worm_type} Worm sold successfully.")

                        return await response.json()
                    else:
                        return None
        except KeyboardInterrupt:
            raise
        except aiohttp.ClientError as e:
            logger.error(session_name, f"Error during selling {worm_type} worm:")

            return None


    async def get_worm_market(query_id: str, worm_type: str, logger: Logger, session_name):
        try:
            url = "https://alb.seeddao.org/api/v1/market/v2"
            params = {
                "market_type": "worm",
                "worm_type": worm_type,
                "sort_by_price": "ASC",
                "page": 1
            }

            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "origin": "https://cf.seeddao.org",
                "telegram-data": query_id,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            }

            async with aiohttp.ClientSession() as session:
                # Pass the params dictionary directly to the `params` argument
                async with session.get(url, headers=headers, params=params) as response:
                    market_data = await response.json()

                    # Handle Bad Request response
                    if response.status == 400 and market_data.get('message') != 'too many requests':
                        logger.info(session_name, f"Bad request (400) for worm type {worm_type}. Skipping this session.")

                        return "skip"

                    # Raise an error if status is not OK
                    response.raise_for_status()

                    # Check if 'data' exists and is not empty
                    if 'data' in market_data and market_data['data']:
                        return market_data
                    else:
                        logger.info(session_name, f"No market data found for worm type {worm_type}. Skipping this session.")

                        return "skip"
        except KeyboardInterrupt:
            raise
        except aiohttp.ClientError as e:
            if 'Bad Request' not in str(e):
                logger.error(session_name, f"Error fetching market data for {worm_type}: {e}")

            return "skip"
        except asyncio.TimeoutError:
            logger.error(session_name, f"Timeout occurred for {worm_type}. Skipping...")

            return "skip"


    async def main():
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        api_id = data.get("API_ID")
        api_hash = data.get("API_HASH")
        path = r"sessions"

        # List all files in the directory
        sessions = [os.path.splitext(f)[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        start_time = time.time()  # Start the timer
        # Define only the first prices
        base_prices = {
            'common': 0.34,
            'uncommon': 0.59,
            'rare': 2.7,
            'epic': 10.2
        }

        # Automatically calculate the 3% discount
        prices = {worm_type: [price, price * 0.97] for worm_type, price in base_prices.items()}

        skip_count = 0
        session_index = 0
        profits = {session: 0 for session in sessions}  # Initialize profits for all sessions
        # Flag for stopping the program
        stop_program = False

        # Change this to async to allow proper asyncio use
        async def listen_for_stop():
            nonlocal stop_program
            while not stop_program:
                if keyboard.is_pressed('ctrl+k'):  # Listen for Ctrl + K
                    print("Ctrl + K detected! Logging profits and stopping...")
                    for session_name, profit in profits.items():

                        logger.info(session_name,  f"Profit for {session_name}: {profit:.2f} SEED")

                    # Print the result in a readable format
                    # Calculate and print elapsed time
                    elapsed_time = time.time() - start_time
                    hours, rem = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    if hours > 0:
                        print(
                            f"The script has run for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
                    elif minutes > 0:
                        print(f"The script has run for {int(minutes)} minutes and {int(seconds)} seconds.")
                    else:
                        print(f"The script has run for {int(seconds)} seconds.")
                    stop_program = True
                    break  # Stop execution after logging profits
                await asyncio.sleep(0.1)  # Non-blocking sleep

        # Start listening for the stop key in a separate thread
        stop_thread = threading.Thread(target=lambda: asyncio.run(listen_for_stop()), daemon=True)
        stop_thread.start()


        try:
            while not stop_program:  # Main loop continues while stop_program is False
                # Check for new sessions
                current_sessions = [os.path.splitext(f)[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                for session_name in current_sessions:
                    if session_name not in profits:
                        profits[session_name] = 0
                    loop = 0
                    if stop_program:
                        break  # If stop_program is set, exit the session loop
                    async with Client(session_name, api_id=api_id,
                                      api_hash=api_hash,
                                      workdir=r'sessions') as tg_client:
                        await tg_client.get_me()
                        tapper = Tapper(tg_client, logger)
                        query_id = await tapper.get_tg_web_data(None)
                        # Handle each worm type for the current session
                        for worm_type in prices:



                            # Fetch worm market data
                            worm_market_data = await get_worm_market(query_id, worm_type, logger, session_name)

                            if worm_market_data == "skip":
                                skip_count += 1
                                if skip_count >= 10:
                                    skip_count = 0
                                    session_index += 1
                                    continue
                            else:
                                items = worm_market_data['data'].get('items', [])
                                base_prices[worm_type] = (items[-1]['price_gross'] / 1000000000) * 0.99
                                prices[worm_type] = [base_prices[worm_type], base_prices[worm_type] * 0.97]
                                # Filter items by price and prepare buy tasks
                                tasks = []
                                for item in items:
                                    if item.get('price_gross', 0) < prices[worm_type][1] * 1000000000:  # Condition to buy worm
                                        tasks.append(buy_worm(item.get('id'), query_id, logger, worm_type, session_name))

                                # If there are tasks to buy worms, execute them asynchronously
                                if tasks:
                                    results = await asyncio.gather(*tasks)
                                    # Process results, sell worms after buying them
                                    for result in results:
                                        if result and 'data' in result:
                                            worm_id = result['data'].get('worm_id')
                                            worm_type = result['data'].get('worm_type')
                                            worm_price = result['data']['price_gross'] / 1000000000
                                            # Sell the worm after purchase
                                            sold = await sell_worm(worm_id, prices[worm_type][0], query_id, logger, worm_type, session_name)
                                            if sold:
                                                profits[session_name] += (prices[worm_type][0] - worm_price - (prices[worm_type][0] * 0.03))
                                else:
                                    logger.info(session_name, f"No worms meet price condition for {worm_type}.")

                    loop += 1
                    if loop == 20:
                        loop = 0
                        for session_name_2 in sessions:
                            async with Client(session_name_2, api_id=api_id,
                                              api_hash=api_hash,
                                              workdir=r'sessions') as tg_client:
                                tapper = Tapper(tg_client, logger)
                                query_id = await tapper.get_tg_web_data(None)
                                max_tries = 10
                                while True:
                                    inventory = await get_inventory(query_id)
                                    if not inventory:
                                        max_tries -= 1
                                    else:
                                        items = inventory['data']['items']
                                        if len(items) == 0:
                                            break
                                        sold_count = 0
                                        for item in items:
                                            if not item['on_market']:
                                                sold = await sell_worm(item.get('id'), prices[item.get('type')][0],
                                                                       query_id, logger, prices[item.get('type')], session_name)
                                                if sold:
                                                    profits[session_name_2] += (prices[item.get('type')][0] -
                                                                                prices[item.get('type')][1] - (
                                                                prices[item.get('type')][0] * 0.03))
                                                sold_count += 1

                                        if sold_count == 0 and inventory['data']['page'] == 1:
                                            break
                                    if max_tries < 1:
                                        break


                # Allow some processing time before checking the stop flag again
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            print("Program interrupted. Logging profits...")
            for session_name, profit in profits.items():
                logger.info(session_name, f"Profit for {session_name}: {profit:.2f} SEED")
    print("To stop the program and get profit hit: ctrl + k")
    asyncio.run(main())
