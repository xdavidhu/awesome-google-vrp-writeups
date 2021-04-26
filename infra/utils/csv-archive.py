import sys, csv, requests, urllib

def parse_writeups(writeups_csv):
    writeups = []
    with open(writeups_csv, "r") as csv_file:
        try:
            for line in csv.DictReader(csv_file):
                writeups.append(line)
        except:
            print("[!!!] Can't parse CSV")
            exit(5)
    writeups = sorted(writeups, key=lambda k: k["date"] if (k["date"] != "?") else "0000-00-00", reverse=False)
    return writeups

def archive(url):
    print(f"[+] Archinving '{url}'")
    headers = {"User-Agent": "https://github.com/xdavidhu/awesome-google-vrp-writeups"}
    url = urllib.parse.quote(url)

    try:
        r = requests.get(f"https://web.archive.org/save/{url}", headers=headers, timeout=120, allow_redirects=False)
        print(f"[+] Successfully archived '{url}', archive: '{r.headers['location']}'")
        return r.headers["location"]
    except:
        return False

    return False

def write_writeups(writeups, writeups_csv):
    headers = []
    for key in writeups[0]:
        headers.append(key)

    with open(writeups_csv, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in writeups:
            writer.writerow(row)

if len(sys.argv) < 2:
    print("Usage: python3 csv-archive.py [csv]")
    exit()

writeups = parse_writeups(sys.argv[1])

for writeup in writeups:
    if writeup["archive-url"] == "?":
        if writeup["type"] != "video":
            archive_url = archive(writeup["url"])
            if archive_url != False:
                writeup["archive-url"] = archive_url

write_writeups(writeups, sys.argv[1])
print("[+] Done")