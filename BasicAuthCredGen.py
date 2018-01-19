import argparse
from argparse import RawTextHelpFormatter
import os
import base64

#Header on the help page
parser = argparse.ArgumentParser(description="----------Program-Help-Page----------", formatter_class=RawTextHelpFormatter)

#Inline Arguments
parser.add_argument("-su", help="Specify a single username for generation. \n")
parser.add_argument("-uf", help="Specify a file containing a list of usernames for generation.  \n")
parser.add_argument("-sp", help="Specify a single password for generation. \n")
parser.add_argument("-pf", help="Specify a file containing a list of usernames for generation.  \n")
parser.add_argument("-o", help="Specify an output file. \n")
parser.add_argument("-s", help="Suppress Terminal Output. \n", action="store_true")
#Allocates the method to call the arguments to 'args'
args = parser.parse_args()

Output = True
Suppress = False

#Checks validity of arguments
if args.su  == None and args.uf == None:
    print("Please Provide Valid Username(s).")
    exit()
if args.sp  == None and args.pf == None:
    print("Please Provide Valid Password(s).")
    exit()
if args.o == None:
    Output = False
    print("No Output File Has Been Provided.  Output Will Only Display Within Terminal.")
if args.s == True:
    Suppress = True
    print("Terminal Output Has Been Suppressed.")

#Obtains the usernames for processing
def ObtainUsername():
    Username = []
    if args.su:
        Username.append(str(args.su))
    if args.uf:
        if os.path.isfile(str(args.uf))==False:
            print("Invalid User File Specified.")
            exit()
        with open(str(args.uf), "r") as Userfile:
            for line in Userfile:
                Username.append(line.strip("\n"))
    return Username

#Obtains the passwords for processing
def ObtainPasswords():
    Password = []
    if args.sp:
        Password.append(str(args.sp))
    if args.pf:
        if os.path.isfile(str(args.pf))==False:
            print("Invalid Password File Specified.")
            exit()
        with open(str(args.pf), "r") as Userfile:
            for line in Userfile:
                Password.append(line.strip("\n"))
    return Password

#Generates the BasicAuth format
def B64CredGenerator(Username, Password, Output, Suppress):
    if Output == True:
        WriteFile = open(args.o, "a")
    for x in Username:
        for y in Password:
            ComboString = str(x+":"+y)
            Encoded = str((base64.b64encode(bytes(ComboString, "utf-8"))))[2:-1]
            if Output == True:
                WriteFile.write(Encoded+"\n")
            if Suppress == False:
                print(Encoded)

B64CredGenerator(ObtainUsername(), ObtainPasswords(), Output, Suppress)
print("-----Generation-Completed.-----")