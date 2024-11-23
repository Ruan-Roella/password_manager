from colorama import Fore, Back, Style
from typing import TypeAlias, Literal
from getpass import getpass

ForegroundColor: TypeAlias = Literal['black', 'blue', 'cyan', 'green', 'lightblack_ex', 'lightblue_ex', 'lightcyan_ex', 'lightgreen_ex', 'lightmagenta_ex', 'lightred_ex', 'lightwhite_ex', 'lightyellow_ex', 'magenta', 'red', 'white', 'yellow']
BackgroundColor: TypeAlias = Literal['black', 'blue', 'cyan', 'green', 'lightblack_ex', 'lightblue_ex', 'lightcyan_ex', 'lightgreen_ex', 'lightmagenta_ex', 'lightred_ex', 'lightwhite_ex', 'lightyellow_ex', 'magenta', 'red', 'white', 'yellow']
FontWeight: TypeAlias = Literal['normal', 'bright', 'dim']


class Console:
    "Customize the echo console"
    
    @classmethod
    def Write(cls, *values: object, fg: ForegroundColor = None, bg: BackgroundColor = None, weight: FontWeight = 'normal'):
        extra = []
        
        if fg: extra.append(getattr(Fore, fg.upper()))
        if bg: extra.append(getattr(Back, bg.upper()))
        if weight: extra.append(getattr(Style, weight.upper()))

        echo = print(*extra, *values, Style.RESET_ALL, sep=str().strip())
        return echo

    @classmethod
    def ReadLine(cls, prompt: object = "", password: bool = False):
        if password:
            return getpass(prompt)
        return input(prompt)