# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from typing import Optional
from pathlib import Path

def getPath(file_name:str):
    """Getting the local Path, deactivate decorator for local testing
    Arguments:
        file_name {str} -- my_file.csv
    Returns:
        Path
    """
    from os import getcwd
    return Path(getcwd(),'out',file_name)

def decoratorCopyFileToAnotherLocalDestination(function):
    def wrapper(filein:Path):
        from os import system
        system("""copy {} D:\QlikData\HR_Data\\ /Y""".format(filein))
    return wrapper
#@decoratorCopyFileToAnotherLocalDestination
def copyFileToAnotherLocalDestination(filein:Path)->None:
    """Copy file to Local Path

    Args:
        filein (Path): This is where the file is being save when donwloaded
    """
    from os import system
    system("""copy {} c:\\Users\\lf188653\\Desktop\\ /Y""".format(filein))