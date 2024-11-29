import json

class ObstacleMap:
    def __init__(self):
        self.list_map = self.load_map_list()
        self.list_gridsize = self.load_gridsize_list()
        
    def add_map(self, map_obstalces, grid_size):
        self.list_map.append(map_obstalces)
        self.list_gridsize.append(grid_size)
    
    def del_map(self, pos):
        self.list_map.pop(pos)
        self.list_gridsize.pop(pos)
    
    def load_map_list(self):
        """
        Return list of set, each set contains position of obstacles in tuple.
        Each set is obstacles position list of a map
        """  
        with open('assets/maps/data.json', 'r') as file:
            data_serializable = json.load(file)

        # Change data type
        data = [set(tuple(item) for item in set_item) for set_item in data_serializable]
        return data
        
    def load_gridsize_list(self):
        """
        Return list of integer, each integer is size of grid
        """  
        with open('assets/maps/sizes.json', 'r') as file:
            data = json.load(file)

        return data
    
    def save_map_list(self):
        data = self.list_map
        
        # Change data type before save
        data_serializable = [ [tuple(item) for item in set_item] for set_item in data ]

        with open('assets/maps/data.json', 'w') as file:
            json.dump(data_serializable, file)

    def save_gridsize_list(self):
        data = self.list_gridsize
        
        with open('assets/maps/sizes.json', 'w') as file:
            json.dump(data, file)
    
    def save_data(self):
        self.save_gridsize_list()
        self.save_map_list()
        
    def __del__(self):
        self.save_data()
        
        