from math import sqrt

def z_limit(z):
    return z%6

class Kite:
    def __init__(self, kite_x, kite_y, kite_z):
        self.kite_x = kite_x
        self.kite_y = kite_y
        self.kite_z = kite_z
        
    def get_center(self):
        center_x = self.kite_x
        center_y =  self.kite_x*(sqrt(3)/3)+self.kite_y*(2*sqrt(3)/3)
                    
        return (center_x, center_y)
        
    def get_hex_points(self):
        l0 = sqrt(3)/6     # approx 0.2887
        l1 = 1/3           # aprrox 0.3333
        l2 = 0.5           # equal 0.5
        l3 = sqrt(3)/3     # approx 0.5774
        l4 = 2/3           # approx 0.6667
        center = self.get_center()
        center_x, center_y = center[0], center[1]
        
        points = [center,
                (center_x + l4, center_y),
                (center_x + l2, center_y + l0),
                (center_x + l1, center_y + l3),
                (center_x, center_y + l3),
                (center_x - l1, center_y + l3),
                (center_x - l2, center_y + l0),
                (center_x - l4, center_y),
                (center_x - l2, center_y - l0),
                (center_x - l1, center_y - l3),
                (center_x, center_y - l3),
                (center_x + l1, center_y - l3),
                (center_x + l2, center_y - l0),
                  ]
        return points
    
    def get_coordinates(self):
        points = self.get_hex_points()
        coordinates = []
        
        if self.kite_z == 0:
            coordinates.append(points[0])
            coordinates.append(points[12])
            coordinates.append(points[1])
            coordinates.append(points[2])        
        elif self.kite_z == 1:
            coordinates.append(points[0])
            coordinates.append(points[2])
            coordinates.append(points[3])
            coordinates.append(points[4])  
        elif self.kite_z == 2:
            coordinates.append(points[0])
            coordinates.append(points[4])
            coordinates.append(points[5])
            coordinates.append(points[6])
        elif self.kite_z == 3:
            coordinates.append(points[0])
            coordinates.append(points[6])
            coordinates.append(points[7])
            coordinates.append(points[8])
        elif self.kite_z == 4:
            coordinates.append(points[0])
            coordinates.append(points[8])
            coordinates.append(points[9])
            coordinates.append(points[10])
        elif self.kite_z == 5:
            coordinates.append(points[0])
            coordinates.append(points[10])
            coordinates.append(points[11])
            coordinates.append(points[12])
            
        return coordinates

    def get_neighbor(self, all = False):
        neighbor = []
        x,y,z = self.kite_x, self.kite_y, self.kite_z
        
        if all == True:
            neighbor.append((x,y,z))
        
        if z == 0:
            neighbor.append((x+1, y-1, 2))
            neighbor.append((x+1, y, 4))
        elif z == 1:
            neighbor.append((x+1, y, 3))
            neighbor.append((x, y+1, 5))
        elif z == 2:
            neighbor.append((x, y+1, 4))
            neighbor.append((x-1, y+1, 0))

        elif z == 3:
            neighbor.append((x-1, y+1, 5))
            neighbor.append((x-1, y, 1))
            
        elif z == 4:
            neighbor.append((x-1, y, 0))
            neighbor.append((x, y-1, 2))
            
        elif z == 5:
            neighbor.append((x, y-1, 1))
            neighbor.append((x+1, y-1, 3))
            
        return neighbor
    
    
    

