import time
import keyboard
import json
from mojang import API, errors
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
    cfg = json.load(open("cfg.json"))["cfg"]
    admins = cfg["admins"]
    region_name = cfg["region-name"]
    while True:
        # logfile = open(r"C:\Users\Blurry\AppData\Roaming\.minecraft\logs\latest.log", "r")
        logfile = open(cfg["log-file"], "r")
        logLines = follow(logfile)
        for line in logLines:
            if "[CHAT]" in line and "<" in line and ">" in line:
                try:
                    if "#register" == line.lower().split()[5]:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        money = open("money.json", "r")
                        names = open("names.json", "r")
                        jobs = open("players_jobs.json", "r")
                        money_data = json.load(money)
                        names_data = json.load(names)
                        jobs_data = json.load(jobs)
                        if username not in money_data and username not in names_data and username not in jobs_data:
                            money_data[username] = 500.0
                            names_data[username] = ""
                            jobs_data[username] = ""
                            print(f"Added {username} as a valid player")
                            mcprint("Thanks for registering with RoleBOT2!")
                        else:
                            mcprint("You have already registered with RoleBOT2.")
                        money = open("money.json", "w")
                        names = open("names.json", "w")
                        jobs = open("players_jobs.json", "w")
                        money.seek(0)
                        names.seek(0)
                        jobs.seek(0)
                        json.dump(money_data, money, indent=2)
                        json.dump(names_data, names, indent=2)
                        json.dump(jobs_data, jobs, indent=2)
                    elif "#balance" == line.lower().split()[5]:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        money = open("money.json", "r")
                        money_data = json.load(money)
                        if username not in money_data:
                            mcprint("You haven't registered yet.")
                        else:
                            mcprint(f"Your balance is {str(money_data[username])} magmas.")
                        money.seek(0)

                    elif "#getmoney" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                        nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        money = open("money.json", "r")
                        money_data = json.load(money)
                        if nameToGet not in money_data:
                            mcprint(f"{nameToGet} hasn't registered yet.")
                        else:
                            mcprint(f"{nameToGet} has {money_data[nameToGet]} magmas.")
                        money.seek(0)

                    elif "#pay" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                        userToPay = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        if username == userToPay:
                            mcprint("You can't pay yourself : )")
                        else:
                            amount = float(args[1])
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            if username not in money_data:
                                mcprint("You haven't registered yet.")
                            else:
                                if userToPay not in money_data:
                                    mcprint(f"{userToPay} hasn't registered yet.")
                                else:
                                    if money_data[username] >= amount >= 1:
                                        money_data[username] -= amount
                                        money_data[userToPay] += amount
                                        mcprint(f"{username} successfully paid {userToPay} {str(amount)} magmas.")
                                    elif amount < 1:
                                        mcprint("Wrong amount. amount < 1!")
                                    else:
                                        mcprint("You don't have enough money.")
                            money = open("money.json", "w")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                    elif "#setname" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                        newName = args[0]
                        names = open("names.json", "r")
                        names_data = json.load(names)
                        if username not in names_data:
                            mcprint("You haven't registered yet.")
                        else:
                            names_data[username] = newName
                            mcprint(f"Set Roleplay name to {newName} for {username}.")
                        names = open("names.json", "w")
                        names.seek(0)
                        json.dump(names_data, names, indent=2)

                    elif "#getname" == line.lower().split()[5]:
                        print(line)

                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                        nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        names = open("names.json", "r")
                        names_data = json.load(names)
                        if nameToGet not in names_data:
                            mcprint(f"{nameToGet} has not registered yet.")
                        else:
                            if names_data[nameToGet] == "":
                                mcprint(f"{nameToGet} hasn't set their name yet.")
                            else:
                                mcprint(f"{nameToGet}'s Roleplay name is '{names_data[nameToGet]}'.")
                        names.seek(0)
                    elif "#resetname" == line.lower().split()[5]:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        names = open("names.json", "r")
                        names_data = json.load(names)
                        if username not in names_data:
                            mcprint("You haven't registered yet.")
                        else:
                            names_data[username] = ""
                            mcprint(f"Successfully reset Roleplay name for {username}.")
                        names = open("names.json", "w")
                        names.seek(0)
                        json.dump(names_data, names, indent=2)

                    elif "#myname" == line.lower().split()[5]:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        names = open("names.json", "r")
                        names_data = json.load(names)
                        if username not in names_data:
                            mcprint("You haven't registered yet.")
                        else:
                            if names_data[username] != "":
                                mcprint(f"Your Roleplay name is '{names_data[username]}'.")
                            else:
                                mcprint(f"You haven't set your Roleplay name yet.")
                        names.seek(0)

                    elif "#addmoney" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToAdd = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = float(args[1])
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            if nameToAdd not in money_data:
                                mcprint(f"{nameToAdd} hasn't registered yet.")
                            else:
                                if amount > 0:
                                    money_data[nameToAdd] += amount
                                    mcprint(f"{amount} magmas were successfully added to {nameToAdd}'s wallet.")
                                else:
                                    mcprint(f"Wrong value!")
                            money = open("money.json", "w")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#removemoney" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToRemove = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = float(args[1])
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            if nameToRemove not in money_data:
                                mcprint(f"{nameToRemove} hasn't registered yet.")
                            else:
                                if amount > 0:
                                    money_data[nameToRemove] -= amount
                                    mcprint(f"{amount} magmas were successfully removed from {nameToRemove}'s wallet.")
                                else:
                                    mcprint("Wrong amount! amount <= 0!")
                            money = open("money.json", "w")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#setmoney" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToSet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            amount = float(args[1])
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            if nameToSet not in money_data:
                                mcprint(f"{nameToSet} hasn't registered yet.")
                            else:
                                money_data[nameToSet] = amount
                                mcprint(f"{amount} magmas were successfully set for {nameToSet}'s wallet.")
                            money = open("money.json", "w")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#resetmoney" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToReset = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            if nameToReset not in money_data:
                                mcprint(f"{nameToReset} hasn't registered yet.")
                            else:
                                money_data[nameToReset] = 500.0
                                mcprint(f"{nameToReset}'s wallet was successfully reset.")
                            money = open("money.json", "w")
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#addmember" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToAdd = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            mcprint(f"/rg addmember {region_name} {nameToAdd}")
                            mcprint(f"Successfully added {nameToAdd}.")
                        else:
                            mcprint("No permissions.")
                    elif "#removemember" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToRemove = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            if nameToRemove in admins:
                                mcprint("You can't remove other admins.")
                            elif nameToRemove == username:
                                mcprint("You can't remove yourself.")
                            else:
                                mcprint(f"/rg removemember {region_name} {nameToRemove}")
                                mcprint(f"Successfully removed {nameToRemove}.")
                        else:
                            mcprint("No permissions.")
                    elif "#addjob" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            job_naming = args[0].lower()
                            wage = float(args[1])
                            available_jobs = open("available_jobs.json", "r")
                            available_jobs_data = json.load(available_jobs)
                            if job_naming not in available_jobs_data and wage >= 0:
                                available_jobs_data[job_naming] = wage
                                print(f"Added new job '{job_naming}' with {wage} magmas wage.")
                                mcprint(f"Added '{job_naming}' job with {wage} wage.")
                            elif wage < 0:
                                mcprint("Wrong value. wage < 0")
                            else:
                                mcprint(f"Job '{job_naming}' already exist.")
                            available_jobs = open("available_jobs.json", "w")
                            available_jobs.seek(0)
                            json.dump(available_jobs_data, available_jobs, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#setjob" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToSet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            job_naming = args[1].lower()
                            available_jobs = open("available_jobs.json", "r")
                            available_jobs_data = json.load(available_jobs)
                            players_jobs = open("players_jobs.json", "r")
                            players_jobs_data = json.load(players_jobs)
                            if job_naming in available_jobs_data:
                                if nameToSet not in players_jobs_data:
                                    mcprint(f"{nameToSet} hasn't registered yet.")
                                else:
                                    players_jobs_data[nameToSet] = job_naming
                                    mcprint(f"Job '{job_naming}' set for {nameToSet}")
                                    print(f"Job '{job_naming}' set for {nameToSet}")
                            else:
                                mcprint("This job doesn't exist.")

                            players_jobs = open("players_jobs.json", "w")
                            available_jobs.seek(0)
                            players_jobs.seek(0)
                            json.dump(players_jobs_data, players_jobs, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#resetjob" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToReset = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            players_jobs = open("players_jobs.json", "r")
                            players_jobs_data = json.load(players_jobs)
                            if nameToReset not in players_jobs_data:
                                mcprint(f"{nameToReset} hasn't registered yet.")
                            elif players_jobs_data[nameToReset] == "":
                                mcprint(f"{nameToReset} doesn't have a job.")
                            else:
                                players_jobs_data[nameToReset] = ""
                                mcprint(f"Job reset for {nameToReset}.")
                                print(f"Job reset for {nameToReset}.")
                            players_jobs.seek(0)
                            players_jobs = open("players_jobs.json", "w")
                            json.dump(players_jobs_data, players_jobs, indent=2)
                        else:
                            mcprint("No permissions.")
                    elif "#getjob" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        args = line.replace("\n", "").split(f"{command}", 1)[1].split()
                        nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                        players_jobs = open("players_jobs.json", "r")
                        players_jobs_data = json.load(players_jobs)
                        if nameToGet not in players_jobs_data:
                            mcprint(f"{nameToGet} hasn't registered yet.")
                        elif players_jobs_data[nameToGet] == "":
                            mcprint(f"{nameToGet} doesn't have a job.")
                        else:
                            mcprint(f"{nameToGet}'s job is '{players_jobs_data[nameToGet]}'.")
                        players_jobs.seek(0)

                    elif "#myjob" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        players_jobs = open("players_jobs.json", "r")
                        players_jobs_data = json.load(players_jobs)
                        if username not in players_jobs_data:
                            mcprint("You haven't registered yet.")
                        elif players_jobs_data[username] == "":
                            mcprint("You don't have job.")
                        else:
                            mcprint(f"Your job is '{players_jobs_data[username]}'.")
                        players_jobs.seek(0)
                    elif "#payall" == line.lower().split()[5]:
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username in admins:
                            available_jobs = open("available_jobs.json", "r")
                            available_jobs_data = json.load(available_jobs)
                            players_jobs = open("players_jobs.json", "r")
                            players_jobs_data = json.load(players_jobs)
                            money = open("money.json", "r")
                            money_data = json.load(money)
                            for player in players_jobs_data:
                                player_job = players_jobs_data[player]
                                if player_job == "":
                                    pass
                                else:
                                    money_data[player] += available_jobs_data[player_job]
                                    print(f"Salary paid to {player}.")
                            money = open("money.json", "w")
                            available_jobs.seek(0)
                            players_jobs.seek(0)
                            money.seek(0)
                            json.dump(money_data, money, indent=2)
                            mcprint("Salary was successfully paid to all players.")
                            print("Salary was successfully paid to all players.")
                        else:
                            mcprint("No permissions.")
                    elif "#github" == line.lower().split()[5]:
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        mcprint("github.com/blurry16/ <3")
                except ValueError:
                    mcprint("Wrong value.")
                except errors.NotFound:
                    mcprint("This account doesn't exist.")
                except IndexError:
                    mcprint("Not enough arguments.")
                except Exception as ex:
                    print(f"Error \"{ex}\" occurred.")
