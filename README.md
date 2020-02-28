# Lurker

A python-based web crawler designed for SMU CS 5337. It is given a preset list of functionalities.

## Installation of Required libraries
```bash
  pip install scrapy
```

## Running the project
In order to run this project, the system must be updated to Python3. A tutorial to do so can be found at: https://realpython.com/installing-python/
##### For Mac:
```bash
  python3 lurker.py
```

## Usage

For the project:
The Web Crawler was developed to only be used on:
http://lyle.smu.edu/~fmoore   aka   https://s2.smu.edu/~fmoore
The crawler is not allowed to get out of this website. The directory(s) listed in the robots.txt file are not to be explored.
The contents of this website will change throughout the Spring 2020 semester.

The required input to the program is 'N', which limits the number of retrieved pages. N should be set such that you retrieve all pages in the directory, and also act as a safety feature for your program to avoid getting an excessive number of pages.

## RoadMap
Ideas to be released int the future - TBD

#### Key Architecture
TBD
#### Identify and describe your major data structures
  Lists are used throughout the project. 
  TBD on more major data structures
#### Politeness
   To avoid overloading a website, a politeness policy is used. The performance of a site is heavily affected while a web crawler downloads a portion. Servers have to handle requests of the viewers of the site and a web crawler could potentially overload it. Administrators are able to indicate which parts of the website that cannot be accessed by the crawler. 
   To implement politness, Lurker uses an interval that restricts itself from overloading the server.

## Bugs
It is known through the project to expect that there are no errors contained in the input files. 
In the very first version, this will be the mindset. 
However, the code will be developed to be robust under Web page errors.

For Efficiency: the project is aimed to be as efficient as possible. Multithreads were not a requirement in the development of this project. In the Project requirements, it's highlighted that "This is a class project, not a production quality implementation."

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and Acknowledgement
Chelby Rhoades, (me), the developer on this project.
Dr. Freeman Moore, my Professor that assigned this project.
My cat Cookie Dough, for being the best, sweetest, greatest, most amazing, jaw-droppingly intelligent, talented, and always there for me.

## License
Currently, a license does not exist other than the code was developed in SMU's Spring 2020 CS 5337/7335 course: Information Retrieval and Web Search

## Project Status
The project was created on 02.28.2020:09:48 and will continue to be updated throughout the semester of this course.
