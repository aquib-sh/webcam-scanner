import shodan
import time
import json
""" 
    SHODAN ENGINE
    COPYRIGHT(C) 2020 SHAIKH AQUIB

    THIS CLASS SIMPLIFIES THE USE OF SHODAN AND PERFORMS VARIOUS TASKS SUCH AS RESULTING THE LIST OF IP ALONG WITH PORT NUMBERS
    FOR THE SERVICES THAT MATCH THE QUERY

"""

class ShodanEngine:
    
    def __init__(self,API_KEY,query):
        self.API_KEY = API_KEY
        self.query = query
        self.__api = shodan.Shodan(self.API_KEY)
        try:
            self.__result = self.__api.search(self.query)
        except:
            time.sleep(3)
            self.__result = self.__api.search(self.query)
    
    #  Returns the dictonary of result 
    def get_search_result(self):
        return self.__result

    #  Returns a list of ip addresses along with the port number 
    #  on which the mentioned service is active
    def get_list_with_port(self):
        res = []
        for service in self.__result['matches']:
            res.append("{}:{}".format(service['ip_str'], service['port']))
        return res
    
    # Returns location list 
    def get_location_list(self):
        res = []
        for service in self.__result['matches']:
            res.append("{}, {}".format(service['location']['city'], service['location']['country_name']))
        return res

    #  Writes the above list to file
    def write_list_to_file(self, filename):
        li = self.get_list_with_port()

        f = open(filename, "w")
        for l in li:
            f.write(l+"\n")
        f.close()

    #  Writes the entire result dictonary to a txt file
    def write_result_to_json_file(self, filename):
        with open(filename,'w') as f:
            f.write(json.dump(self.__result,f))
        f.close()

    # Return the dict from json file
    def get_result_from_json_file(self, filename):
        with open(filename,'r') as f:
            data = json.load(f)
        f.close()
        return data








