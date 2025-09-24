this is my first touch with python and second touch with scraping

gaol of this repo:
gathering data for image classification ai


what does this repo do:
takes copart search query url and parses up to 100 items on page
(did not implemented pagination yet, not enough items on first page)
it download images of car with zip archive
also it includes basic details in txt format

what is useage of this repo:
images and basic data will help to label car images with different definitions such as:
color, side of car, model, brand, year, feul type and etc.

setup:
I have linux, I'll add windows setup later
go to project directory and run 'source venv/bin/activate' to activate virtual environment
and then run
pip install -r requirements.txt
to install requirements and libraries

run "python copart.com/scrape.py"
is opens playwright chromium browser with headed mode and starts scraping