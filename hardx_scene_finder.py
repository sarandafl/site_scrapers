# +---------------------------------------------+
# | Author: sarandafl                           |
# |                                             |
# | Usage:                                      |
# | Return all photo- and/or video scenes for   |
# | a specific actress or actor from hardx.com  |
# |                                             |
# +---------------------------------------------+
# | Example:                                    |
# | Return all videos and photos.               |
# | get_scene_info.py -a "august ames" -v -p    |
# |                                             |
# +---------------------------------------------+

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser


# Changes the date from 'YYYY-MM-dd' to 'dd.MM.YY'
def fix_date(scene_date):
    date = datetime.strptime(scene_date, '%Y-%M-%d')
    return format(date, '%d.%M.%y')


# Removes whitespace from string and returns the safe word to use in the URL manipulation.
def make_url_safe(actress_name):
    if " " in actress_name:
        return (actress_name.replace(' ', '%20')).lower()
    else:
        return actress_name.lower()


# Shows whether the current output is outputting video- or photo scenes.
def scene_type(link):
    if "scene" in link:
        return "Videos"
    else:
        return "Photos"


# Passes on the correct URL(s) needed for the request.
def correct_urls(argv, argp, actress_name):
    # Checks if the -v or -p (or both) argument was used.
    if argv is True and argp is True:
        return ["http://www.hardx.com/en/search/" + actress_name + "/scene?query=" + actress_name,
                "http://www.hardx.com/en/search/" + actress_name + "/photoSet?query=" + actress_name]
    elif argv is True and argp is False:
        return ["http://www.hardx.com/en/search/" + actress_name + "/scene?query=" + actress_name]
    else:
        return ["http://www.hardx.com/en/search/" + actress_name + "/photoSet?query=" + actress_name]


def main():
    parser = ArgumentParser()

    parser.add_argument("-a", dest="actress_name", help="The name of the actress/actor.")
    parser.add_argument('-v', action="store_true", help="Use this arguments to get all the video scenes for the actress/actor.")
    parser.add_argument('-p', action="store_true", help="Use this arguments to get all the photo scenes for the actress/actor.")

    args = parser.parse_args()

    actress_name = make_url_safe(args.actress_name)
    urls = correct_urls(args.v, args.p, actress_name)

    # Iterate over the URLs - needed when both -v and -p are selected.
    for url in urls:
        request = requests.get(url)

        data = request.text
        soup = BeautifulSoup(data, 'html.parser')

        if soup.findAll("div", {"class": "tlcDetails"}):
            num_of_files = len(soup.findAll("div", {"class": "tlcDetails"}))
            print("\n" + str(num_of_files) + " " + scene_type(url) + " scenes found:")

            # Extracting the relevant scene information.
            for link in soup.findAll("div", {"class": "tlcDetails"}):
                scene_name = link.find('a').contents[0]
                release_date = fix_date((link.find("span", {"class": "tlcSpecsDate"}).contents[2]).contents[0])

                # Extract a list of actors
                for cast_member in link.findAll("div", {"class": "tlcActors"}):
                    cast = []
                    for person in cast_member.findAll("a"):
                        cast.append(person.contents[0])

                pornstars = ", ".join(cast)
                print("[HardX]" + str(pornstars) + " - " + str(scene_name) + "[" + str(release_date) + "]")
        else:
            print("No matching actresses or actors with the name '" + actress_name + "' found!")

if __name__ == "__main__":
    main()
