# seatrack
------

http://3.88.29.132/
Python flask app hosted on Amazon EC2 using Gunicorn & Nginx, use this link to access the deployed webapp: http://3.88.29.132/
-----

OpenSea collection and floor tracking webapp built in Python, Flask and My SQL, integrated with OpenSea API.

Version 2.0 is a functioning webapp that succesfully integrates OpenSea API to track floor price & market cap of specific collections that are added by users.

Includes a many to many SQL database relationship to track how many followers each collection has, as well as basic validation & bcrypt hashing for the login & registration.

Updated 5.22.22

Video walkthrough of the updated SeaTrack app: https://www.loom.com/share/f66403dafaa642f3be490bf065f3da4b

Future roadmap:

-typo corrections (dashboard)
-improved UI experience
-additional API data & API assets like images
-favorite collection filtering page so a user can see only their favorite collections
-discord bot integration for integration with a community discord server
