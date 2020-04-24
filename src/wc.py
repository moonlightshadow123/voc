import os
wc_data = []
with open("google10000.txt", "r") as f:
    for eachLine in f:
        wc_data.append(eachLine.strip(" ").strip('\r\n'))
# print(wc_data)