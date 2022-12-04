import os
from collections import defaultdict
r = os.popen("ipconfig")
lines = r.read().split("\n")
ops = defaultdict(list)
current_key = ""
for line in lines:
    if line:
        if (ord(line[0]) > ord(" ")):
            current_key = line
        else:
            ops[current_key].append(line.strip())
wifi_key = [op for op in ops if "wi-fi" in op.lower()]
if wifi_key:
    for line in ops[wifi_key[0]]:
        if "ipv4" in line.lower():
            print()
            print("your network ip:", line.split(":")[-1].strip())
else:
    print("No wifi found")
print("-----"*5)