import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to scrape the website and extract the specific link
def get_url(link):
    try:
        logging.info(f"Processing URL: {link}")
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # Find all divs with class 'row proceeding-row'
            rows = soup.find_all('div', class_='row proceeding-row')

            # Iterate through each row to find the one containing 'Additional information'
            for row in rows:
                label_div = row.find('div', class_='col-lg-4 col-5 body proceeding-label')
                if label_div and 'Additional information' in label_div.text:
                    # Find the corresponding body div
                    body_div = row.find('div', class_='col-lg-8 col-7 body')
                    if body_div:
                        # Extract the text from the <p> tag and get the link part
                        p_tag = body_div.find('p')
                        if p_tag:
                            link_text = p_tag.text.split(':')[-1].strip()
                            logging.info(f"Found link: {link_text}")
                            return link_text  # Return the found link

            logging.warning("Link not found")
            return "Link not found"  # Case when 'Additional information' row is not found
        else:
            logging.error("Request failed with status code: " + str(response.status_code))
            return "Request failed"  # Case when the HTTP request fails
    except requests.RequestException as e:
        logging.error(f"RequestException for URL: {link} - {e}")
        return "Invalid URL or request failed"  # Case when the URL is invalid or the request fails

# Function to process a list of URLs and save the results in a DataFrame
def process_urls_from_csv(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    input_df = pd.read_csv(input_csv)

    # Assuming the column containing URLs is named 'URL'
    data = []
    for index, url in enumerate(input_df['URL']):
        logging.info(f"Processing {index + 1}/{len(input_df)}: {url}")
        address = get_url(url)
        data.append({'URL': url, 'Address': address})
    
    # Creating a DataFrame
    output_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    output_df.to_csv(output_csv, index=False)
    logging.info(f"Results saved to {output_csv}")

    return output_df

# Example usage
input_csv = 'ASC_input.csv'  
output_csv = 'ASC_output.csv' 

result_df = process_urls_from_csv(input_csv, output_csv)
