# UUIDs.json stuff is stolen directly from a private fork of mcdatacollector xd
# nobody cares though, I'm the author of that fork.
# anyways im so dumb so i rewrote whole this thing lol. but! it should be stable rn :3

from sys import argv

from mojang import errors

from commands import *

logo = r""" ___ .-.       .-..    ___ .-. .-.     .---.   ___ .-.     .---.    .--.     .--.    ___ .-.    
(   )   \     /    \  (   )   '   \   / .-, \ (   )   \   / .-, \  /    \   /    \  (   )   \   
 | ' .-. ;   ' .-,  ;  |  .-.  .-. ; (__) ; |  |  .-. .  (__) ; | ;  ,-. ' |  .-. ;  | ' .-. ;  
 |  / (___)  | |  . |  | |  | |  | |   .'`  |  | |  | |    .'`  | | |  | | |  | | |  |  / (___) 
 | |         | |  | |  | |  | |  | |  / .'| |  | |  | |   / .'| | | |  | | |  |/  |  | |        
 | |         | |  | |  | |  | |  | | | /  | |  | |  | |  | /  | | | |  | | |  ' _.'  | |        
 | |         | |  ' |  | |  | |  | | ; |  ; |  | |  | |  ; |  ; | | '  | | |  .'.-.  | |        
 | |         | `-'  '  | |  | |  | | ' `-'  |  | |  | |  ' `-'  | '  `-' | '  `-' /  | |        
(___)        | \__.'  (___)(___)(___)`.__.'_. (___)(___) `.__.'_.  `.__. |  `.__.'  (___)       
             | |                                                   ( `-' ;                      
            (___)                                                   `.__.  
Welcome back!
"""

if __name__ == "__main__":
    print(logo)

    argv = [i.lower() for i in argv]

    while True:
        logfile = open(paths["log"], "r", encoding="utf-8")
        logLines = follow(logfile)
        for line in logLines:
            if "[CHAT]" in line and "<" in line and ">" in line and len(rpgetargs(line.strip())) > 0:
                line = line.strip()
                try:
                    match rpgetargs(line)[0].lower():
                        case "#register":
                            registercommand(line)
                        case "#unregister":
                            unregistercommand(line)
                        case "#balance":
                            balancecommand(line)
                        case "#pay":
                            paycommand(line)
                        case "#setname":
                            setnamecommand(line)
                        case "#getname":
                            getnamecommand(line)
                        case "#resetname":
                            resetnamecommand(line)
                        case "#addmoney":
                            addmoneycommand(line)
                        case "#removemoney":
                            removemoneycommand(line)
                        case "#setmoney":
                            setmoneycommand(line)
                        case "#resetmoney":
                            resetmoneycommand(line)
                        case "#newjob":
                            newjobcommand(line)
                        case "#setjob":
                            setjobcommand(line)
                        case "#resetjob":
                            resetjobcommand(line)
                        case "#getjob":
                            getjobcommand(line)
                        case "#payall":
                            payallcommand(line)
                        case "#paywage":
                            paywagecommand(line)
                        case "#addmember":
                            if region_name != "" and region_name is not None:
                                manageplot(line, True)
                        case "#removemember":
                            if region_name != "" and region_name is not None:
                                manageplot(line, False)
                        case "#github":
                            print(line)
                            mcprint("https://github.com/blurry16/RPManager")
                except ValueError:
                    mcprint("Wrong value.")
                except errors.NotFound:
                    mcprint("This account doesn't exist.")
                except errors.TooManyRequests:
                    mcprint("Too many requests to Mojang. Please, try again later.")
                    print(f"too many requests {time.time()}")
                except IndexError:
                    mcprint("Not enough arguments.")
                except Exception as e:
                    print(f"Error \"{e}\" occurred.")
                    if "--debug" in argv:
                        print("[RPManager]: debugging!")
                        raise
