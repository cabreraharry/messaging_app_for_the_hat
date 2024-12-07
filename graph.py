import matplotlib.pyplot as plt
from kite import Kite


colors = ['blue', 'green', 'red', 'yellow', 'orange', 'purple', 'brown', 'pink']


def graph_hat(source, title, save_path=None):
    plt.figure(figsize=(12, 8))

    for group_index, group in enumerate(source):
        color = colors[group_index % len(colors)]
        
        for kite_index, item in enumerate(group):
            i, j, k = item
            new_kite = Kite(i, j, k)
            coordinates = new_kite.get_coordinates()
            
            x = [point[0] for point in coordinates]
            y = [point[1] for point in coordinates]
            
            x.append(x[0])
            y.append(y[0])
            
            # alpha_value = 1 - (kite_index / len(group))*0.5
            alpha_value = 0.5
                        
            plt.fill(x, y, color=color, alpha=alpha_value)
            
    plt.gca().set_aspect('equal', adjustable='box')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)

    plt.show()


def graph_with_value(source, title, save_path=None):

    plt.figure(figsize=(12, 8))

    for group_index, group in enumerate(source):
        color = colors[group_index % len(colors)]
        
        for kite_index, item in enumerate(group.items()):
            (i, j, k), bit = item
            new_kite = Kite(i, j, k)
            coordinates = new_kite.get_coordinates()
            
            x = [point[0] for point in coordinates]
            y = [point[1] for point in coordinates]
            
            x.append(x[0])
            y.append(y[0])
            
            alpha_value = 1 - (kite_index / len(group)) * 0.5
            
            plt.fill(x, y, color=color, alpha=alpha_value)
            
            center_x = sum(x[:-1]) / len(x[:-1])
            center_y = sum(y[:-1]) / len(y[:-1])
            
            plt.text(center_x, center_y, bit, fontsize=12, ha='center', va='center', color='black', weight='bold')
    
    plt.gca().set_aspect('equal', adjustable='box')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)

    plt.show()


def graph_with_coordinates(source, title, save_path=None):
    
    plt.figure(figsize=(12, 8))

    for group_index, group in enumerate(source):
        color = colors[group_index % len(colors)]
        
        for kite_index, item in enumerate(group.items()):
            (i, j, k), bit = item
            new_kite = Kite(i, j, k)
            coordinates = new_kite.get_coordinates()
            
            x = [point[0] for point in coordinates]
            y = [point[1] for point in coordinates]
            
            x.append(x[0])
            y.append(y[0])
            
            alpha_value = 1 - (kite_index / len(group)) * 0.8

            plt.fill(x, y, color=color, alpha=alpha_value)
            
            center_x = sum(x[:-1]) / len(x[:-1])
            center_y = sum(y[:-1]) / len(y[:-1])
            
            coord_text = f"({i}, {j}, {k})"
            plt.text(center_x, center_y, coord_text, fontsize=6, ha='center', va='center', color='black', weight='bold')
    
    plt.gca().set_aspect('equal', adjustable='box')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)

    plt.show()
    
    


def graph_with_list_coordinates(data_list, title, save_path=None):
    plt.figure(figsize=(12, 8))

    for group_index, group in enumerate(data_list):
        color = colors[group_index % len(colors)]
        
        for kite_index, (i, j, k) in enumerate(group):
            new_kite = Kite(i, j, k)
            coordinates = new_kite.get_coordinates()
            
            x = [point[0] for point in coordinates]
            y = [point[1] for point in coordinates]
            
            x.append(x[0])
            y.append(y[0])
            
            alpha_value = 1 - (kite_index / len(group)) * 0.9
            
            plt.fill(x, y, color=color, alpha=alpha_value)
            
            center_x = sum(x[:-1]) / len(x[:-1])
            center_y = sum(y[:-1]) / len(y[:-1])
            
            coord_text = f"({i}, {j}, {k})"
            plt.text(center_x, center_y, coord_text, fontsize=6, ha='center', va='center', color='black', weight='bold')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    plt.show()

order = 0
def graph_with_order(data, title, save_path=None):
    global order
    
    plt.figure(figsize=(8, 8))

    for group_index, group in enumerate(data):
        color = colors[group_index % len(colors)]
        
        for kite_index, (i, j, k) in enumerate(group):
            new_kite = Kite(i, j, k)
            coordinates = new_kite.get_coordinates()
            
            x = [point[0] for point in coordinates]
            y = [point[1] for point in coordinates]
            
            x.append(x[0])
            y.append(y[0])
            
            alpha_value = 1 - (kite_index / len(group)) * 0.5
            # alpha_value = 0.1

            plt.fill(x, y, color=color, alpha=alpha_value)
            
            center_x = sum(x[:-1]) / len(x[:-1])
            center_y = sum(y[:-1]) / len(y[:-1])
            
            coord_text = f"{order}"
            order += 1
            plt.text(center_x, center_y, coord_text, fontsize=6, ha='center', va='center', color='black', weight='bold')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    plt.show()


order1D = 0
def graph_1D_with_order(data, title, save_path=None):
    global order1D
    
    plt.figure(figsize=(8, 8))

        
    for kite_index, (i, j, k) in enumerate(data):
        color = colors[0]
        new_kite = Kite(i, j, k)
        coordinates = new_kite.get_coordinates()
        
        x = [point[0] for point in coordinates]
        y = [point[1] for point in coordinates]
        
        x.append(x[0])
        y.append(y[0])
        
        alpha_value = 1 - (kite_index / len(data)) * 0.9
        # alpha_value = 0.1

        plt.fill(x, y, color=color, alpha=alpha_value)
        
        center_x = sum(x[:-1]) / len(x[:-1])
        center_y = sum(y[:-1]) / len(y[:-1])
        
        coord_text = f"{order1D}"
        order1D += 1
        plt.text(center_x, center_y, coord_text, fontsize=6, ha='center', va='center', color='black', weight='bold')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    plt.show()