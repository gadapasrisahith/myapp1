class ProductNode:
    def __init__(self, id, name, stock, location):
        self.id = int(id)
        self.name = name
        self.stock = int(stock)
        self.location = location
        self.left_child = None
        self.right_child = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, id, name, stock, location):
        new_product = ProductNode(id, name, stock, location)
        
        if self.root is None:
            self.root = new_product
            return True # <--- SUCCESS: Added first item

        current_node = self.root
        while True:
            if new_product.id < current_node.id:
                if current_node.left_child is None:
                    current_node.left_child = new_product
                    return True # <--- SUCCESS: Added to left
                else:
                    current_node = current_node.left_child
            elif new_product.id > current_node.id:
                if current_node.right_child is None:
                    current_node.right_child = new_product
                    return True # <--- SUCCESS: Added to right
                else:
                    current_node = current_node.right_child
            else:
                # Rule: If ID already exists, STOP. Do not add.
                return False # <--- FAIL: Duplicate found!

    def find_product(self, id):
        try:
            id = int(id)
        except:
            return None
            
        if self.root is None:
            return None

        current_node = self.root
        while current_node is not None:
            if id == current_node.id:
                return current_node
            elif id < current_node.id:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child
        return None

    def get_all_products(self):
        results = []
        self._inorder_traversal(self.root, results)
        return results

    def _inorder_traversal(self, node, results):
        if node is not None:
            self._inorder_traversal(node.left_child, results)
            results.append(node)
            self._inorder_traversal(node.right_child, results)