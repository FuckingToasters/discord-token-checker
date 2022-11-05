import httpx
import colorama

FILENAME = "tokens.txt"
FORMAT = 2 # 0 = token, 1 = token:password, 2 = mail:pass:token, 3 = token:mail:pass
OUTPUT = 2 # 0 = token, 1 = token:password, 2 = mail:pass:token, 3 = token:mail:pass

colorama.init(autoreset=True)

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
            
        headers = {"Authorization": token}
        checktoken = httpx.get("https://discord.com/api/v9/users/@me", headers=headers)
        
        if checktoken is None: print(f"{colorama.Fore.RED} No Token found inside {FILENAME}"), sys.exit(69)
        
        try:
            if checktoken.json()["message"] == "401: Unauthorized":
                with open("invalid.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
                print(f"{colorama.Fore.RED} [-] Invalid Token: {token}")
                

        except KeyError:
            # print(checktoken.json())
            if checktoken.json()["verified"] is False:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.RED}Unverified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token}")
                with open("unverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")

            elif checktoken.json()["email"] is not None and checktoken.json()["phone"] is not None:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Fully Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token}")
                with open("fullyverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")

            elif checktoken.json()["email"] is not None and checktoken.json()["phone"] is None and checktoken.json()["verified"] is True:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Email Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token}")
                with open("emailverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
            
            elif checktoken.json()["email"] is None and checktoken.json()["phone"] is not None:
                print(f"{colorama.Fore.GREEN} [+] Valid {colorama.Fore.YELLOW}Phone Verified {colorama.Fore.GREEN}Token: {colorama.Fore.CYAN}{token}")
                with open("phoneonlyverified.txt", "a+") as file:
                    if OUTPUT == 0: file.write(f"{token}\n")
                    elif OUTPUT == 1: file.write(f"{token}:{password}\n")
                    elif OUTPUT == 2: file.write(f"{mail}:{password}:{token}:\n")
                    elif OUTPUT == 3: file.write(f"{token}:{mail}:{password}\n")
            
