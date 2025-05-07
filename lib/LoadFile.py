def loadFile(path):
    try:
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as error:
        print(f"[!] Failed to load wordlist: {error}")
        return []