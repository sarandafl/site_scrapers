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


# Get a list of all available pornstars.
def get_pornstars():
    pornstars = []

    request = requests.get("http://www.hardx.com/en/models/alphabetical/1/0")
    data = request.text
    soup = BeautifulSoup(data, 'html.parser')

    for ul in soup.findAll("div", {"class": "Giraffe_ActorList Gamma_Component Giraffe_ActorList_Filters Giraffe_ActorList_Structure Giraffe_ActorList_Title"}):
        for li in ul.findAll("li"):
            if li.find('a').get('href') is not None:
                pornstars.append((li.find('a').contents[0]).strip())
                #print((li.find('a').contents[0]).strip())
    
    return pornstars


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
        
        return "Video scenes:"
    else:
        
        return "Photo scenes:"


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


# Fetches all scenes from the URL matching the optional filter.
def get_scenes(url, filter):
    filter = filter.lower()
    scenes = []

    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data, 'html.parser')

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
        scene = "[HardX]" + str(pornstars) + " - " + str(scene_name) + "[" + str(release_date) + "]"

        # Only append the matched scenes to return.
        if filter in scene.lower():
            scenes.append(scene)

    return scenes


def main():
    parser = ArgumentParser()

    parser.add_argument("-a", dest="actress_name", default="", help="The name of the actress/actor.")
    parser.add_argument('-v', action="store_true", help="Use this arguments to get all the video scenes for the actress/actor.")
    parser.add_argument('-p', action="store_true", help="Use this arguments to get all the photo scenes for the actress/actor.")
    parser.add_argument('-l', action="store_true", help="Outputs a list of all pornstars. Not compatible with '-a','-v','-p','-f'.")
    parser.add_argument('-f', dest="filter", default="", help="Filter scenes by using a single keyword.")

    args = parser.parse_args()

    filter = args.filter
    actress_name = make_url_safe(args.actress_name)

    # Outputs a list of pornstars when only the '-l' argument is used.
    if actress_name is "":
        if args.l is True:
            pornstars = get_pornstars()
            output_pornstars = "\n".join(pornstars)
            print(output_pornstars)
    else:
        urls = correct_urls(args.v, args.p, actress_name)

        # Iterate over the URLs - needed when both -v and -p are selected.
        for url in urls:
            scenes = get_scenes(url, filter)
            output_scenes = "\n".join(scenes)

            print("\n" + str(len(scenes)) + " " + scene_type(url))
            print(output_scenes)

if __name__ == "__main__":
    main()
