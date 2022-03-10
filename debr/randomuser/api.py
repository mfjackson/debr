import pandas as pd
import requests


class RandomUser:
    """A class used to instantiate an object that can return JSON from randomuser.me"""
    def __init__(self, response_format="json", number_of_records=500):
        self.format = response_format
        self.base_url = f"https://randomuser.me/api/?results={str(number_of_records)}"
        self.headers = {"accept": "application/json"}

    def __get_data(self, url):
        """Uses the `requests` library to get JSON response from a given URL"""
        return self.__to_format(requests.get(url, headers=self.headers)).get("results")

    def __get_metadata(self, url):
        """Gets the metadata from randomusers, i.e. information returned in the JSON repsponse's `info` attribute"""
        return self.__to_format(requests.get(url, headers=self.headers)).get("info")

    def __to_format(self, response):
        """Formats the returned data."""
        if self.format == "json":
            return response.json()
        else:
            raise Exception("JSON is currently the only supported output type")

    def get_data_as_df(self):
        df = pd.json_normalize(self.__get_data(self.base_url))  # Flattening the JSON data
        df.columns = [col.replace(".", "_") for col in df.columns]  # replacing periods with underscores
        return df
