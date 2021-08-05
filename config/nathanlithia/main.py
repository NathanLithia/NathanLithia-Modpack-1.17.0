import sys
import time
from os import system, name, mkdir, getcwd, rename, path
import urllib.request
import zipfile
import shutil
import json


class Minecraft:
    def __init__(self):
        self = Minecraft
        #Name variables passed on from the game
        self.Username = sys.argv[1]
        self.UUID = sys.argv[2]
        self.MinecraftVersion = sys.argv[3]
        self.ForgeVersion = sys.argv[4]
        self.ModCount = sys.argv[5]
        #lets try our best to find where we are
        self.NathanLithiaDir = str(getcwd())
        self.ConfigDir = self.NathanLithiaDir.rstrip("\\nathanlithia")
        self.MinecraftDir = self.ConfigDir.rstrip("\\config")
        self.ShadersDir = self.MinecraftDir+"\\shaderpacks"
        self.AssetsDir = self.MinecraftDir+"\\kubejs\\assets"


class Console:
    def __init__(self):
        self = Console
        Minecraft()
        Commands()
        while True:
            request = input(f"{sys.argv[1]}: ")
            try:
                if request in Commands.ValidCommands:
                    output = eval("Commands."+request+"()")
                    if output != None:
                        print(output)
                else:
                    print(f"Not a valid command: {request}")
            except Exception as e: print(str(e))


class Functions:
    def __init__(self):
        self = Functions

    def download(url, save_path):
        print(f"Downloading: {save_path} from {url}")
        with urllib.request.urlopen(url) as dl_file:
            with open(save_path, 'wb') as out_file:
                out_file.write(dl_file.read())

    def unzipfile(filezip, path):
        print(f"Unzipping {filezip} to {path}.")
        with zipfile.ZipFile(filezip, 'r') as unzip:
            unzip.extractall(path)
    
    def deldir(directory):
        if path.isdir(directory) == True:
            try:
                system(f'rmdir /S /Q "{directory}"')
                print(f'Deleted: {directory}')
            except:
                print(f"failed to delete: {directory}")
        else:
            return


class NLGit:
    def __init__(self):
        self = Git

    def clone(repository, save_path):
        url = f"https://github.com/{repository}/archive/refs/heads/main.zip"
        repohash = NLGit.shahash(repository)
        print(f"Cloning: {save_path} from https://github.com/{repository}\nHash: {repohash}")
        with urllib.request.urlopen(url) as dl_file:
            with open(save_path, 'wb') as out_file:
                try:
                    out_file.write(dl_file.read())
                    print(f"Wrote: {save_path}")
                except Exception as e: print(e)

    def shahash(repository):
        RequestedJson = NLGit.RequestJson(f"https://api.github.com/repos/{repository}/branches/main")
        return RequestedJson['commit']['sha']

    def RequestJson(URL, TimeOutInSeconds = 15):
        try:
            RequestedJson = json.loads(urllib.request.urlopen(URL, timeout=TimeOutInSeconds).read().decode("utf8"))
        except Exception as e:
            print(str(e))
            return e
        else:
            return RequestedJson

class Commands:
    def __init__(self):
        self = Commands
        self.ValidCommands = [ m for m in dir(self) if not m.startswith('__')]

    def stats():
        """Prints minecraft stats"""
        print(f"Username: {Minecraft.Username} / UUID: {Minecraft.UUID}")
        print(f"Minecraft Version: {Minecraft.MinecraftVersion}")
        print(f"Forge: {Minecraft.ForgeVersion} with {Minecraft.ModCount} mods loaded")

    def commands():
        """Prints Commands"""
        print(Commands.ValidCommands)

    def sandbox():
        """Development command for sandboxing code"""
        print("\nThis is a development function, which is really dangerous!")
        print("Type 'break' to exit the loop!\n")
        while True:
            code = input(f"Evaluate: ")
            if code == "break": break
            if code != None:
                try:
                    print(eval(code))
                except Exception as e: print(str(e))

    def clear():
        """Clear console for Windows & Linux/Mac"""
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def update(): 
        """Updates the shader and resources"""
        Commands.shaders()
        Commands.resources()

    def shaders():
        """Updates the shader"""
        NLGit.clone('NathanLithia/NLShader', 'NLShader.zip')
        Functions.unzipfile("NLShader.zip", Minecraft.ShadersDir)
        print("!!! Its highly Recommended to F3-R ingame !!!")

    def resources():
        """Updates the resources"""
        NLGit.clone('NathanLithia/NLResourcePack', 'NLResourcePack.zip')
        Functions.unzipfile('NLResourcePack.zip', Minecraft.NathanLithiaDir)
        Functions.deldir('assets')
        rename('NLResourcePack-main', 'assets')
        Functions.deldir(f'{Minecraft.MinecraftDir}/kubejs/assets')
        shutil.move('assets', f'{Minecraft.MinecraftDir}/kubejs/assets') 
        print("!!! Its highly Recommended to F3-T ingame !!!")


Console()