# A simple example was added in the end in order to show the implementation
class AVLTree:
    def __init__(self, comparator):
        self.root = None
        self.compare = comparator
    
    def insert(self, key, obj):
        new_node = Node(key, obj)
        self.root = self._insert(self.root, new_node)
    
    def _insert(self, root, new_node):
        if not root:
            return new_node
        if self.compare(new_node, root) < 0:
            root.left = self._insert(root.left, new_node)
        else:
            root.right = self._insert(root.right, new_node)
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        return self._balance(root)
    
    def delete(self, key):
        temp_node = Node(key)
        self.root = self._delete(self.root, temp_node)

    def _delete(self, node, temp_node):
        if not node:
            return node
        if self.compare(temp_node, node) < 0:
            node.left = self._delete(node.left, temp_node)
        elif self.compare(temp_node, node) > 0:
            node.right = self._delete(node.right, temp_node)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.obj = temp.obj
            node.right = self._delete(node.right, temp)
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return None
        if key < node.key:
            return self._search(node.left, key)
        elif key > node.key:
            return self._search(node.right, key)
        elif key == node.key:
            return node.obj
        else:
            raise ValueError()
    
    def _get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def _get_height(self, node):
        if not node:
            return 0
        return 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _balance(self, node):
        balance = self._get_balance(node)
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        return y

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        return y

    def in_order(self):
        return self._in_order(self.root)

    def _in_order(self, node):
        result = []
        if node:
            result.extend(self._in_order(node.left))
            result.append(node.key)
            result.extend(self._in_order(node.right))
        return result

class GCMS:
    def __init__(self):
        self.bins_by_capacity = AVLTree(self._compare_bin_capacity)
        self.bins_by_id = AVLTree(self._compare_id)
        self.find_bin = AVLTree(self._compare_id)

    def _compare_id(self, node1, node2):
        if node1 is None and node2 is None:
          return 0
        elif node2 is None:
            return 1
        elif node1 is None:
            return -1
        elif node1.key > node2.key:
            return 1
        else:
            return -1

    def _compare_bin_capacity(self, node1, node2):
        if node1 is None and node2 is None:
          return 0
        elif node2 is None:
            return 1
        elif node1 is None:
            return -1
        return (node1.key > node2.key) - (node1.key < node2.key)

    def add_bin(self, bin_id, capacity):
        if bin_id is None or capacity is None:
            raise ValueError
        new_bin = Bin(bin_id, capacity)
        self.bins_by_capacity.insert((new_bin.remaining_capacity, bin_id), new_bin)
        self.bins_by_id.insert(bin_id, new_bin)

    def add_object(self, object_id, size, color):
        new_obj = Object(object_id, size, color)
        if object_id is None or size is None or color is None:
            raise ValueError()
        best_bin = None
        best_fit_capacity = None
        best_bin_id = None
        def RED(node, size):
            nonlocal best_bin, best_fit_capacity, best_bin_id
            if node is None:
                return
            RED(node.right, size)
            cap, bin_id = node.key
            if cap >= size:
                if best_bin is None or cap > best_fit_capacity or (
                    cap == best_fit_capacity and
                    (bin_id < best_bin_id)):
                    best_bin = node.obj
                    best_fit_capacity = cap
                    best_bin_id = bin_id
            RED(node.left, size)
        
        def GREEN(node, size):
            nonlocal best_bin, best_fit_capacity, best_bin_id
            if node is None:
                return
            GREEN(node.right, size)
            cap, bin_id = node.key
            if cap >= size:
                if best_bin is None or cap > best_fit_capacity or (
                    cap == best_fit_capacity and
                    (bin_id > best_bin_id)):
                    best_bin = node.obj
                    best_fit_capacity = cap
                    best_bin_id = bin_id
            GREEN(node.left, size)
        
        def BLUE(node, size):
            nonlocal best_bin, best_fit_capacity, best_bin_id
            if node is None:
                return
            BLUE(node.left, size)
            cap, bin_id = node.key
            if cap >= size:
                if best_bin is None or cap < best_fit_capacity or (
                    cap == best_fit_capacity and 
                        (bin_id < best_bin_id)):
                    best_bin = node.obj
                    best_fit_capacity = cap
                    best_bin_id = bin_id
            BLUE(node.right, size)
        
        def YELLOW(node, size):
            nonlocal best_bin, best_fit_capacity, best_bin_id
            if node is None:
                return            
            YELLOW(node.left, size)
            cap, bin_id = node.key
            if cap >= size:
                if best_bin is None or cap < best_fit_capacity or (
                    cap == best_fit_capacity and 
                        (bin_id > best_bin_id)):
                    best_bin = node.obj
                    best_fit_capacity = cap
                    best_bin_id = bin_id
            YELLOW(node.right, size)
        if color == Color.RED:
            RED(self.bins_by_capacity.root, size)
        elif color == Color.GREEN:
            GREEN(self.bins_by_capacity.root, size)
        elif color == Color.BLUE:
            BLUE(self.bins_by_capacity.root, size)
        elif color == Color.YELLOW:
            YELLOW(self.bins_by_capacity.root, size)
        
        if best_bin is None:
            raise NoBinFoundException()
        else:
            initial_capacity = best_bin.remaining_capacity
            best_bin.add_object(new_obj)
            self.find_bin.insert(object_id, best_bin.bin_id)
            self.bins_by_capacity.delete((initial_capacity, best_bin.bin_id))
            new_key = (best_bin.remaining_capacity, best_bin.bin_id)
            self.bins_by_capacity.insert(new_key, best_bin)

    def delete_object(self, object_id):
        if object_id is None:
            raise ValueError()
        bin_id = self.find_bin.search(object_id)
        if bin_id is None:
            raise NoBinFoundException()
        
        bin_obj = self.bins_by_id.search(bin_id)
        bin_obj.remove_object(object_id)
        self.find_bin.delete(object_id)
        self.bins_by_capacity.delete((bin_obj.remaining_capacity, bin_obj.bin_id))
        self.bins_by_capacity.insert((bin_obj.remaining_capacity, bin_obj.bin_id), bin_obj)

    def bin_info(self, bin_id):
        req_bin = self.bins_by_id.search(bin_id)
        if req_bin is None:
            raise NoBinFoundException()
        return req_bin.remaining_capacity, req_bin.objects_tree.in_order()

    def object_info(self, object_id):
        bin_id = self.find_bin.search(object_id)
        return bin_id
        

        
class NoBinFoundException(Exception):
    def __init__(self):
        super().__init__("No Bin found to store the given object")
from enum import Enum

class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4
    

class Object:
    def __init__(self, object_id, size, color):
        self.object_id  = object_id
        self.size = size
        self.colour = color
class Node:
    
    def __init__(self,key,val=None):
        self.key = key
        self.obj = val
        self.left, self.right = None, None
        self.height = 1

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id, self.capacity, self.remaining_capacity = bin_id, capacity, capacity
        self.objects_tree = AVLTree(self._compare_objects)

    def _compare_objects(self, node1, node2):
        if node1 is None and node2 is None:
          return 0
        elif node2 is None:
            return 1
        elif node1 is None:
            return -1
        return (node1.key > node2.key) - (node1.key < node2.key)

    def add_object(self, obj):
        self.objects_tree.insert(obj.object_id, obj)
        self.remaining_capacity -= obj.size

    def remove_object(self, object_id):
        obj = self.objects_tree.search(object_id)
        self.objects_tree.delete(object_id)
        self.remaining_capacity += obj.size
        return obj.size
        

        
class NoBinFoundException(Exception):
    def __init__(self):
        super().__init__("No Bin found to store the given object")
from enum import Enum

class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4
    

class Object:
    def __init__(self, object_id, size, color):
        self.object_id  = object_id
        self.size = size
        self.colour = color
class Node:
    
    def __init__(self,key,val=None):
        self.key = key
        self.obj = val
        self.left, self.right = None, None
        self.height = 1

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id, self.capacity, self.remaining_capacity = bin_id, capacity, capacity
        self.objects_tree = AVLTree(self._compare_objects)

    def _compare_objects(self, node1, node2):
        if node1 is None and node2 is None:
          return 0
        elif node2 is None:
            return 1
        elif node1 is None:
            return -1
        return (node1.key > node2.key) - (node1.key < node2.key)

    def add_object(self, obj):
        self.objects_tree.insert(obj.object_id, obj)
        self.remaining_capacity -= obj.size

    def remove_object(self, object_id):
        obj = self.objects_tree.search(object_id)
        self.objects_tree.delete(object_id)
        self.remaining_capacity += obj.size
        return obj.size


def print_separator():
    print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    # Initialize GCMS
    gcms = GCMS()
    
    # Adding an initial set of bins with varying capacities
    initial_bin_data = [
        (1001, 50),
        (1002, 30),
        (1003, 40),
        (1004, 25),
        (1005, 35),
        (1006, 60),
        (1007, 45),
        (1008, 55),
        (1009, 20),
        (1010, 70)
    ]
    
    print("Adding Initial Bins:")
    for bin_id, capacity in initial_bin_data:
        gcms.add_bin(bin_id, capacity)
        print(f"Added Bin ID: {bin_id}, Capacity: {capacity}")
    
    print_separator()
    
    # Adding an initial set of objects with varying sizes and colors
    initial_object_data = [
        (2001, 20, Color.RED),
        (2002, 15, Color.YELLOW),
        (2003, 10, Color.BLUE),
        (2004, 25, Color.GREEN),
        (2005, 30, Color.RED),
        (2006, 5, Color.YELLOW),
        (2007, 8, Color.BLUE),
        (2008, 22, Color.GREEN),
        (2009, 35, Color.BLUE),
        (2010, 40, Color.RED),
        (2011, 12, Color.YELLOW),
        (2012, 18, Color.GREEN),
        (2013, 7, Color.BLUE),
        (2014, 28, Color.RED),
        (2015, 16, Color.YELLOW)
    ]
    
    print("Adding Initial Objects:")
    for obj_id, size, color in initial_object_data:
        try:
            gcms.add_object(obj_id, size, color)
            print(f"Added Object ID: {obj_id}, Size: {size}, Color: {color.name}")
        except NoBinFoundException:
            print(f"Failed to add Object ID: {obj_id}, Size: {size}, Color: {color.name} - No suitable bin found")
    
    print_separator()
    
    # Displaying bin information after initial additions
    print("Bin Information After Adding Initial Objects:")
    for bin_id, _ in initial_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    # Displaying object information after initial additions
    print("Object Information After Adding Initial Objects:")
    for obj_id, _, _ in initial_object_data:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Error retrieving info for Object ID: {obj_id} - {str(e)}")
    
    print_separator()
    
    # Adding additional bins after some objects have been placed
    additional_bin_data = [
        (1011, 65),
        (1012, 45),
        (1013, 55)
    ]
    
    print("Adding Additional Bins:")
    for bin_id, capacity in additional_bin_data:
        gcms.add_bin(bin_id, capacity)
        print(f"Added Bin ID: {bin_id}, Capacity: {capacity}")
    
    print_separator()
    
    # Adding additional objects after new bins have been added
    additional_object_data = [
        (2016, 25, Color.GREEN),
        (2017, 14, Color.YELLOW),
        (2018, 9, Color.BLUE),
        (2019, 50, Color.RED),
        (2020, 33, Color.YELLOW),
        (2021, 12, Color.GREEN),
        (2022, 7, Color.BLUE),
        (2023, 19, Color.RED),
        (2024, 28, Color.YELLOW),
        (2025, 11, Color.BLUE)
    ]
    
    print("Adding Additional Objects:")
    for obj_id, size, color in additional_object_data:
        try:
            gcms.add_object(obj_id, size, color)
            print(f"Added Object ID: {obj_id}, Size: {size}, Color: {color.name}")
        except NoBinFoundException:
            print(f"Failed to add Object ID: {obj_id}, Size: {size}, Color: {color.name} - No suitable bin found")
    
    print_separator()
    
    # Displaying bin information after adding additional objects
    print("Bin Information After Adding Additional Objects:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    # Displaying object information after adding additional objects
    print("Object Information After Adding Additional Objects:")
    for obj_id, _, _ in initial_object_data + additional_object_data:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Object ID: {obj_id} has been deleted or does not exist - {str(e)}")
    
    print_separator()
    
    # Deleting some objects
    objects_to_delete = [2003, 2005, 2010, 2015, 2018, 2019] 
    print("Deleting Objects:")
    for obj_id in objects_to_delete:
        try:
            gcms.delete_object(obj_id)
            print(f"Deleted Object ID: {obj_id}")
        except Exception as e:
            print(f"Failed to delete Object ID: {obj_id} - {str(e)}")
    
    print_separator()
    
    # Displaying bin information after deletions
    print("Bin Information After Deleting Objects:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()

    # Displaying object information after deletions
    print("Object Information After Deleting Objects:")
    current_items = initial_object_data + additional_object_data

    current_items = [ elt for elt, _, _ in current_items] 
    current_items = [elt for elt in current_items if elt not in objects_to_delete]
    for obj_id in current_items:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Object ID: {obj_id} has been deleted or does not exist - {str(e)}")
    
    print_separator()
    
    # Attempting to add an object that cannot fit into any bin
    print("Adding an Object That Cannot Fit into Any Bin:")
    try:
        gcms.add_object(2026, 100, Color.BLUE)
        print(f"Added Object ID: 2026, Size: 100, Color: BLUE")
    except NoBinFoundException:
        print("Failed to add Object ID: 2026, Size: 100, Color: BLUE - No suitable bin found")
    
    print_separator()
    
    # Final bin information
    print("Final Bin Information:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    print("All enhanced tests completed.")
