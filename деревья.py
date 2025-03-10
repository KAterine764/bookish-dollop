class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class AVLNode(TreeNode):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1

#симметричный обход
def inorder_traversal(node):
    if node:
        inorder_traversal(node.left)
        print(node.key, end=' ')
        inorder_traversal(node.right)

#прямой обход
def preorder_traversal(node):
    if node:
        print(node.key, end=' ')
        preorder_traversal(node.left)
        preorder_traversal(node.right)

#обратный обход
def postorder_traversal(node):
    if node:
        postorder_traversal(node.left)
        postorder_traversal(node.right)
        print(node.key, end=' ')

def parse_tree(expression):
    stack = []
    current = None
    open_brackets = []

    i = 0
    while i < len(expression):
        char = expression[i]
        if char == '(':
            open_brackets.append(char)
            stack.append(current)
            current = None
        elif char == ')':
            if not open_brackets:
                raise ValueError("Unmatched closing bracket")
            open_brackets.pop()
            if stack:
                parent = stack.pop()
                if parent:
                    if not parent.left:
                        parent.left = current
                    else:
                        parent.right = current
                    current = parent
        elif char.isdigit():
            num = 0
            while i < len(expression) and expression[i].isdigit():
                num = num * 10 + int(expression[i])
                i += 1
            i -= 1
            if current is None:
                current = TreeNode(num)
            else:
                if not current.left:
                    current.left = TreeNode(num)
                else:
                    current.right = TreeNode(num)
        elif char not in ' ()':
            raise ValueError(f"Invalid character: {char}")
        i += 1

    if open_brackets:
        raise ValueError("Unmatched opening bracket")

    return current

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

#вставка нового узла с ключом
    def insert_node(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self.insert_node(node.left, key)
        else:
            node.right = self.insert_node(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node
#вставка ключа
    def insert(self, key):
        if not self.root:
            self.root = AVLNode(key)
        else:
            self.root = self.insert_node(self.root, key)

    def min_value_node(self, node):
            current = node
            while current.left is not None:
                current = current.left
            return current
#удаляет узел с ключом
    def delete_node(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, key):
        self.root = self.delete_node(self.root, key)

    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

#обход в ширину
    def level_order_traversal(self):
        if not self.root:
            return
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=' ')
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

def main():
    # Чтение скобочной записи из файла
    with open('tree_expression.txt', 'r') as file:
        expression = file.read().strip()

    try:
        # Парсинг дерева
        root = parse_tree(expression)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Создание АВЛ-дерева из обычного дерева
    avl_tree = AVLTree()
    def insert_from_tree(node):
        if node:
            avl_tree.insert(node.key)
            insert_from_tree(node.left)
            insert_from_tree(node.right)

    insert_from_tree(root)

    # Вывод всех узлов 4 способами: в ширину и 3 в глубину
    print("Level Order Traversal:")
    avl_tree.level_order_traversal()
    print("\nInorder Traversal:")
    inorder_traversal(avl_tree.root)
    print("\nPreorder Traversal:")
    preorder_traversal(avl_tree.root)
    print("\nPostorder Traversal:")
    postorder_traversal(avl_tree.root)

main()