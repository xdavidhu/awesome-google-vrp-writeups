from datetime import datetime
import locale

def generate_readme(writeups, output_file):

    writeups = sorted(writeups, key=lambda k: k["date"] if (k["date"] != "?") else "0000-00-00", reverse=True)

    with open(output_file, "w") as output:
        output.write("# Awesome Google VRP Writeups\n🐛 A list of writeups from the Google VRP Bug Bounty program\n\n*\*writeups: **not just** writeups*\n\n")
        output.write("**Follow [@gvrp_writeups](https://twitter.com/gvrp_writeups) on Twitter to get new writeups straigt into your feed!**\n\n")
        output.write("## Contributing:\n\nIf you know of any writeups/videos not listed in this repository, feel free to open a Pull Request.\n\nTo add a new writeup, simply add a new line to `writeups.csv`:\n```\n[YYYY-MM-DD],[bounty],[title],[url],[author-name],[author-url],[type],false,?\n```\n*If a value is not available, write `?`.*<br>\n*The value of `type` can either be `blog` or `video`.*<br>\n*Please keep the last two fields set to `false` and `?`. The automation will modify these fields.*<br>\n*If available, set `author-url` to the author's Twitter URL, so the automation can @mention the author.*\n")

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
                
                author = writeup['author']
                if author == "?":
                    author = "???"
                
                author_url = writeup['author-url']
                if author_url == "?":
                    author_url = "#"
                
                archive_url = writeup['archive-url']
                if archive_url == "?":
                    archive_url = "#"

                output.write(f"- **[{date_string} - ${bounty}]** [{writeup['title']}]({writeup['url']})[*]({archive_url}) by [{author}]({author_url})\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 csv-to-readme.py [csv] [output]")
        exit()
    
    generate_readme(sys.argv[1], sys.argv[2])
    print("[+] Done")