import os, json, random, string, math, time
from concurrent.futures import ThreadPoolExecutor
from pystyle import Colors, Center
from threading import Lock

BaseFolder = os.getcwd()
OutputFolder = os.path.join(BaseFolder, 'Jsons')
os.makedirs(OutputFolder, exist_ok=True)
os.system('title Shitty Teleport Tool - Made By .lordhippo')

def Title():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Center.XCenter(Colors.pink + r"""
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

def Option(Text): print(Center.XCenter(Text))
def EditFile(FilePath, Description, Name, RoundPos):
    with open(FilePath, 'r+') as Jsonf:
        Data = json.load(Jsonf)
        Data.update({
            'description': Description or "Teleport",
            'name': Name or "Teleport",
            'position': [round(coord, 2) for coord in Data.get('position', [])] if RoundPos else Data.get('position', [])
        })
        Jsonf.seek(0); json.dump(Data, Jsonf, indent=4); Jsonf.truncate()

def EditFiles(Description, Name, RoundPos, SortFile):
    Files = [F for F in os.listdir(OutputFolder) if F.endswith('.json')]
    if SortFile: Files.sort(key=lambda f: math.sqrt(sum(coord**2 for coord in json.load(open(os.path.join(OutputFolder, f)))['position'])))
    with ThreadPoolExecutor() as executor:
        futures = [  executor.submit(EditFile, os.path.join(OutputFolder, File), Description, Name, RoundPos) for File in Files ]
        for future in futures: future.result()

CoordMapLock = Lock()
def CheckCoordFile(FilePath, CoordMap, Same, Ranges):
    with open(FilePath, 'r', encoding='utf-8') as Jsonf:
        Coords = tuple(json.load(Jsonf).get('position', []))
    
    with CoordMapLock:
        if Same:
            if Coords in CoordMap:
                print(f"Match found: {os.path.basename(FilePath)} and {CoordMap[Coords]} have the same coordinates: {Coords}"); os.remove(FilePath)
            else:
                CoordMap[Coords] = os.path.basename(FilePath)
        else:
            for coord, name in CoordMap.items():
                if all(abs(Coords[i] - coord[i]) <= Ranges[i] for i in range(3)):
                    print(f"Close match found: {os.path.basename(FilePath)} is close to {name}"); os.remove(FilePath); return
            CoordMap[Coords] = os.path.basename(FilePath)

def CheckCoords(Same=True, XRange=0, YRange=0, ZRange=0):
    Ranges,CoordMap = (XRange, YRange, ZRange),{}
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(CheckCoordFile, os.path.join(OutputFolder, File), CoordMap, Same, Ranges)
                   for File in os.listdir(OutputFolder) if File.endswith('.json')]
        for future in futures: future.result()

def TakeFolderContent():
    StartTimer, TotalJsons, TotalFolders = time.time(), 0, 0
    
    for root, _, files in os.walk(os.path.join(BaseFolder, 'Folders')):
        JsonFiles = [f for f in files if f.endswith('.json')]
        NumJsons = len(JsonFiles)
        
        if NumJsons > 0:
            TotalJsons += NumJsons
            TotalFolders += 1
            print(f"Going through {os.path.basename(root)}, {NumJsons} JSON(s)")
        
            for JsonFile in JsonFiles:
                with open(os.path.join(root, JsonFile), 'r', encoding='utf-8') as f:
                    Content = json.load(f)
                RandomName = f"{''.join(random.choices(string.ascii_letters + string.digits, k=13))}.json"
                with open(os.path.join(OutputFolder, RandomName), 'w', encoding='utf-8') as Outfile:
                    json.dump(Content, Outfile, indent=4)

    print(f"\nFinished {TotalJsons} files in {TotalFolders} folders, Time taken: {time.time() - StartTimer:.2f} seconds"); time.sleep(1)

def SplitFiles(FilesPerFolder):
    Files = [F for F in os.listdir(OutputFolder) if F.endswith('.json')]
    for I in range(0, len(Files), FilesPerFolder):
        NewFolder = os.path.join(OutputFolder, f"Batch_{(I // FilesPerFolder) + 1}"); os.makedirs(NewFolder, exist_ok=True)
        for File in Files[I:I + FilesPerFolder]: os.rename(os.path.join(OutputFolder, File), os.path.join(NewFolder, File)); print(f"Moved file {File} to {NewFolder}")

def Main():
    while True:
        Title(); Option("(1): Edit Files"); Option("(2): Check Coordinates"); Option("(3): Take Folder Content"); Option("(4): Split Files")

        try:  Choice = int(input(Colors.white + "    > " + Colors.reset))
        except ValueError:  print(Colors.red + "Invalid input. Please enter a number." + Colors.reset); continue

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
                        os.remove(os.path.join(OutputFolder, File)); print(f"Deleted file: {File}")
            TakeFolderContent()
            
        elif Choice == 4:
            FilesPerFolder = int(input(Colors.white + "    How many files per folder? "))
            SplitFiles(FilesPerFolder)

if __name__ == "__main__":
    Main()
