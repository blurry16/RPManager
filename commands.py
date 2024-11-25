import json
import time
from pathlib import Path
from typing import TextIO, Generator

import keyboard
import mojang.errors
from mojang import API


def mcprint(text):
    keyboard.press_and_release("t")
    time.sleep(0.1)
    keyboard.write(text, delay=0)
    time.sleep(0.01)
    keyboard.press_and_release("enter")


def follow(file: TextIO) -> Generator[str, None, None]:
    file.seek(0, 2)
    while True:
        li = file.readline()
        if not li:
            time.sleep(0.1)
            continue
        yield li


getusername = lambda line: line.split()[4].split("<")[1][:-1]
rpgetargs = lambda line: line.split("<" + getusername(line) + ">")[1].split()


class Json:
    def __init__(self, path: Path | str):
        self.path = path

    def load(self) -> list | dict:
        with open(self.path, "r", encoding="UTF-8") as file:
            return json.load(file)

    def dump(self, data: list | dict) -> None:
        with open(self.path, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=2)


mojang_api = API()

CONFIG_PATH = Path("config.json")
configfile = Json(CONFIG_PATH)
config = configfile.load()
paths = config["paths"]
admins = config["admins"]
region_name = config["region-name"]

datafile = Json(paths["data"])
uuidsfile = Json(paths["uuids"])
availablejobsfile = Json(paths["available_jobs"])


def getuuid(username: str) -> str:
    uuids = uuidsfile.load()
    if username.lower() not in uuids:
        uuids[username.lower()] = mojang_api.get_uuid(username)
        uuidsfile.dump(uuids)
    return uuids[username.lower()]


def registercommand(line: str):
    """#register"""
    print(line)
    username = getusername(line)
    uuid = getuuid(username)
    data = datafile.load()
    if uuid not in data:
        data[uuid] = {
            "username": username,
            "balance": 500.0,
            "in-bot-name": None,
            "job": None
        }
        datafile.dump(data)
        print(f"Added {username} as a valid player")
        mcprint(f"Thanks for registering, {username}!")
    else:
        mcprint("You have already registered with RoleBOT2.")


def unregistercommand(line: str):
    """admin only: #unregister <username>"""
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions!")

    args = rpgetargs(line)
    uuid = getuuid(args[1])
    data = datafile.load()
    if uuid not in data:
        return mcprint(f"{args[1]} is not registered.")
    del data[uuid]
    datafile.dump(data)
    mcprint(f"Successfully unregistered {args[1]}.")
    print(f"Unregistered {args[1]}")


def balancecommand(line: str):
    """#balance - | <username>"""
    print(line)
    username = getusername(line)
    args = rpgetargs(line)

    uuid = getuuid(args[1] if len(args) > 1 else username)
    data = datafile.load()

    if uuid not in data:
        return mcprint("You haven't registered yet." if len(args) <= 1 else f"{args[1]} is not registered.")

    mcprint(("Your" if len(args) <= 1 else args[1] + "'s") + f" balance is {data[uuid]['balance']}.")


def paycommand(line: str):
    """#pay <username> <amount>"""
    print(line)
    username = getusername(line)
    args = rpgetargs(line)
    authoruuid = getuuid(username)
    topayuuid = getuuid(args[1])
    data = datafile.load()
    if authoruuid == topayuuid:
        mcprint("You can't pay yourself : )")
        return
    amount = float(args[2])

    if authoruuid not in data:
        mcprint("You haven't registered yet.")
        return

    if topayuuid not in data:
        mcprint(f"{args[1]} hasn't registered yet.")
        return

    if data[authoruuid]["balance"] >= amount >= 1:
        data[authoruuid]["balance"] -= amount
        data[topayuuid]["balance"] += amount

        datafile.dump(data)
        mcprint(f"{username} successfully paid {data[topayuuid]['username']} {str(amount)}.")
    elif amount < 1:
        mcprint("Wrong amount. amount < 1!")
    else:
        mcprint("You don't have enough money.")


def setnamecommand(line: str):
    """#setname <argument>"""
    print(line)
    username = getusername(line)
    uuid = getuuid(username)
    newname = rpgetargs(line)[1]
    data = datafile.load()
    if uuid not in data:
        return mcprint("You haven't registered yet.")

    data[uuid]["in-bot-name"] = newname
    datafile.dump(data)
    mcprint(f"Set Roleplay name to {newname} for {username}.")


def getnamecommand(line: str):
    """#getname <username>"""
    print(line)

    args = rpgetargs(line)
    name = getusername(line) if len(args) <= 1 else args[1]
    toget = getuuid(name)

    data = datafile.load()

    if toget not in data:
        return mcprint(f"{args[1]} has" if len(args) > 1 else "You have" + f" not registered yet.")
    if data[toget]["in-bot-name"] is None:
        return mcprint(f"{name} hasn't set their name yet." if len(args) > 1 else "You haven't set your name yet.")

    mcprint((f"{name}'s" if len(args) > 1 else "Your") + f" roleplay name is '{data[toget]['in-bot-name']}'.")


def resetnamecommand(line: str):
    """#resetname"""
    print(line)
    username = getusername(line)
    uuid = getuuid(username)
    data = datafile.load()
    if uuid not in data:
        return mcprint("You haven't registered yet.")
    data[uuid]["in-bot-name"] = None
    datafile.dump(data)
    mcprint(f"Successfully reset Roleplay name for {username}.")


def addmoneycommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    toaddname = args[1]
    toadd = getuuid(toaddname)
    amount = float(args[2])
    data = datafile.load()
    if toadd not in data:
        return mcprint(f"{toadd} hasn't registered yet.")

    if amount <= 0:
        return mcprint(f"Wrong value!")
    data[toadd]["balance"] += amount
    datafile.dump(data)
    mcprint(f"{amount} were successfully added to {toaddname}'s wallet.")


def removemoneycommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")

    args = rpgetargs(line)
    toremovename = args[1]
    toremove = getuuid(toremovename)
    amount = float(args[2])
    data = datafile.load()
    if toremove not in data:
        return mcprint(f"{toremovename} hasn't registered yet.")

    if amount <= 0:
        return mcprint("Wrong amount! amount <= 0!")
    data[toremove]["balance"] -= amount
    datafile.dump(data)
    mcprint(f"{amount} were successfully removed from {toremovename}'s wallet.")


def setmoneycommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    tosetname = args[1]
    toset = getuuid(tosetname)
    amount = float(args[2])
    data = datafile.load()
    if toset not in data:
        return mcprint(f"{tosetname} hasn't registered yet.")

    data[toset]["balance"] = amount
    datafile.dump(data)
    mcprint(f"{amount} were successfully set for {tosetname}'s wallet.")


def resetmoneycommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    nametoreset = args[1]
    toreset = getuuid(nametoreset)
    data = datafile.load()
    if toreset not in data:
        return mcprint(f"{nametoreset} hasn't registered yet.")
    data[toreset]["balance"] = 500.0
    datafile.dump(data)
    mcprint(f"{nametoreset}'s wallet was successfully reset.")


def manageplot(line: str, add: bool):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    argument = args[1]
    if add:
        mcprint(f"/rg addmember {region_name} {argument}")
        mcprint(f"Successfully added {argument}.")
    else:
        mcprint(f"/rg removemember {region_name} {argument}")
        mcprint(f"Successfully added {argument}.")


def newjobcommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    job_naming = args[1].lower()
    wage = float(args[2])
    available_jobs_data = availablejobsfile.load()
    if job_naming not in available_jobs_data and wage >= 0:
        available_jobs_data[job_naming] = wage
        availablejobsfile.dump(available_jobs_data)
        print(f"Added new job '{job_naming}' with {wage} wage.")
        mcprint(f"Added '{job_naming}' job with {wage} wage.")
    elif wage < 0:
        mcprint("Wrong value. wage < 0")
    else:
        mcprint(f"Job '{job_naming}' already exist.")


def deletejobcommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    job_naming = args[1].lower()
    available_jobs_data = availablejobsfile.load()
    if job_naming not in available_jobs_data:
        return mcprint(f"Job '{job_naming}' does not exist.")
    del availablejobsfile[job_naming]
    availablejobsfile.dump(available_jobs_data)
    data = datafile.load()
    for uuid in data:
        if data[uuid]["job"] == job_naming:
            data[uuid]["job"] = None
    datafile.dump(data)


def setjobcommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    args = rpgetargs(line)
    tosetname = args[1]
    toset = getuuid(tosetname)
    job_naming = args[2].lower()
    available_jobs_data = availablejobsfile.load()
    data = datafile.load()
    if job_naming not in available_jobs_data:
        return mcprint("This job doesn't exist.")

    if toset not in data:
        return mcprint(f"{tosetname} hasn't registered yet.")
    data[toset]["job"] = job_naming
    datafile.dump(data)
    mcprint(f"Job '{job_naming}' set for {tosetname}")
    print(f"Job '{job_naming}' set for {tosetname}")


def resetjobcommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")

    args = rpgetargs(line)
    toresetname = args[1]
    toreset = getuuid(toresetname)
    data = datafile.load()
    if toreset not in data:
        return mcprint(f"{toresetname} hasn't registered yet.")
    if data[toreset]["job"] is None:
        return mcprint(f"{toresetname} doesn't have a job.")

    data[toreset]["job"] = None
    datafile.dump(data)
    mcprint(f"Job reset for {toresetname}.")
    print(f"Job reset for {toresetname}.")


def getjobcommand(line: str):
    print(line)
    args = rpgetargs(line)
    togetname = getusername(line) if len(args) <= 1 else args[1]
    toget = getuuid(togetname)
    data = datafile.load()
    if toget not in data:
        return mcprint(f"{togetname} hasn't registered yet." if len(args) > 1 else "You haven't registered yet.")
    if data[toget]["job"] is None:
        return mcprint(f"{togetname} doesn't have a job." if len(args) > 1 else "You don't have a job.")
    mcprint(f"{togetname}'s job is '{data[toget]['job']}'." if len(args) > 1 else f"Your job is '{data[toget]['job']}'")


def payallcommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")
    data = datafile.load()
    available_jobs_data = availablejobsfile.load()
    for uuid in data:
        player_job = data[uuid]["job"]
        if player_job is not None:
            data[uuid]["balance"] += available_jobs_data[player_job]
            print(f"Salary paid to {data[uuid]['username']}.")
    datafile.dump(data)
    mcprint("Salary was successfully paid to all players.")
    print("Salary was successfully paid to all players.")


def paywagecommand(line: str):
    print(line)
    username = getusername(line)
    if username not in admins:
        return mcprint("No permissions.")

    args = rpgetargs(line)
    data = datafile.load()
    available_jobs_data = availablejobsfile.load()
    paid = []
    for i in args[1:]:
        try:
            uuid = getuuid(i)
            if data[uuid]["job"] is not None:
                data[uuid]["balance"] += available_jobs_data[data[uuid]["job"]]
                paid.append(data[uuid]["username"])
                print("Paid wage to " + data[uuid]["username"] + ".")
            else:
                print("Player doesn't have job -> " + i)
        except mojang.errors.NotFound:
            print("Player doesn't exist -> " + i)
        except KeyError:
            print("Player hasn't registered -> " + i)
    datafile.dump(data)
    print("Wage was paid to " + ", ".join(paid) + ".")
    mcprint("Wage was paid to passed players.")
