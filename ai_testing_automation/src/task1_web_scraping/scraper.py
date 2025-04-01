from bs4 import BeautifulSoup
import requests
import json
from typing import Dict, List
import logging
from pathlib import Path
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.config import BASE_URL, ELEMENTS_JSON_PATH

class WebScraper:
    def __init__(self, url: str = BASE_URL):
        self.url = url
        self.elements: Dict[str, List[Dict]] = {
            "buttons": [],
            "links": [],
            "inputs": [],
            "forms": []
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_elements(self) -> None:
        """Extract UI elements from the webpage"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract buttons
            buttons = soup.find_all('button') + soup.find_all('input', type='button')
            for button in buttons:
                self.elements["buttons"].append({
                    "text": button.text.strip(),
                    "id": button.get('id', ''),
                    "class": button.get('class', []),
                    "type": button.get('type', '')
                })

            # Extract links
            links = soup.find_all('a')
            for link in links:
                self.elements["links"].append({
                    "text": link.text.strip(),
                    "href": link.get('href', ''),
                    "id": link.get('id', ''),
                    "class": link.get('class', [])
                })

            # Extract input fields
            inputs = soup.find_all('input')
            for input_field in inputs:
                if input_field.get('type') != 'button':
                    self.elements["inputs"].append({
                        "type": input_field.get('type', ''),
                        "name": input_field.get('name', ''),
                        "id": input_field.get('id', ''),
                        "placeholder": input_field.get('placeholder', '')
                    })

            # Extract forms
            forms = soup.find_all('form')
            for form in forms:
                self.elements["forms"].append({
                    "action": form.get('action', ''),
                    "method": form.get('method', ''),
                    "id": form.get('id', ''),
                    "inputs": [{"type": i.get('type', ''), "name": i.get('name', '')} 
                             for i in form.find_all('input')]
                })

            self.logger.info(f"Successfully extracted elements from {self.url}")

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch webpage: {str(e)}")
            raise

    def save_to_json(self, output_path: str = ELEMENTS_JSON_PATH) -> None:
        """Save extracted elements to JSON file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.elements, f, indent=4)
            self.logger.info(f"Successfully saved elements to {output_path}")
        except IOError as e:
            self.logger.error(f"Failed to save JSON file: {str(e)}")
            raise

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.extract_elements()
    scraper.save_to_json()