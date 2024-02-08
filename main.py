import tls_client
import colorama
import time

FILENAME = "tokens.txt"
FORMAT = 0 # 0 = token, 1 = token:password, 2 = mail:pass:token, 3 = token:mail:pass
OUTPUT = 0 # 0 = token, 1 = token:password, 2 = mail:pass:token, 3 = token:mail:pass

colorama.init(autoreset=True)

session = tls_client.Session(
    client_identifier=f"chrome_119",
    random_tls_extension_order=True
)

session.get("https://discord.com")

with open(FILENAME, "r") as token_file: 
    token_file.seek(0)
    checktoken = None
    token, mail, password = None, None, None
    lines = token_file.readlines()
    for token in lines:
        token = token.strip()
        
        if ":" in token:
                
            if FORMAT == 1:
                token = token.split(":")
                token, password = token[0], token[1]
            
            elif FORMAT == 2:
                token = token.split(":")
                mail, password, token = token[0], token[1], token[2]
            
            elif FORMAT == 3:
                token = token.split(":")
                token, mail, password  = token[0], token[1], token[2]
            
        headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        checktoken = session.get("https://discord.com/api/v9/users/@me", headers=headers)
        if checktoken is None: print(f"{colorama.Fore.RED} No Token found inside {FILENAME}"), sys.exit(69)

        response = session.get(url="https://discord.com/api/v9/users/@me/guilds", headers=headers)
        
        delay = 0
        guild_count = "" # Default in case it couldn't be retrieved

        if "message" in response.text:
            if "rate limited" in response.json()["message"]:
                delay = response.json()["retry_after"]

            elif "verify your account" in response.json()["message"]:
                # Unverified Text is printed later on
                #print(f"{colorama.Fore.YELLOW} [-] {token} | You need to verify your account in order to perform this action.")
                pass

        try:
            id_list = [entry["id"] for entry in response.json()]
            guild_count = len(id_list)

        except TypeError:
            pass
        
        time.sleep(delay)

        if "message" in checktoken.json():
            if checktoken.json()["message"] == "401: Unauthorized":
                with open("invalid.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
                print(f"{colorama.Fore.RED} [-] Invalid Token: {token}")

        else:
            # print(checktoken.json())
            if checktoken.json()["verified"] is False:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.RED}Unverified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token} Guild Count: {colorama.Fore.MAGENTA}{guild_count}")
                with open("unverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")

            elif checktoken.json()["email"] is not None and checktoken.json()["phone"] is not None:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Fully Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token} Guild Count: {colorama.Fore.MAGENTA}{guild_count}")
                with open("fullyverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")

            elif checktoken.json()["email"] is not None and checktoken.json()["phone"] is None and checktoken.json()["verified"] is True:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Email Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token} Guild Count: {colorama.Fore.MAGENTA}{guild_count}")
                with open("emailverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
            
            elif checktoken.json()["email"] is None and checktoken.json()["phone"] is not None:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Phone Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token} Guild Count: {colorama.Fore.MAGENTA}{guild_count}")
                with open("phoneonlyverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
