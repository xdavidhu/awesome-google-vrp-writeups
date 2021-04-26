from datetime import datetime
import locale

def generate_readme(writeups, output_file):

    writeups = sorted(writeups, key=lambda k: k["date"] if (k["date"] != "?") else "0000-00-00", reverse=True)

    with open(output_file, "w") as output:
        output.write("# Awesome Google VRP Writeups\n🐛 A list of writeups from the Google VRP Bug Bounty program\n\n*\*writeups: **not just** writeups*\n")

        types = ["blog", "video"]
        for type in types:

            if type == "blog":
                output.write("\n## Blog posts:\n")
            elif type == "video":
                output.write("\n## Videos:\n")

            last_year = False
            for writeup in writeups:
                if writeup["type"] != type:
                    continue

                if writeup["date"] != "?":
                    date = datetime.strptime(writeup["date"], "%Y-%m-%d")
                else:
                    date = False
                
                if date != False:
                    if last_year != date.year:
                        output.write(f"\n### {date.year}:\n\n")
                        last_year = date.year
                if date == False:
                    if last_year != "?":
                        output.write(f"\n### Unknown Date:\n\n")
                        last_year = "?"
                
                if date != False:
                    date_string = date.strftime("%b") + " " + date.strftime("%d")
                else:
                    date_string = f"???"
                
                if writeup["bounty"] != "?":
                    bounty = f"{float(writeup['bounty']):,g}"
                else:
                    bounty = "???"
                
                if writeup['author'] == "?":
                    writeup['author'] = "???"
                if writeup['author-url'] == "?":
                    writeup['author-url'] = "#"

                output.write(f"- **[{date_string} - ${bounty}]** [{writeup['title']}]({writeup['url']}) by [{writeup['author']}]({writeup['author-url']})\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 csv-to-readme.py [csv] [output]")
        exit()
    
    generate_readme(sys.argv[1], sys.argv[2])
    print("[+] Done")