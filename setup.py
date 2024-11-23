import aiohttp


async def login(email, password):
    login_url = (
        "https://ikknngrgxuxgjhplbpey.supabase.co/auth/v1/token?grant_type=password"
    )
    login_data = {
        "email": email,
        "password": password,
        "gotrue_meta_security": {},
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlra25uZ3JneHV4Z2pocGxicGV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzgxNTAsImV4cCI6MjA0MTAxNDE1MH0.DRAvf8nH1ojnJBc3rD_Nw6t1AV8X_g6gmY_HByG2Mag",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlra25uZ3JneHV4Z2pocGxicGV5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0MzgxNTAsImV4cCI6MjA0MTAxNDE1MH0.DRAvf8nH1ojnJBc3rD_Nw6t1AV8X_g6gmY_HByG2Mag",
        "content-type": "application/json;charset=UTF-8",
        "origin": "chrome-extension://emcclcoaglgcpoognfiggmhnhgabppkm",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "x-client-info": "supabase-js-web/2.45.4",
        "x-supabase-api-version": "2024-01-01",
    }
    async with aiohttp.ClientSession() as client:
        result = await client.post(login_url, json=login_data, headers=headers)
        if result.status != 200:
            print(f"[x] Login failed for {email}, please try again later!")
            return None
        res = await result.json()
        userid = res.get("user", {}).get("id")
        if userid:
            print(f"[+] Login success for {email}!")
            return userid
        else:
            print(f"[x] User ID not found for {email}!")
            return None


async def main():
    while True:
        try:
            # Input email sebagai banyak akun, dipisahkan dengan spasi
            email_input = input("Input emails (separate with space): ").strip()
            if not email_input:
                print("[!] Email cannot be empty.")
                continue

            # Memecah email menjadi list
            email_list = email_input.split()

            # Input password sekali
            password = input("Input password for all accounts: ").strip()
            if not password:
                print("[!] Password cannot be empty.")
                continue

            user_ids = []
            for email in email_list:
                user_id = await login(email, password)
                if user_id:
                    user_ids.append(user_id)

            if user_ids:
                with open("userid.txt", "a") as f:
                    for user_id in user_ids:
                        f.write(user_id + "\n")
                print(f"[+] {len(user_ids)} User IDs saved to userid.txt.")
            else:
                print("[x] Login failed for all accounts, no user IDs saved.")

            next_action = input("Do you want to add another set of emails? (y/n): ").strip().lower()
            if next_action != "y":
                break
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user.")
            break
        except Exception as e:
            print(f"[x] An error occurred: {e}")
            break


try:
    import asyncio

    asyncio.run(main())
except KeyboardInterrupt:
    print("\n[!] Program stopped by user.")