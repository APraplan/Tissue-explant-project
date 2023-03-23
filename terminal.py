from colorama import *

init(autoreset=True)
print(Fore.RED + 'some red text')
print('automatically back to default color again')
print(Fore.GREEN + 'WIN !')

# Python 3
print(Fore.BLUE + 'blue text on stderr' + Back.RED)