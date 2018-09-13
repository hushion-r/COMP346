import requests
import json

# author: Rae Hushion
# MetroTransit Activity
# Due Fri 7 Sept 2018


class GetInfo:
    def __init__(self):
        self.all_metro_info = CallMetroAPI()

        # establish values
        self.route = 000
        self.direction_value = 0
        self.direction_text = "0"
        self.stop_code = "0"
        self.stop_name = "0"

        # run methods
        self.get_routes()
        self.get_direction()
        self.get_stops()
        self.get_times()

    # asks user for route and checks for validity
    def get_routes(self):
        all_routes = self.all_metro_info.get_all_route_numbers()
        while self.route not in all_routes:
            self.route = input("Which bus route are you taking?")
            if self.route not in all_routes:
                print("ERROR. TRY AGAIN.")
        return self.route

    # asks user for direction and checks for validity
    def get_direction(self):
        directions = self.all_metro_info.get_which_directions(self.route)
        directions_keys = directions.keys()
        while self.direction_value not in directions_keys:
            # if SOUTH/NORTH
            if "1" in directions_keys:
                self.direction_value = input("\nWhich direction are you travelling on route "
                                             + str(self.route) + "(Enter number)"
                                             + "\n1 for Southbound"
                                             + "\n4 for Northbound")
            # if EAST/WEST
            elif "2" in directions_keys:
                self.direction_value = input("\nWhich direction are you travelling on route "
                                             + str(self.route) + "(Enter number)"
                                             + "\n2 for Eastbound"
                                             + "\n3 for Westbound")
            else:
                print("ERROR. TRY AGAIN.")
        self.direction_text = directions[self.direction_value]

    # asks user for stop and checks for validity
    def get_stops(self):
        all_stops = self.all_metro_info.get_all_stops(self.route, self.direction_value)
        print("\n")
        for i in all_stops:
            print(i + " for " + all_stops[i])
        while self.stop_code not in all_stops.keys():
            self.stop_code = input("\nWhich stop will you depart from? (Enter stop code)"
                                   " (case sensitive)")
            if self.stop_code not in all_stops.keys():
                print("ERROR. TRY AGAIN.")
        self.stop_name = all_stops[self.stop_code]

    # gives user times of next 3 departures
    def get_times(self):
        times = self.all_metro_info.get_bus_times(self.route, self.direction_value, self.stop_code)
        print("\nThe next bus for route " + str(self.route) + " " + self.direction_text
              + " at " + self.stop_name + " will arrive in/at " + times[0] + ".\n"
              + "The following buses will arrive in/at " + times[1] + " and " + times[2] + ".")


# to make requests, get json files, and process those files from MetroTransit
class CallMetroAPI:
    def __init__(self):
        self.r = requests.get('http://svc.metrotransit.org/NexTrip/Routes?format=json')

    # returns list of all routes
    def get_all_route_numbers(self):
        r = self.r.json()
        routes_list = []
        for routes in r:
            routes_list.append(routes['Route'])
        return routes_list

    # returns list of valid directions for a given route
    def get_which_directions(self, route):
        d = requests.get('http://svc.metrotransit.org/NexTrip/Directions/'
                         + str(route) + '?format=json')
        d = d.json()
        directions_dict = {}
        for directions in d:
            directions_dict[directions['Value']] = directions['Text']
        return directions_dict

    # returns list of valid stops for a given route and direction
    def get_all_stops(self, route, direction):
        s = requests.get('http://svc.metrotransit.org/NexTrip/Stops/' + str(route)
                         + '/' + str(direction) + '?format=json')
        s = s.json()
        stops_dict = {}
        for stops in s:     # makes dict with key being the stop code and value being the stop name
            stops_dict[stops["Value"]] = stops['Text']
        return stops_dict

    # returns list of next 3 scheduled departures for a given route, direction, and stop
    def get_bus_times(self, route, direction, stop):
        t = requests.get('http://svc.metrotransit.org/NexTrip/' + str(route)
                         + '/' + str(direction) + '/' + stop + '?format=json')
        t = t.json()
        times_list = []
        for index in range(3):
            times_list.append(t[index]['DepartureText'])
        return times_list


userInfo = GetInfo()
