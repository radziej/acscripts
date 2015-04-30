#!/usr/bin/python

import sys, os
from subprocess import Popen, PIPE
import re

# read the website
(stdout, stderr) = Popen(["lynx", "-width 300", "-dump", "http://www.studentenwerk-aachen.de/speiseplaene/vita-t.html"], stdout=PIPE).communicate()
lines = stdout.decode("utf-8").split("\n")

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
        self.price      = ""
    def extract_price(self, line):
        return re.search("[0-9],[0-9][0-9] (\xe2\x82\xac|EUR)".decode("utf-8"), line).group()
    def extract_description(self, line):
        return re.sub(" \^(.(,[a-zA-Z0-9])*|\w+)", "", (line[len(self.category):-len(self.price)] if self.price else line[len(self.category):]).strip())


def main():
    # parse the websites information into each dish
    dishes = [Dish("Tellergericht"), Dish("Vegetarisch"), Dish("Empfehlung des Tages"), Dish("Klassiker"), Dish("Pizza des Tages"), Dish("Pasta"), Dish("Pasta"), Dish("Pasta"), Dish("Wok")]
    i = 0
    for line in lines:
        sline = line.strip()
        if sline.lower().startswith(dishes[i].category.lower()):
            dishes[i].price       = dishes[i].extract_price(sline)
            dishes[i].description = dishes[i].extract_description(sline)
            if i < len(dishes) - 1:
                i += 1
            else:
                break

    # parse the website information for the side dishe
    sides = [Dish("Gemuese/Salat".decode("utf-8")), Dish("Hauptbeilage")]
    i = 0
    for line in lines[::-1]:
        sline = line.strip()
        if sline.lower().startswith(sides[i].category.lower()) or sline.lower().startswith(sides[i].category.replace("ue", "\xc3\xbc".decode("utf-8")).lower()):
            sides[i].description = sides[i].extract_description(sline)
            if i < len(sides) - 1:
                i += 1
            else:
                break

    # print out the information
    print bcolors.BOLD + lines[0], "\n", bcolors.ENDC
    for i in range(len(dishes)):
        if i % 2:
            print bcolors.OKBLUE + dishes[i].category.rjust(21), dishes[i].description.ljust(80), dishes[i].price, bcolors.ENDC
        else:
            print dishes[i].category.rjust(21), dishes[i].description.ljust(80), dishes[i].price
    print
    for side in sides[::-1]:
        print side.category.rjust(21), side.description.ljust(80)
    print

if __name__ == "__main__":
    sys.exit(main())
