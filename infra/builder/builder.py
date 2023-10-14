import os, random, string, errno, csv, requests, re, urllib
from requests_oauthlib import OAuth1Session
import csv_to_readme

twitter_ck = os.getenv("AGVRPW_TWITTER_CK", "")
twitter_cs = os.getenv("AGVRPW_TWITTER_CS", "")
twitter_rk = os.getenv("AGVRPW_TWITTER_RK", "")
twitter_rs = os.getenv("AGVRPW_TWITTER_RS", "")
workspace_dir = os.getenv("GITHUB_WORKSPACE")
repo_url = "https://github.com/xdavidhu/awesome-google-vrp-writeups"

def random_string(length):
    return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

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

def parse_twitter_user(author_url):
    match = re.match(r"https:\/\/twitter.com\/([a-zA-Z0-9_]+)", author_url)
    if match != None:
        return match.group(1)
    return False

def new_tweet(title, bounty, author, url, mention=False):
    twitter = OAuth1Session(twitter_ck, client_secret=twitter_cs, resource_owner_key=twitter_rk, resource_owner_secret=twitter_rs)
    
    title = (title[:137] + "...") if len(title) >= 140 else title
    if len(author) >= 50:
        mention = False
    author = (author[:47] + "...") if len(author) >= 50 else author

    author_string = "@" + author if mention else author
    bounty_string = "???" if bounty == "?" else f"{float(bounty):,g}"
    tweet_string = f"New Google VRP writeup \"{title}\" for a bounty of ${bounty_string} by {author_string}:\n{url}"
    try:
        r = twitter.post("https://api.twitter.com/2/tweets", data={"text": tweet_string})
        if r.status_code == 200:
            return True
        else:
            print(f"[!] Twitter API call to '/2/tweets' failed:")
            print(r.status_code)
            print(r.content)
    except:
        print(f"[!] Twitter API call to '/2/tweets' failed with an exception")
        return False
    
    return False

def archive(url):
    print(f"[+] Archinving '{url}'")
    headers = {"User-Agent": repo_url}
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

def builder():
    writeups_csv = os.path.join(workspace_dir, "writeups.csv")
    readme_md = os.path.join(workspace_dir, "README.md")

    if not os.path.isfile(writeups_csv):
        print("[!!!] writeups.csv doesn't exist")
        exit(5)
    
    writeups = parse_writeups(writeups_csv)

    for writeup in writeups:

        # Tweet new writeups
        if writeup["tweeted"] == "false":
            print("[+] Tweeting " + writeup["url"])
            mention = True
            author = parse_twitter_user(writeup["author-url"])
            if author == False:
                mention = False
                author = writeup["author"]
            if new_tweet(writeup["title"], writeup["bounty"], author, writeup["url"], mention=mention) == True:
                writeup["tweeted"] = "true"
                print("[+] Writeup " + writeup["url"] + " tweeted and updated successfully")
        
        # Archive writeups
        if writeup["archive-url"] == "?":
            if writeup["type"] != "video":
                archive_url = archive(writeup["url"])
                if archive_url != False:
                    writeup["archive-url"] = archive_url

    # Generate new README.md
    csv_to_readme.generate_readme(writeups, readme_md)
    
    write_writeups(writeups, writeups_csv)

    # Request an archive for the repo page
    archive(repo_url)

builder()
