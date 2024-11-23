import os
import aiohttp
import asyncio
from colorama import Fore, Style
from datetime import datetime

black = Fore.LIGHTBLACK_EX
green = Fore.LIGHTGREEN_EX
blue = Fore.LIGHTBLUE_EX
red = Fore.LIGHTRED_EX
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.LIGHTYELLOW_EX
reset = Style.RESET_ALL

# Variabel global untuk total poin semua akun
total_points_all_accounts = 0
total_points_lock = asyncio.Lock()  # Lock untuk memastikan akses aman ke variabel global

class TeneoXD:
    def __init__(self, account_label):
        self.wss_url = "wss://secure.ws.teneo.pro/websocket"
        self.account_label = account_label

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    async def connect(self, userid):
        max_retry = 10
        retry = 1
        self.ses = aiohttp.ClientSession()
        while True:
            try:
                if retry >= max_retry:
                    self.log(f"{yellow}{self.account_label} - max retrying reached, try again later")
                    return
                async with self.ses.ws_connect(
                    url=f"{self.wss_url}?userId={userid}&version=v0.2"
                ) as wss:
                    retry = 1
                    self.log(f"{green}{self.account_label} - Connected to {white}websocket {green}server")
                    while True:
                        msg = await wss.receive_json(timeout=10)
                        point_today = msg.get("pointsToday")
                        point_total = msg.get("pointsTotal")

                        # Update total poin dari semua akun
                        async with total_points_lock:
                            global total_points_all_accounts
                            total_points_all_accounts += point_total
                            self.log(
                                f"{green}{self.account_label} - Point today: {white}{point_today} {magenta}| {green}Point total: {white}{point_total}"
                            )
                            self.log(
                                f"{blue}Total points across all accounts: {white}{total_points_all_accounts}"
                            )

                        # Send PING setiap 10 detik sebanyak 90 kali
                        for i in range(90):
                            await wss.send_json({"type": "PING"})
                            self.log(f"{white}{self.account_label} - Sent {green}PING {white}to server!")
                            await countdown(10)
            except KeyboardInterrupt:
                await self.ses.close()
                break
            except Exception as e:
                self.log(f"{red}{self.account_label} - Error: {white}{e}")
                retry += 1
                continue

async def countdown(t):
    for i in range(t, 0, -1):
        minute, seconds = divmod(i, 60)
        hour, minute = divmod(minute, 60)
        seconds = str(seconds).zfill(2)
        minute = str(minute).zfill(2)
        hour = str(hour).zfill(2)
        print(f"waiting for {hour}:{minute}:{seconds} ", flush=True, end="\r")
        await asyncio.sleep(1)

async def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(
        f"""
    {magenta}╔═╗╔╦╗╔═╗  {green}╔═╗┬─┐┌─┐ ┬┌─┐┌─┐┌┬┐
    {magenta}╚═╗ ║║╚═╗  {green}╠═╝├┬┘│ │ │├┤ │   │ 
    {magenta}╚═╝═╩╝╚═╝  {green}╩  ┴└─└─┘└┘└─┘└─┘ ┴ 
    
    {green}Github: {white}github.com/AkasakaID
          """
    )

    if not os.path.exists("userid.txt"):
        print(f"{red}error: {white}userid.txt file is not found, run setup.py first!")
        exit()

    with open("userid.txt", "r") as file:
        user_ids = [line.strip() for line in file if line.strip()]

    if not user_ids:
        print(f"{red}error: {white}No user IDs found in userid.txt")
        exit()

    tasks = []
    for idx, userid in enumerate(user_ids):
        account_label = f"Account {idx + 1}"
        teneo_instance = TeneoXD(account_label=account_label)
        tasks.append(asyncio.create_task(teneo_instance.connect(userid=userid)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        if os.name == "nt":
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop=loop)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
