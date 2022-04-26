#!/usr/bin/env python3

from jinja2 import Template, FileSystemLoader
import ruamel.yaml
import os
import pathlib
from colorama import Fore, Style
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='The file to be templated')
    parser.add_argument('--configFile','-f', help='The config file to be loaded', default='config.yaml')
    args = parser.parse_args()
    return args

yaml = ruamel.yaml.YAML(typ='safe')

def fetchConfig(configFile):
    with open(configFile, 'r') as stream:
        try:
            config = yaml.load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)

def templateFile(file, config):
    with open(file, 'r') as stream:
        try:
            template = Template(stream.read())
            output = template.render(config)
            return output
        except Exception as e:
            print(e)

def saveFile(file, output):
    with open(file, 'w') as stream:
        stream.write(output)

def splitName(file):
    fileName = pathlib.Path(file).name
    return fileName.split('.j2')[0]

def main(file, configFile):
    print(f"{Fore.BLUE}Start template {file} {Style.RESET_ALL}")
    config = fetchConfig(configFile)
    print(f"{Fore.CYAN}This is the config loaded from config.yaml:\n{config}{Style.RESET_ALL}")
    file_path = os.path.join(os.path.dirname(__file__), file)
    templated = templateFile(file_path, config)
    outputFileName = splitName(file)
    saveFile(outputFileName, templated)
    print(f"{Fore.MAGENTA}This is the template file is successfully saved here : {outputFileName}{Style.RESET_ALL}")


main(getArgs().file, getArgs().configFile)

