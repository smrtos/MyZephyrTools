import os
import sys
import subprocess

import ruamel.yaml
import json

import jsonschema
import cerberus
import pykwalify


def GetYamlFiles(rootDir):
    """
    Get all the yamls recursively from the rootDir
    """
    yamlFiles = []
    for dirPath, subDirPaths, filenames in os.walk(rootDir):
        for filename in filenames:
            if filename.endswith(".yaml"):
                yamlFiles.append(os.path.normpath(os.path.join(dirPath, filename)))
    return yamlFiles


def YamlValidate(yamlFiles, schemaFile):
    """
    Validate the yamlFiles using schemaFile
    """
    invalidYamls = []
    invalidYamlCount = 0
    validYamlCount = 0
    for yamlFile in yamlFiles:
        args = f"-d {yamlFile} -s {schemaFile}"
        process = subprocess.Popen(["pykwalify", "-d", f"{yamlFile}", "-s", f"{schemaFile}"], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout = process.stdout.readline()
        stderr = process.stderr.readline()
        if(not "validation.valid" in stdout):
            invalidYamls.append(yamlFile)
            invalidYamlCount += 1
            print(f"\nInvalid YAML: {yamlFile}")
        else:
            validYamlCount += 1
        print(f"\rValid YAMLs: {validYamlCount}, InvalidYAMLs: {invalidYamlCount}", end="")            
    return invalidYamls


if __name__ == "__main__":
   rootDir = sys.argv[1]
   schema = os.path.normpath(sys.argv[2])
   print("\n")
   print(f"rootDir: {rootDir}")
   print(f"schema: {schema}")   
   yamls = GetYamlFiles(rootDir)
   print(f"Total YAMLs: {len(yamls)}")
   invlaidYamls = YamlValidate(yamls, schema)
   print("\n")
   print(f"rootDir: {rootDir}")
   print(f"schema: {schema}")
   print("Invalid YAMLs:")
   for invalidYaml in invlaidYamls:
       print(invalidYaml)
   pass



