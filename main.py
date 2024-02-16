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
    with (open("cfg.json", "r") as cfg_file,
          open("money.json", "r", encoding="utf-8") as money,
          open("names.json", "r", encoding="utf-8") as names,
          open("players_jobs.json", "r", encoding="utf-8") as players_jobs,
          open("available_jobs.json", "r", encoding="utf-8") as available_jobs):
        cfg = json.load(cfg_file)["cfg"]
        admins = cfg["admins"]
        region_name = cfg["region-name"]
        money_data = json.load(money)
        names_data = json.load(names)
        players_jobs_data = json.load(players_jobs)
        available_jobs_data = json.load(available_jobs)

    while True:
        logfile = open(cfg["log-file"], "r", encoding="utf-8")
        logLines = follow(logfile)
        for line in logLines:
            if "[CHAT]" in line and "<" in line and ">" in line:
                try:
                    match line.lower().split()[5]:
                        case "#register":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if (username not in money_data
                                    and username not in names_data
                                    and username not in players_jobs_data):
                                money_data[username] = 500.0
                                names_data[username] = ""
                                players_jobs_data[username] = ""
                                print(f"Added {username} as a valid player")
                                mcprint("Thanks for registering with RoleBOT2!")
                            else:
                                mcprint("You have already registered with RoleBOT2.")

                        case "#balance":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]

                            if username not in money_data:
                                mcprint("You haven't registered yet.")
                            else:
                                mcprint(f"Your balance is {str(money_data[username])} magmas.")
                        case "#getmoney":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))

                            if nameToGet not in money_data:
                                mcprint(f"{nameToGet} hasn't registered yet.")
                            else:
                                mcprint(f"{nameToGet} has {money_data[nameToGet]} magmas.")

                        case "#pay":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            userToPay = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            if username == userToPay:
                                mcprint("You can't pay yourself : )")
                            else:
                                amount = float(args[1])

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

                        case "#setname":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            newName = args[0]

                            if username not in names_data:
                                mcprint("You haven't registered yet.")
                            else:
                                names_data[username] = newName
                                mcprint(f"Set Roleplay name to {newName} for {username}.")

                        case "#getname":
                            print(line)

                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                            nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))

                            if nameToGet not in names_data:
                                mcprint(f"{nameToGet} has not registered yet.")
                            else:
                                if names_data[nameToGet] == "":
                                    mcprint(f"{nameToGet} hasn't set their name yet.")
                                else:
                                    mcprint(f"{nameToGet}'s Roleplay name is '{names_data[nameToGet]}'.")
                        case "#resetname":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]

                            if username not in names_data:
                                mcprint("You haven't registered yet.")
                            else:
                                names_data[username] = ""
                                mcprint(f"Successfully reset Roleplay name for {username}.")

                        case "#myname":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username not in names_data:
                                mcprint("You haven't registered yet.")
                            else:
                                if names_data[username] != "":
                                    mcprint(f"Your Roleplay name is '{names_data[username]}'.")
                                else:
                                    mcprint(f"You haven't set your Roleplay name yet.")

                        case "#addmoney":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToAdd = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                                amount = float(args[1])
                                if nameToAdd not in money_data:
                                    mcprint(f"{nameToAdd} hasn't registered yet.")
                                else:
                                    if amount > 0:
                                        money_data[nameToAdd] += amount
                                        mcprint(f"{amount} magmas were successfully added to {nameToAdd}'s wallet.")
                                    else:
                                        mcprint(f"Wrong value!")
                            else:
                                mcprint("No permissions.")
                        case "#removemoney":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToRemove = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                                amount = float(args[1])
                                if nameToRemove not in money_data:
                                    mcprint(f"{nameToRemove} hasn't registered yet.")
                                else:
                                    if amount > 0:
                                        money_data[nameToRemove] -= amount
                                        mcprint(
                                            f"{amount} magmas were successfully removed from {nameToRemove}'s wallet.")
                                    else:
                                        mcprint("Wrong amount! amount <= 0!")
                            else:
                                mcprint("No permissions.")
                        case "#setmoney":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToSet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                                amount = float(args[1])
                                if nameToSet not in money_data:
                                    mcprint(f"{nameToSet} hasn't registered yet.")
                                else:
                                    money_data[nameToSet] = amount
                                    mcprint(f"{amount} magmas were successfully set for {nameToSet}'s wallet.")
                            else:
                                mcprint("No permissions.")
                        case "#resetmoney":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToReset = mojang_api.get_username(mojang_api.get_uuid(args[0]))

                                if nameToReset not in money_data:
                                    mcprint(f"{nameToReset} hasn't registered yet.")
                                else:
                                    money_data[nameToReset] = 500.0
                                    mcprint(f"{nameToReset}'s wallet was successfully reset.")

                            else:
                                mcprint("No permissions.")
                        case "#addmember":
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
                        case "#removemember":
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
                        case "#newjob":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                job_naming = args[0].lower()
                                wage = float(args[1])
                                if job_naming not in available_jobs_data and wage >= 0:
                                    available_jobs_data[job_naming] = wage
                                    print(f"Added new job '{job_naming}' with {wage} magmas wage.")
                                    mcprint(f"Added '{job_naming}' job with {wage} wage.")
                                elif wage < 0:
                                    mcprint("Wrong value. wage < 0")
                                else:
                                    mcprint(f"Job '{job_naming}' already exist.")
                            else:
                                mcprint("No permissions.")
                        case "#setjob":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToSet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                                job_naming = args[1].lower()
                                if job_naming in available_jobs_data:
                                    if nameToSet not in players_jobs_data:
                                        mcprint(f"{nameToSet} hasn't registered yet.")
                                    else:
                                        players_jobs_data[nameToSet] = job_naming
                                        mcprint(f"Job '{job_naming}' set for {nameToSet}")
                                        print(f"Job '{job_naming}' set for {nameToSet}")
                                else:
                                    mcprint("This job doesn't exist.")
                            else:
                                mcprint("No permissions.")
                        case "#resetjob":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                args = line.replace("\n", "").split(f"{command} ", 1)[1].split()
                                nameToReset = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                                if nameToReset not in players_jobs_data:
                                    mcprint(f"{nameToReset} hasn't registered yet.")
                                elif players_jobs_data[nameToReset] == "":
                                    mcprint(f"{nameToReset} doesn't have a job.")
                                else:
                                    players_jobs_data[nameToReset] = ""
                                    mcprint(f"Job reset for {nameToReset}.")
                                    print(f"Job reset for {nameToReset}.")

                            else:
                                mcprint("No permissions.")
                        case "#getjob":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            args = line.replace("\n", "").split(f"{command}", 1)[1].split()
                            nameToGet = mojang_api.get_username(mojang_api.get_uuid(args[0]))
                            if nameToGet not in players_jobs_data:
                                mcprint(f"{nameToGet} hasn't registered yet.")
                            elif players_jobs_data[nameToGet] == "":
                                mcprint(f"{nameToGet} doesn't have a job.")
                            else:
                                mcprint(f"{nameToGet}'s job is '{players_jobs_data[nameToGet]}'.")

                        case "#myjob":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username not in players_jobs_data:
                                mcprint("You haven't registered yet.")
                            elif players_jobs_data[username] == "":
                                mcprint("You don't have job.")
                            else:
                                mcprint(f"Your job is '{players_jobs_data[username]}'.")
                        case "#payall":
                            print(line)
                            command = line.split()[5]
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                for player in players_jobs_data:
                                    player_job = players_jobs_data[player]
                                    if player_job == "":
                                        pass
                                    else:
                                        money_data[player] += available_jobs_data[player_job]
                                        print(f"Salary paid to {player}.")
                                mcprint("Salary was successfully paid to all players.")
                                print("Salary was successfully paid to all players.")
                            else:
                                mcprint("No permissions.")
                        case "#github":
                            print(line)
                            mcprint("github.com/blurry16/ <3")

                        case "#save":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username in admins:
                                with (open("money.json", "w", encoding="utf-8") as money,
                                      open("names.json", "w", encoding="utf-8") as names,
                                      open("players_jobs.json", "w", encoding="utf-8") as players_jobs,
                                      open("available_jobs.json", "w", encoding="utf-8") as available_jobs):
                                    json.dump(money_data, money, indent=4)
                                    print("Saved money_data.")
                                    json.dump(names_data, names, indent=4)
                                    print("Saved names_data.")
                                    json.dump(players_jobs_data, players_jobs, indent=4)
                                    print("Saved players_jobs_data.")
                                    json.dump(available_jobs_data, available_jobs, indent=4)
                                    print("Saved available_jobs_data.")
                                mcprint("Successfully saved data in files.")
                            else:
                                mcprint("No permissions.")
                        case "#stop":
                            print(line)
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username == cfg["host"]:
                                with (open("money.json", "w", encoding="utf-8") as money,
                                      open("names.json", "w", encoding="utf-8") as names,
                                      open("players_jobs.json", "w", encoding="utf-8") as players_jobs,
                                      open("available_jobs.json", "w", encoding="utf-8") as available_jobs):
                                    json.dump(money_data, money, indent=4)
                                    print("Saved money_data.")
                                    json.dump(names_data, names, indent=4)
                                    print("Saved names_data.")
                                    json.dump(players_jobs_data, players_jobs, indent=4)
                                    print("Saved players_jobs_data.")
                                    json.dump(available_jobs_data, available_jobs, indent=4)
                                    print("Saved available_jobs_data.")
                                mcprint("Stopped with code 0.")
                                exit(0)
                            else:
                                print(f"{username} tried to stop the script.")
                except ValueError:
                    mcprint("Wrong value.")
                except errors.NotFound:
                    mcprint("This account doesn't exist.")
                except IndexError:
                    mcprint("Not enough arguments.")
                except Exception as ex:
                    print(f"Error \"{ex}\" occurred.")
