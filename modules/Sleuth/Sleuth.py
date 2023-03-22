from modules.SNCF_API import sncfAPI
import yaml

class Sleuth():
    def __init__(self, configuration_file: str):
        self.configuration_file = configuration_file
        self.update_configuration_file()
        # self.origin = origin 
        # self.destination = destination 
        # self.departure_date = departure_date 
        #self.trainRequest = sncfAPI.TrainRequest(self.origin, self.destination, self.departure_date)

    def update_configuration_file(self):
        with open(self.configuration_file) as file:
            try:
                databaseConfig = yaml.safe_load(file)   
                print(databaseConfig)
            except yaml.YAMLError as exc:
                print(exc)