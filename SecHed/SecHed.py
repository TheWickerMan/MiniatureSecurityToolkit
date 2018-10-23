import requests
import argparse
from argparse import RawTextHelpFormatter
import json
import re
import csv

#Header on the help page
parser = argparse.ArgumentParser(description="----------Program-Help-Page----------", formatter_class=RawTextHelpFormatter)

#Inline Arguments
parser.add_argument("-t", help="Provide a list of domains to check. \n")
#Allocates the method to call the arguments to 'args'
args = parser.parse_args()

if not args.t or args.t == "":
    print("\nNo file provided.\n")
    exit()

class Main():
    BasicInformation = {"Config File":"HeaderConfig.json", "Target File":str(args.t), "OutputFile":"{}Output.csv".format(str(args.t))}
    ResultCharacters= {True:"✔", False:"X"}
    Domains = []
    #Reads the security header config from the json file
    SecurityHeaders = {}
    SecurityHeadersOrder = []
    BooleanHeaders = {}

    def ReadConfig():
        Main.SecurityHeaders = json.loads(open(Main.BasicInformation["Config File"], "r").read())
        Main.SecurityHeadersOrder = list(Main.SecurityHeaders)

    def ReadDomains():
        Main.Domains = open(Main.BasicInformation["Target File"], "r").read().splitlines()

    def SiteConnect(Site):
            #Makes sure that the URL in the file matches the regex
            if re.match("^((http:\/\/)|(https:\/\/)(www\.)?)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", Site) == False:
                print("Site does not match regex.  Please ensure either \'http://\' or \'https://\' is provided.")
                Domains.remove(Site)
                return "False"
            else:
                print("Checking \'{}\' headers.".format(Site))
            #Checks for the sites status code
            try:
                StatusCode = requests.get(Site).status_code
                if StatusCode != 200:
                    print("Site: '{}' returns a HTTP status code of '{}'.  Should probably be something to double check.".format(Site, str(StatusCode)))
            except Exception:
                print("Issue connecting to '{}'.  Make sure that you included the correct URL and that access is available.".format(Site))
                return "False"
            return requests.get(Site).headers

    def CheckHeaders():
        for Site in Main.Domains:
            WebRequest = (Main.SiteConnect(Site))
            if WebRequest == "False":
                break
            #Iterates through the different header titles
            for HeaderTitle in Main.SecurityHeaders:
                if Site not in Main.BooleanHeaders:
                    Main.BooleanHeaders[Site] = {}
                Main.BooleanHeaders[Site][HeaderTitle] = Main.ResultCharacters[False]
                for Header in Main.SecurityHeaders[HeaderTitle]:
                    if Header in WebRequest:
                        #Checks the header values against approved ones
                        if re.search(Main.SecurityHeaders[HeaderTitle][Header], WebRequest[Header]):
                            Main.BooleanHeaders[Site][HeaderTitle] = Main.ResultCharacters[True]

    def WriteOutput():
        with open(Main.BasicInformation["OutputFile"], "a") as CSVOutput:
            Writer = csv.writer(CSVOutput, delimiter=",")
            #Writes table headers
            FormatSecHeader = [""] + Main.SecurityHeadersOrder
            Writer.writerow(FormatSecHeader)

            #Outputs the site results
            for Sites in Main.BooleanHeaders:
                SpreadsheetLines = [Sites]
                for Order in Main.SecurityHeadersOrder:
                    for Header in Main.BooleanHeaders[Sites][Order]:
                        SpreadsheetLines.append(Header)
                print(SpreadsheetLines)

                #Writes site values
                Writer.writerow(SpreadsheetLines)

    def Run():
        Main.ReadConfig()
        Main.ReadDomains()
        Main.CheckHeaders()
        Main.WriteOutput()

Main.Run()
