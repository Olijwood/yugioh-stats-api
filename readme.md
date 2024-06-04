# Yugioh Daily Automated Price Statistics 

## WORK IN PROGRESS

'*' This project is currently a 'Work in Progress'(WIP). Most functionality is present (which you may see when inspecting the code)

Features to be completed:

- Card Detail View HTML
- Functions to simulate other yugioh sets with different probabilities for 'opening'
- Updating the set-detail view to display the average values for the given set, its value gain/loss once opened and a graph tracking its value over time.
- Adding a graph tracking eacg card's value over time for its corresponding detail view
- Updating the filter functionality for the card list view for each Set (currently broken after some code changes)

With this in mind, if you do attempt to run every feature with in this current stage of development you will likely run into some errors. '*'

## Introduction

This project scrapes data for (Yugioh) sets and cards from TCGPlayer. The initial scraping of the webpages is done using Selenium instead of BeautifulSoup as TCGPlayer loads the content of its pages after the GET request. BeautifulSoup is then used to find the neccesary data from the returned HTML, which will then be saved through the corresponding Django Model into the database. 

As there are hundreds of sets and countless cards it would be ineffienct to be scraping one at a time, to optimize the time for this process to occur I use Celery and Redis to aynschronously scrape the tcg pages in chunks. Celery is also used so that these 'Tasks' can be automated to run on a schedule(currently daily).

The initial scrape for each set's cards will gather the basic data for each card (eg: Image, Name, Rarity, Details etc) aswell as the prices. Afterwards, it will just be the Market Price and Min listed price being scraped to optimize performance. 

Each Yugioh Set comes in a variety of containers, the standard usually being a booster box. So for each set I've written a function that calculate the probability of each rarity being opened for a pack in that booster box, to then return the total value based on the market price for each 'opened' card. This will be run 10,000 times for a more accurate representation of the value of the booster box to run statistics on. Again I use Celery Tasks to optimize speed.

Then using statistics I find the most likely value of the booster box (For that day's market prices of that set). With the latest being displayed on that Sets Detail Page and a graph showing the tracking history. I also calculate the percentage increase/descrease from the value of the sealed box to the probable value once opened and display that.

## Getting Started

'*' This project is in development on a laptop with 16Gb RAM and an I7 processor. When the tasks are being called it uses most of the memory and processing, so if your system does not meet these specificatons I do not recommend runnning this project as it will likely crash '*'

To set up the project:

1. Ensure Redis is installed and running (listening on localhost:6379)

2. Install all dependencies listed in requirements.txt. The project requires Python 3.12.

- `pip install -r requirements.txt`

3. After installing dependencies, migrate the database and start the Django server:

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

4. In a separate terminal, launch the Celery worker:

- `celery -A yugiohscraper worker -l info`

5. Open `initial-scrape.ipynb` and run all cells

After following these steps, the program will run automatically everyday (unless you close the redis-server or celery workers)

## Technologies used

- **Django**: Django framework powers the backend development of the project.
- **Celery**: Celery is used for task queue implementation.
- **Selenium**: Selenium automates web browser interaction for scraping.
- **Redis**: Redis serves as the broker for Celery.
- **Bootstrap**: Bootstrap framework is utilized for frontend styling.
- **MatPlotLib/Seaborn**: For visualising the data analysis of the market prices

## About the Author

This project is maintained by **Oliver Wood**. Connect with me on [LinkedIn](https://www.linkedin.com/in/olijwood)!

## Thank You

Thank you for your interest in this Daily Automated Yugioh Price Statistics Project! 