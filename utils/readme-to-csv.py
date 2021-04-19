import re
from datetime import datetime
import csv
import sys

writeup_regex = r"- \*\*\[((\w\w\w) (\d\d)|\?\?\?) - \$([0-9,.]*|\?\?\?)]\*\* \[([^\]]*)\]\(([^\)]*)\) by \[([^\]]*)\]\(([^\)]*)\)"

data = []
year = 0
type = "blog"
introduction = True

if len(sys.argv) < 3:
    print("Usage: python3 readme-to-csv.py [readme] [output]")
    exit()

# loop through every line
file = open(sys.argv[1], "r")
for line in file:
    
    # skip the introduction
    if line == "## Blog posts:\n":
        introduction = False
        continue
    if introduction:
        continue

    # skip the empty lines
    if line == "\n":
        continue
    
    # update parameters if the line is not a writeup
    if line.startswith("##"):
        if "Videos" in line:
            type = "video"
            year = 0
        elif "Unknown Date:" in line:
            year = 0
        else:
            match = re.search(r"\d\d\d\d", line)
            year = int(match.group(0))
    else:
        # parse the data line with writeup_regex
        match = re.search(writeup_regex, line)
        
        if year == 0:
            date = "?"
        else:
            # reformat the date to YYYY-MM-DD
            date_string = str(year) + " " + match.group(1)
            datetime_object = datetime.strptime(date_string, "%Y %b %d")
            date = datetime_object.strftime("%Y-%m-%d")

        # save the row
        row = {
            'date': date,
            'bounty': match.group(4).replace(",", "") if not match.group(4)=="???" else "?",
            'title': match.group(5),
            'url': match.group(6),
            'author': match.group(7) if not match.group(7)=="???" else "?",
            'author-url': match.group(8) if not match.group(8)=="#" else "?",
            'type': type
        }
        data.append(row)
file.close()

# prepare the csv headers
headers = []
for key in data[0]:
    headers.append(key)

# save to csv
with open(sys.argv[2], "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("[+] Done")