# Trading Card Daily Automated Price Statistics 

## Introduction

This project automates the collection and analysis of trading card data from multiple sources, primarily focusing on Yugioh sets and cards from TCGPlayer and CardMarket (European Markets). The project leverages several technologies to efficiently scrape, process, and analyze large datasets, presenting valuable insights into the market prices and potential profitability of trading card sets.

### Key Features

- **Automated Data Collection:** Utilizes Selenium to scrape dynamic content from TCGPlayer and CardMarket's API for European market data.

- **Efficient Data Processing:** Implements Celery and Redis to handle asynchronous tasks, optimizing the scraping process by running tasks in parallel.

- **Statistical Analysis:** Simulates the opening of booster boxes to estimate the value of each set, running these simulations 100,000 times for accuracy.

- **Historical Data Tracking:** Tracks and visualizes the value changes of booster boxes over time, providing insights into market trends.

- **API Integration:** Includes a RESTful API using Django Rest Framework, enabling third-party access to the collected data.


## Getting Started

**Note**: This project is resource-intensive and was developed on a system with 16GB RAM and an i7 processor. Running it on systems with lower specifications may lead to performance issues.

### Prerequisites
 
 - Python 3.12
 - Redis

### Installation

1. **Ensure Redis is installed and running**(listening on localhost:6379)

2. **Install dependencies:**

- `pip install -r requirements.txt`

3. **Migrate the database:**

- `python manage.py makemigrations`
- `python manage.py migrate`

4. **In a separate terminal, launch the Celery worker:**

- `celery -A yugiohstats worker --beat -l info`

5. **Run initial data collection:**

Find the call_tasks directory in `./backend/yugiohstats/` and run every cell in:

 - `cm-main-tasks.ipynb`
 - `tcg-main-tasks.ipynb`

6. **Access the application:**

- `python manage.py runserver`

After following these steps, navigate to the link you see after running the server to see the data!

## Technologies used

- **Django**: Django framework powers the backend development of the project.
- **Celery**: Celery is used for task queue implementation.
- **Selenium**: Selenium automates web browser interaction for scraping.
- **Redis**: Redis serves as the broker for Celery.
- **Bootstrap**: Bootstrap framework is utilized for frontend styling.
- **MatPlotLib/Seaborn**: For visualising the data analysis of the market prices
- **Django Rest Framework**: To allow third parties to request data from this application.

## WORK IN PROGRESS

'*' This project is currently a 'Work in Progress'(WIP). While most functionality is operational, ongoing developments include:

- Enhancing Card Detail View
- Expanding simulation functions to accommodate various Yugioh sets with different opening probabilities.
- Fixing and updating the filter functionality for the card list view.
- Extending API capabilities to expose more data.

## About the Author

This project is maintained by **Oliver Wood**. Connect with me on [LinkedIn](https://www.linkedin.com/in/olijwood)!

## Thank You

Thank you for your interest in the Trading Card Daily Automated Price Statistics Project! Your feedback and contributions are welcome as this project continues to evolve.