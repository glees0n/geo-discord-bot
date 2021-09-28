import os
import requests
import json
import googlemaps

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
        imgur = load_creds("auth/auth.yml")

        image = imgur.upload_from_path(image_path)

        return image["link"]

    def pointInPoly(x, y, poly):
        """
        http://www.ariel.com.au/a/python-point-int-poly.html
        """
        n = len(poly)
        inside = False

        p1x,p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

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