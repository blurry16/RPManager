import time
import keyboard
import json
from mojang import API
mojang_api = API()


def mcprint(text):
    keyboard.press("T")
    time.sleep(0.001)
    keyboard.release("T")
    time.sleep(0.1)
    keyboard.write(text, delay=0)
    time.sleep(0.5)
    keyboard.press_and_release("enter")


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        li = thefile.readline()
        if not li:
            time.sleep(0.1)
            continue
        yield li


if __name__ == "__main__":
    while True:
        logfile = open(r"C:\Users\Blurry\AppData\Roaming\.minecraft\logs\latest.log", "r")
        logLines = follow(logfile)
        for line in logLines:
            if "[Render thread/INFO]: [CHAT]" in line and "<" in line and ">" in line:

                try:
                    if "#register".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        money = open("money.json", "r+")
                        names = open("names.json", "r+")
                        money_data = json.load(money)
                        names_data = json.load(names)
                        if username not in money_data and username not in names_data:
                            money_data[username] = 500
                            names_data[username] = "Unset"
                            print(f"Added {username} as a valid player")
                            mcprint("Thanks for registering with RoleBOT2!")
                        else:
                            mcprint("You have already registered with RoleBOT2.")
                        money.seek(0)
                        names.seek(0)
                        json.dump(money_data, money, indent=2)
                        json.dump(names_data, names, indent=2)
                    elif "#balance".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        money = open("money.json", "r+")
                        money_data = json.load(money)
                        if username not in money_data:
                            mcprint("You haven't registered yet.")
                        else:
                            mcprint(f"Your balance is {str(money_data[username])} magmas.")
                    elif "#pay".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split("#pay ", 1)[1].split()
                        userToPay = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        if username == userToPay:
                            mcprint("You can't pay yourself : )")
                        else:
                            amount = args[1]
                            money = open("money.json", "r+")
                            money_data = json.load(money)
                            if username not in money_data:
                                mcprint("You haven't registered yet.")
                            else:
                                if userToPay not in money_data:
                                    mcprint(f"{userToPay} hasn't registered yet.")
                                else:
                                    if money_data[username] >= int(amount):
                                        money_data[username] -= int(amount)
                                        money_data[userToPay] += int(amount)
                                        mcprint(f"{username} successfully paid {userToPay} {str(amount)} magmas.")
                                    else:
                                        mcprint("You don't have enough money.")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                    elif "#setname".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split("#setname ", 1)[1].split()
                        newName = args[0]
                        names = open("names.json", "r+")
                        names_data = json.load(names)
                        if username not in names_data:
                            mcprint("You haven't registered yet.")
                        else:
                            names_data[username] = newName
                            names.seek(0)
                            json.dump(names_data, names, indent=2)
                            mcprint(f"Set Roleplay Name to {newName}")

                    elif "#getname".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split("#getname ", 1)[1].split()
                        nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        names = open("names.json", "r+")
                        names_data = json.load(names)
                        if nameToGet not in names_data:
                            mcprint(f"{nameToGet} has not registered yet.")
                        else:
                            if names_data[nameToGet] == "Unset":
                                mcprint(f"{nameToGet} hasn't set their name yet.")
                            else:
                                mcprint(f"{nameToGet}'s Roleplay Name is '{names_data[nameToGet]}'.")

                    elif "#getmoney".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split("#getmoney ", 1)[1].split()
                        nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        money = open("money.json", "r+")
                        money_data = json.load(money)
                        if nameToGet not in money_data:
                            mcprint(f"{nameToGet} hasn't registered yet.")
                        else:
                            mcprint(f"{nameToGet} has {money_data[nameToGet]} magmas.")

                    elif "#addmoney".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username == "blurry16" or username == "ItzMeFred":
                            args = line.replace("\n", "").split("#addmoney ", 1)[1].split()
                            nameToAdd = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = args[1]
                            money = open("money.json", "r+")
                            money_data = json.load(money)
                            if nameToAdd not in money_data:
                                mcprint(f"{nameToAdd} hasn't registered yet.")
                            else:
                                if int(amount) > 0:
                                    money_data[nameToAdd] += int(amount)
                                    mcprint(f"{amount} magmas were successfully added to {nameToAdd}")
                                else:
                                    mcprint(f"Wrong value!")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#removemoney".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username == "blurry16" or username == "ItzMeFred":
                            args = line.replace("\n", "").split("#removemoney ", 1)[1].split()
                            nameToRemove = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = args[1]
                            money = open("money.json", "r+")
                            money_data = json.load(money)
                            if nameToRemove not in money_data:
                                mcprint(f"{nameToRemove} hasn't registered yet.")
                            else:
                                money_data[nameToRemove] -= int(amount)
                                mcprint(
                                    f"{amount} magmas were successfully removed from {nameToRemove}'s wallet.")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#setmoney".lower() in line:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username == "blurry16" or username == "ItzMeFred":
                            args = line.replace("\n", "").split("#setmoney ", 1)[1].split()
                            nameToSet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = args[1]
                            money = open("money.json", "r+")
                            money_data = json.load(money)
                            if nameToSet not in money_data:
                                mcprint(f"{nameToSet} hasn't registered yet.")
                            else:
                                money_data[nameToSet] = int(amount)
                                mcprint(f"{amount} magmas were successfully set for {nameToSet}.")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#github".lower() in line:
                        username = line.split()[4].split("<")[1].split(">")[0]
                        mcprint("github.com/blurry16/")
                except Exception as ex:
                    print(f"Error \"{ex}\" occurred.")
