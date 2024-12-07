from kite import z_limit

class Hat:
    def __init__(self, head, is_flipped = False):
        self.head = head
        self.is_flipped = is_flipped
        
    def getKites(self):
        kites = [self.head]
        if not self.is_flipped:
            kites.append([self.head[0],self.head[1],z_limit(self.head[2]+1)])
            
    def generate_hat(kite, position):
        hat_list = []
        if position == 0:
            hat_list.append(kite)
            hat_list.append((kite[0], kite[1], z_limit(kite[2]+1)))
            hat_list.append((kite[0], kite[1], z_limit(kite[2]+2)))
            hat_list.append((kite[0], kite[1], z_limit(kite[2]+3)))

        
            
# TRANSFORMATION
def translate(array, position=0):
    
    '''
    Translation guide
            2
        3        1
            0
        4       6
            5
    
    '''
    result = []
    for sublist in array:
        new_sublist = []
        for j in sublist:
            coords = list(j)
            
            if position == 1:
                coords[0] += 1
                
            if position == 2:
                coords[1] += 1
                
            if position == 3:
                coords[1] += 1
                coords[0] -= 1
                
            if position == 4:
                coords[0] -= 1
                
            if position == 5:
                coords[1] -= 1
                
            if position == 6:
                coords[1] -= 1
                coords[0] += 1
                
            new_sublist.append(tuple(coords))
        result.append(new_sublist)
    return result


def rotate(array, angle):
    for i in array:
        pass

def reflect(array, direction = "horizontal"):
    result = []
    new_z = [3, 2, 1, 0, 5, 4]
    for sublist in array:
        new_sublist = []
        for j in sublist:
            coords = list(j)
            
            if direction == 0:
                coords[0] = coords[0]*-1
                coords[1] = coords[1]+(-1*coords[0])
                coords[2] = new_z[coords[2]]
                
            if direction == 1:
                pass
                
            new_sublist.append(tuple(coords))
        result.append(new_sublist)
    return result

def rotate(array, angle_index):
    
    if angle_index > 5:
        angle_index = angle_index % 6
        
    result = []
    angles = [60, 120, 180, 240, 300, 360]
    for sublist in array:
        new_sublist = []
        for j in sublist:
            coords = list(j)
            
            x, y = coords[0], coords[1]
            
            angle = angles[angle_index]
            
            if angle == 60:
                coords[0], coords[1] = -y, x + y
            elif angle == 120:
                coords[0], coords[1] = -x - y, x
            elif angle == 180:
                coords[0], coords[1] = -x, -y
            elif angle == 240:
                coords[0], coords[1] = y, -x - y
            elif angle == 300:
                coords[0], coords[1] = x+y, -x
            else:
                return array
            
            coords[2] = z_limit(coords[2]+angle_index+1)
                
            new_sublist.append(tuple(coords))
        result.append(new_sublist)
    return result


