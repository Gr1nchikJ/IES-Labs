import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url
   
    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        try:
            # Convert the processed data batch to JSON
            processed_data_json = []
            for processed_data in processed_agent_data_batch:
                agent_data_dict = processed_data.agent_data.dict()
                # Convert timestamp to ISO format string
                agent_data_dict['timestamp'] = agent_data_dict['timestamp'].isoformat()
                processed_data_dict = processed_data.dict()
                processed_data_dict['agent_data'] = agent_data_dict
                processed_data_json.append(processed_data_dict)
            
            # Make a POST request to the Store API endpoint
            response = requests.post(
                f"{self.api_base_url}/processed_agent_data",
                json=processed_data_json
            )

            # Check if the request was successful
            if response.status_code == 200:
                logging.info("Processed data saved successfully.")
                return True
            else:
                logging.error(f"Failed to save processed data. Status code: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"An error occurred while saving processed data: {e}")
            return False