"""
A script to automate the YAML file validation.
By ming.shao@intel.com
"""
import argparse
import os
import sys
import subprocess
import time

import ruamel.yaml
import json

import jsonschema
import cerberus
import pykwalify



def parse_arguments():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-T", dest="rootDir", action="store", help="the root where to scan for YAMLs.")
    parser.add_argument("-s", dest="schemaFile", action="store", help="the full path of the pykwalify YAML schema file.")
    options = parser.parse_args()
    if options.rootDir is None or options.schemaFile is None:
        parser.print_help()
        sys.exit(0)
    return options


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

def main():
    start_time = time.time()
    options = parse_arguments()
    rootDir = options.rootDir
    schemaFile = options.schemaFile
    print("\n")
    print(f"rootDir: {rootDir}")
    print(f"schema: {schemaFile}")     
    yamls = GetYamlFiles(rootDir)
    print(f"Total YAMLs: {len(yamls)}")
    invlaidYamls = YamlValidate(yamls, schemaFile)
    print("\n")
    print(f"rootDir: {rootDir}")
    print(f"schema: {schemaFile}")
    print("Invalid YAMLs:")
    for invalidYaml in invlaidYamls:
        print(invalidYaml)
    duration = time.time() - start_time
    print(f"Completed in {duration} seconds")
    pass

if __name__ == "__main__":
    main()
    pass



