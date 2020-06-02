
import json

from . import main

def cache_uic(filename = "uic.json"):
    try:
        fp = open(filename)
        d = json.load(fp)
    except:
        # collect by prefix
        d = {}
        for c1 in range(ord('a'),ord('z') + 1):
            for c2 in range(ord('a'),ord('z') + 1):
                prefix = f"{chr(c1)}{chr(c2)}"
                print(prefix)
                x = main.stations(prefix, limit = 100)
                for s in x:
                    mapping = {s['uicCode']: s['name']}
                    try:
                        d = {**d, **mapping}
                    except:
                        pass
        # write to file
        with open(filename, "w") as fp:
            json.dump(d, fp)
    else: 
        fp.close()
    return d
                    
            