# iNaturalist-Uploads

### Thanks
To [glmory](https://www.inaturalist.org/people/glmory), the iNaturalist user who brought the idea up on
the iNaturalist forums and graciously allowed me to fork his uploader to get started.

To [Micah Scott](http://twitter.com/scanlime), one of the most thoughtful folks I'm acquainted with, for (besides being a lovely person) a body of video work 
that has been and still is wonderful encouragement that there are still human ways we can poke at tech instead of engaging with silicon valley,
drones, AI, or venture capital.

To iNaturalist, of course, not just for making a fascinating platform I greatly enjoy using, but for exposing a set of APIs to make this possible.

### What's iNaturalist?

I would defer [to them](https://www.inaturalist.org/pages/help#general1)

### What's this thing for?

The idealized finished version (we might get there eventually) is a utility to facilitate combining photos, GPS data, 
and metadata (e.g., gender, invasive status, captivity status) to streamline getting your observations onto iNat

[iNaturalist](https://www.inaturalist.org) has a fairly nice full featured uploader--it rules if you have
one, or five, or ten observations to add. But if you have 50 from a camping trip, or --like me-- you put off cleaning off 
your camera for a few months and now there are 200, it's a little tedious.

It also requires configuring location data unless your 
photo taking device embeds it in each photo.  The latter isn't much recommended for privacy reasons, so what then?  Hikers
might be familiar with GPX files recording by a smartphone hiking app or dedicated GPS device; among other things these files 
typically have a set of GPS points each with a datestamp. From those datestamps we can estimate the correct location of a
photo plenty close enough for iNaturalist. If you're doing an area survey, or working with endangered species this 
might not be precise enough, but for most it should be fine.

### How do I use it?

#### Requirements
* Python >= 3.7
* [poetry](https://github.com/sdispater/poetry) (or, feel free to use another package manager if you want to parse dependencies out of the poetry project files yourself)

#### Installation
* Install Python
* Install poetry (typically `pip install poetry` from your shell of choice)
* Extract the release, mantaining relative paths
* In your shell, navigate to the extracted files and use the command `poetry install`
* Poetry will install the required packages; this may take a few minutes
* The GUI application can be launched with `poetry run python gui.py`
  
#### Usage
* [wip]


# Reference

### Packages
[Pillow](https://pillow.readthedocs.io/en/3.0.x/index.html) (PIL fork)  
[Pyinaturalist](https://github.com/inbo/pyinaturalist)   
[pytz](https://pypi.org/project/pytz/)  
[keyring](https://keyring.readthedocs.io/en/latest/) ([Github](https://github.com/jaraco/keyring))  
[PySimpleGUI](https://pysimplegui.readthedocs.io/)  
[poetry](https://github.com/sdispater/poetry)  
[pendulum](https://github.com/sdispater/pendulum)  
[pytest]()

### External docs
[iNaturalist JSON API ](https://api.inaturalist.org/v1/docs/)  
[iNaturalist REST API](https://www.inaturalist.org/pages/api+reference)  
[Exif tag catalog](https://www.exiv2.org/tags.html)  
[GPX file format](https://www.topografix.com/gpx.asp)
[Accepted timezones](https://gist.github.com/mjrulesamrat/0c1f7de951d3c508fb3a20b4b0b33a98)
