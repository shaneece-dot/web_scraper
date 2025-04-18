# web_scraper
# VacancyMail Job Scraper 🕵️‍♀️

This is a Python web scraper that extracts the latest job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/). It saves the job data (like title, company, expiry date, and more) into a `CSV` file for easy access and analysis.

## 💡 Features

- Scrapes the top job listings from VacancyMail
- Extracts job title, company, location, expiry date, and description
- Saves data to a CSV file
- Easy to customize or automate
- Logs activity to `scraper.log`

## 📦 Requirements

- Python 3.8 or above
- Libraries used:
  - `requests`
  - `beautifulsoup4`
  - `pandas`

Install the dependencies with:

```bash
pip install -r requirements.txt
