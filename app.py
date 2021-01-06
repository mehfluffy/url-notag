#!/usr/env/python3

from parser import parser

def main():
    url = input("Paste URL to be cleaned: ")
    print("Clean URL:", parser(url))

if __name__ == "__main__":
    main()