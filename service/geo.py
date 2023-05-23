import requests


class OverQueryLimit(Exception):
    pass

class Geographic():
    api_queries = {
        "reverse_geocode": "https://api.geoapify.com/v1/geocode/autocomplete?text={dest_text}&bias=proximity:{origin}|countrycode:none&format=json&apiKey={apiKey}",
        "routing": "https://api.geoapify.com/v1/routing?waypoints={origin}|{dest}&mode=transit&apiKey={apiKey}",
        "isoline_map": "https://api.geoapify.com/v1/isoline?lat={origin_lat}&lon={origin_lon}&type=time&mode=approximated_transit&range=1800&apiKey={apiKey}"
    }

    geo = {
        "work": [40.75589705, -73.98927342121596]
    }

    def __init__(self, api_key: str, query_limit: int = 3000):
        self.key = api_key
        self.credits_remaining = query_limit
    
    def _check_query_limit(self, credits_needed: int):
        """
        Simple checker to determine if we have enough credits remaining
        (not very robust, since we're not saving state anywhere)
        """
        if (self.credits_remaining - credits_needed > 0):
            raise OverQueryLimit

    def get_closest_poi(self, poi_name: str, bias: list(float, float)):
        """
        reverse-geocode the name of a place of interest relative to the proximity of a pre-defined point.
        Ex. Lat/lon of closest grocery store to a new apartment
        poi_name: Plain text name of the POI
        bias: list of lat,lon coords to filter the POI
        """
        origin = ",".join([str(coord) for coord in bias])

        query_str = self.api_queries["reverse_geocode"].format(dest_text = poi_name, origin=origin, apiKey = self.key)

        try:
            self._check_query_limit(1)
            response = requests.get(query_str)
        except OverQueryLimit:
            print("Over daily query limit! Try Tomorrow or buy API usage.")

        if response.status_code == 200:
            data = response.json()
            closest_poi = data["results"][0]
            self.credits_remaining -= 1
            return closest_poi
        else:
            raise Exception(f"Error getting closest POI, {poi_name}: {response.status_code}")
    
    def get_routing(self, origin: list(float, float), dest: list(float, float)) -> dict:
        """
        Construct routing API query to return routing time from origin to dest
        """
        origin_str = ",".join([str(coord) for coord in origin])
        dest_str = ",".join([str(coord) for coord in dest])

        query_str = self.api_queries["routing"].format(origin=origin_str, dest=dest_str, apiKey=self.key)

        try:
            self._check_query_limit(1)
            response = requests.get(query_str)
        except OverQueryLimit:
            print("Over daily query limit! Try Tomorrow or buy API usage.")

        if response.status_code == 200:
            data = response.json()
            features = data["features"][0]
            travel_time = features["properties"]["time"] / 60 # In min
            travel_distance = features["properties"]["distance"]

            self.credits_remaining -= 1
            return {
                "time": travel_time,
                "distance": travel_distance,
                "legs": features["properties"]["legs"],
                "geometry": features["geometry"]
            }
        else:
            raise Exception(f"Error getting routing: {response.status_code}")

    
    def get_isoline_map(self, origin: list(float, float), time: int = 15) -> dict:
        """
        Pull Isoline map for the origin, highlighting areas reachable within x minutes
        by public transit

        NOTE: Free API version only allows 15min calculations by default
        and these cost 1 credit per 5min cone size.

        """
        query_str = self.api_queries["isoline_map"].format(origin_lat=str(origin[0]), origin_lon=str(origin[1]), time=str(time), apiKey=self.key)

        try:
            self._check_query_limit(3)
            response = requests.get(query_str)
        except OverQueryLimit:
            print("Request would be over daily query limit! Try tomorrow or buy API usage.")

        if response.status_code == 200:
            self.credits_remaining -= (time // 5)
            return response.json()
        else:
            raise Exception(f"Error getting isoline map: {response.status_code}")





