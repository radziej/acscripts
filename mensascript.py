#!/usr/bin/python

import sys, os
from subprocess import Popen, PIPE
import re

# read the website
(stdout, stderr) = Popen(["lynx", "-width 300", "-dump", "http://www.studentenwerk-aachen.de/speiseplaene/vita-t.html"], stdout=PIPE).communicate()
lines = stdout.split("\n")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# setup dishes as a class
class Dish():
    def __init__(self, category):
        self.category   = category
        self.description= ""
        self.price      = "0,00"
    def extract_price(self, line):
        return re.search("[0-9],[0-9][0-9]", line).group()
    def extract_description(self, line):
        return re.sub(" \^(.(,[a-zA-Z0-9])*|\w+)", "", line.replace(" EUR", "")[len(self.category):-len(self.price)]).strip()


# parse the websites information into each dish
dishes = [Dish("Tellergericht"), Dish("Vegetarisch"), Dish("Empfehlung des Tages"), Dish("Klassiker"), Dish("Pizza des Tages"), Dish("Pasta"), Dish("Wok")]
for dish in dishes:
    for line in lines:
        sline = line.strip()
        if sline.lower().startswith(dish.category.lower()):
            dish.price = dish.extract_price(sline)
            dish.description = dish.extract_description(sline)
            break

# parse the website information for the side dishe
sides = [Dish("Gemuese/Salat"), Dish("Hauptbeilage")]
for side in sides:
    for line in lines[::-1]:
        sline = line.strip()
        if sline.lower().startswith(side.category.lower()):
            side.description = side.extract_description(sline)
            break

# print out the information
print bcolors.BOLD + lines[0], "\n", bcolors.ENDC
for i in range(len(dishes)):
    if i % 2:
        print bcolors.OKBLUE + dishes[i].category.rjust(20), dishes[i].description.ljust(170), dishes[i].price, "Euro", bcolors.ENDC
    else:
        print dishes[i].category.rjust(20), dishes[i].description.ljust(170), dishes[i].price, "Euro"
print
for side in sides[::-1]:
    print side.category.rjust(20), side.description.ljust(170)
print
