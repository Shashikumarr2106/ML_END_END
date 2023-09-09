from setuptools import find_packages,setup

from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    ##file opening requirements.txt
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    ## if -e . present in requrirement.text ,then remove it
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    
    return requirement_list

#it is used to trigger the __init__py
setup(
    name="sensor",
    version="0.0.2",
    author="shashikumar",
    author_email="shashikumarr2106@gmail.com",
    packages = find_packages(),   ##point to the all __init__.py file
    install_requires=get_requirements(),
)


