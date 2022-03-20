
import os
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
import time
from tqdm import tqdm

d = "repos"

for dirpath, dirnames, filenames in tqdm(os.walk(d)):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        if full_path.endswith(".py"):
            print(green(f"Keeping {full_path}"))
        else:
            print(red(f"Deleting {full_path}"))

            if d in full_path:
                os.remove(full_path)
            else:
                print(yellow("Something is wrong"))
                time.sleep(60)