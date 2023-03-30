import os

def crack_wordlist(filename, wordlist):
    os.system(f"stegseek {filename} {wordlist}")
