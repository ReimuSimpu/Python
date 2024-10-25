import os
import json
import random
import string
import math
from pystyle import Colors, Center
from concurrent.futures import ThreadPoolExecutor

if os.name == 'nt':
    os.system('title Shitty Teleport Tool - Made By .lordhippo')

BaseFolder = os.getcwd()
OutputFolder = os.path.join(BaseFolder, 'Jsons')
os.makedirs(OutputFolder, exist_ok=True)

def Title():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Center.XCenter(Colors.pink + """
        /$$   /$$ /$$                                     /$$   /$$
        | $$  | $$|__/                                    | $$  | $$
        | $$  | $$ /$$  /$$$$$$   /$$$$$$   /$$$$$$       | $$  | $$  /$$$$$$  /$$    /$$ /$$$$$$  /$$$$$$$ 
        | $$$$$$$$| $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$$$$$$$ |____  $$|  $$  /$$//$$__  $$| $$__  $$
        | $$__  $$| $$| $$  \ $$| $$  \ $$| $$  \ $$      | $$__  $$  /$$$$$$$ \\  $$/$$/| $$$$$$$$| $$  \\ $$
        | $$  | $$| $$| $$  | $$| $$  | $$| $$  | $$      | $$  | $$ /$$__  $$  \\  $$$/ | $$_____/| $$  | $$
        | $$  | $$| $$| $$$$$$$/| $$$$$$$/|  $$$$$$/      | $$  | $$|  $$$$$$$   \\  $/  |  $$$$$$$| $$  | $$
        |__/  |__/|__/| $$____/ | $$____/  \\______/       |__/  |__/ \\_______/    \\_/    \\_______/|__/  |__/
                    | $$      | $$
                    | $$      | $$
                    |__/      |__/
    """))

def Option(Text):
    print(Center.XCenter(Text))

def EditFile(FilePath, Description, Name, RoundPos):
    with open(FilePath, 'r+') as Jsonf:
        Data = json.load(Jsonf)
        Data['description'] = Description or "Teleport"
        Data['name'] = Name or "Teleport"
        if RoundPos:
            Data['position'] = [round(coord, 2) for coord in Data.get('position', [])]
            print(f"Rounded positions: {Data['position']}")
        Jsonf.seek(0)
        json.dump(Data, Jsonf, indent=4)
        Jsonf.truncate()

def EditFiles(Description, Name, RoundPos, SortFile):
    Files = [F for F in os.listdir(OutputFolder) if F.endswith('.json')]
    
    if SortFile:
        Files.sort(key=lambda f: math.sqrt(sum(coord**2 for coord in json.load(open(os.path.join(OutputFolder, f)))['position'])))
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for Index, File in enumerate(Files):
            FilePath = os.path.join(OutputFolder, File)
            if SortFile:
                NewFileName = f"{Index + 1}_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}.json"
                NewFilePath = os.path.join(OutputFolder, NewFileName)
                os.rename(FilePath, NewFilePath)
                print(f"Renamed {File} to {NewFileName}")
                FilePath = NewFilePath
            futures.append(executor.submit(EditFile, FilePath, Description, Name, RoundPos))
        
        for future in futures:
            future.result()

def CheckCoords(Same=True, XRange=0, YRange=0, ZRange=0):
    CoordMap = {}
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(CheckCoordFile, os.path.join(OutputFolder, File), CoordMap, Same, XRange, YRange, ZRange)
            for File in os.listdir(OutputFolder) if File.endswith('.json')
        ]
        for future in futures:
            future.result()

def CheckCoordFile(FilePath, CoordMap, Same, XRange, YRange, ZRange):
    with open(FilePath, 'r') as Jsonf:
        Data = json.load(Jsonf)
    Coords = tuple(Data.get('position', []))
    
    if Same:
        if Coords in CoordMap:
            print(f"Match found: {os.path.basename(FilePath)} and {CoordMap[Coords]} have the same coordinates: {Coords}")
            os.remove(FilePath)
        else:
            CoordMap[Coords] = os.path.basename(FilePath)
    else:
        if any(all(abs(Coords[i] - otherCoords[i]) <= [XRange, YRange, ZRange][i] for i in range(3)) for otherCoords in CoordMap.values()):
            print(f"Match found: {os.path.basename(FilePath)} has similar coordinates.")
            os.remove(FilePath)
        else:
            CoordMap[Coords] = os.path.basename(FilePath)

def TakeFolderContent():
    for Root, _, Files in os.walk(os.path.join(BaseFolder, 'Folders')):
        for File in Files:
            if File.endswith('.json'):
                with open(os.path.join(Root, File), 'r') as F:
                    Content = json.load(F)
                RandomName = ''.join(random.choices(string.ascii_letters + string.digits, k=13)) + '.json'
                with open(os.path.join(OutputFolder, RandomName), 'w') as Outfile:
                    json.dump(Content, Outfile, indent=4)
                print(f"Moved {File} and renamed to {RandomName}")

def SplitFiles(FilesPerFolder):
    Files = [F for F in os.listdir(OutputFolder) if F.endswith('.json')]
    for I in range(0, len(Files), FilesPerFolder):
        NewFolder = os.path.join(OutputFolder, f"Batch_{(I // FilesPerFolder) + 1}")
        os.makedirs(NewFolder, exist_ok=True)
        for File in Files[I:I + FilesPerFolder]:
            os.rename(os.path.join(OutputFolder, File), os.path.join(NewFolder, File))
            print(f"Moved file {File} to {NewFolder}")

def Main():
    Title()
    Option("(1): Edit Files")
    Option("(2): Check Coordinates")
    Option("(3): Take Folder Content")
    Option("(4): Split Files")

    while True:
        try: 
            Choice = int(input(Colors.white + "    > " + Colors.reset))
            break
        except ValueError: 
            print(Colors.red + "Invalid input. Please enter a number." + Colors.reset)

    Title()
    if Choice == 1:
        Description = input(Colors.white + "    Enter description (leave blank for default): ")
        Name = input(Colors.white + "    Enter name (leave blank for default): ")
        RoundPos = input(Colors.white + "    Round positions? (y/n): ").lower() == 'y'
        SortFile = input(Colors.white + "    Sort File by coord? (y/n): ").lower() == 'y'
        EditFiles(Description, Name, RoundPos, SortFile)
    elif Choice == 2:
        NearRangeCheck = input(Colors.white + "    Use near check (y/n)? ").lower() == 'y'
        if NearRangeCheck:
            XRange = float(input(Colors.white + "    Enter X Range: ")) 
            YRange = float(input(Colors.white + "    Enter Y Range: "))
            ZRange = float(input(Colors.white + "    Enter Z Range: "))
            CheckCoords(Same=False, XRange=XRange, YRange=YRange, ZRange=ZRange)
        else:
            CheckCoords(Same=True)

    elif Choice == 3:
        if input(Colors.white + "    Delete old files (y/n)? ").lower() == 'y':
            for File in os.listdir(OutputFolder):
                if File.endswith('.json'):
                    os.remove(os.path.join(OutputFolder, File))
                    print(f"Deleted file: {File}")
        TakeFolderContent()
    elif Choice == 4:
        FilesPerFolder = int(input(Colors.white + "    How many files per folder? "))
        SplitFiles(FilesPerFolder)
    
    Main()

if __name__ == "__main__":
    Main()
