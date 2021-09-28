import os
import json
import requests
import random

from faker import Faker
from datetime import datetime

from auth.imgur_auth import *

class StreetViewer(object):
    def __init__(self, api_key, location, size="640x640", fov="120", folder="temp/", verbose=True):
        """
        This class handles a single API request to the Google Static Street View API
        """
        self.key = api_key
        self.location = location
        self.size = size
        self.fov = fov
        self.folder = folder
        self.meta_params = dict(key=self.key, location=self.location)
        self.image_params = dict(key=self.key, location=self.location, size=self.size)
        self.verbose = verbose

    def uploadImage(self, image_path):
        """
        Uploads the generated static street view image to imgur
        """
        imgur = loadCreds("auth/auth.yml")

        image = imgur.upload_from_path(image_path)

        return image["link"]

    def storeImageData(self, answer, link):
        """
        Stores the answer and image link in a json file for later reference
        """
        data = {"answer": answer, "link": link}

        with open("streetviews/image_data.json", "w") as file:
            json.dump(data, file)

    def fetchImageMetaData(self):
        """
        Method to query the metadata of the address
        """
        self.meta_path = "{}metadata_{}.json".format(self.folder, self.location.replace(",", "_"))
        self.meta_response = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata?', params=self.meta_params)
        self.meta_info = self.meta_response.json()
        self.meta_status = self.meta_info["status"]

        if self.meta_response.ok:
            if self.verbose:
                with open(self.meta_path, 'w') as file:
                    json.dump(self.meta_info, file)

                self.meta_response.close()

    def fetchImage(self):
        """
        Method to query the StreetView picture and save to local directory
        """
        self.image_path = "{}image_{}.jpg".format(self.folder, self.location.replace(",", "_"))
        self.meta_path = "{}metadata_{}.json".format(self.folder, self.location.replace(",", "_"))

        if self.meta_status == "OK":
            if self.verbose:
                self.image_response = requests.get("https://maps.googleapis.com/maps/api/streetview?", params=self.image_params)
            if self.image_response.ok:
                with open(self.image_path, 'wb') as file:
                    file.write(self.image_response.content)

                link = self.uploadImage(self.image_path)

                self.storeImageData("Georgia", link)

                os.remove(self.image_path)
                os.remove(self.meta_path)

                self.image_response.close()
                
        return link