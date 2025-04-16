import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_vacancymail():
    url = "https://vacancymail.co.zw/jobs/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    jobs_data = []
    
    try:
        logging.info(f"Starting scrape of {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('a', class_='job-listing')[:10]  # Get only first 10 jobs
        
        for job in job_listings:                        
            try:
                # Extract job title
                title_elem = job.find('h3', class_='job-listing-title')
                title = title_elem.text.strip() if title_elem else "Not specified"
                
                # Extract company
                company_elem = job.find('h4', class_='job-listing-company')
                company = company_elem.text.strip() if company_elem else "Not specified"
                
                # Extract location and expiry date from footer
                footer = job.find('div', class_='job-listing-footer')
                location = "Not specified"
                expiry_date = "Not specified"
                
                if footer:
                    # Get all list items in footer
                    items = footer.find_all('li')
                    for item in items:
                        text = item.get_text(strip=True)
                        # Check for location (looks for location pin icon class)
                        if 'icon-material-outline-location-on' in str(item):
                            location = text
                        # Check for expiry date (looks for time icon class)
                        elif 'icon-material-outline-access-time' in str(item) and 'Expires' in text:
                            expiry_date = text.replace('Expires', '').strip()
                
                # Extract job description
                description_elem = job.find('p', class_='job-listing-text')
                description = description_elem.text.strip() if description_elem else "Not specified"
                
                jobs_data.append({
                    "Job Title": title,
                    "Company": company,
                    "Location": location,
                    "Expiry Date": expiry_date,
                    "Description": description,
                    "Scraped Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
            except Exception as e:
                logging.error(f"Error processing job listing: {str(e)}")
                continue
        
        # Create DataFrame and save to CSV
        if jobs_data:
            df = pd.DataFrame(jobs_data)
            df.to_csv('scraped_data.csv', index=False)
            logging.info(f"Successfully saved {len(jobs_data)} jobs to scraped_data.csv")
            return df
        else:
            logging.warning("No job listings found")
            return None
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    scrape_vacancymail()