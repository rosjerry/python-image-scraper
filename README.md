# Introduction

This is my first experience with Python and my second experience with web scraping.

## Goal of This Repository

The goal of this repository is to gather data for image classification AI.

## What Does This Repository Do?

- Takes a Copart search query URL and parses up to 100 items on the page.
  - (Pagination is not implemented yet, as there are not enough items on the first page.)
- Downloads images of cars as a ZIP archive.
- Includes basic details in TXT format.

## Usage

The images and basic data will help label car images with different attributes such as:
- Color
- Side of the car
- Model
- Brand
- Year
- Fuel type
- Etc.

## Setup

I am using Linux; I will add Windows setup instructions later.

1. Go to the project directory and run `source venv/bin/activate` to activate the virtual environment.
2. Then run:
   ```
   pip install -r requirements.txt
   ```
   to install the required libraries.

## Running the Script

Run:
 to run latest ready scraper file run 
 
 ```
  python copart.com/scrape.py
 ```

it will open playwright chromium broweser in headed mode

after finishing it press enter in cli to end scraping.

rerun the command will not scrape same url again, scraped urls are saved in db.json