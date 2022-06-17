import hashlib


class Node:
    def __init__(self, val, height):
        self.val = hashlib.sha256(val.encode('utf-8'))
        # self.val = val
        self.parent = None
        self.left = None
        self.right = None
        if height == 0:
            self.is_complete = True
        else:
            self.is_complete = False
        self.height = height
        self.is_finished = False
        self.children_counter = 0

    def update_is_finished(self):
        if self.is_finished:
            return
        if self.left:
            self.left.update_is_finished()
        if self.right:
            self.right.update_is_finished()
        if self.children_counter == pow(2, self.height + 1) - 2:
            self.is_finished = True

    def downgrade_height(self):
        if self.left:
            self.left.height -= 1
            self.left.downgrade_height()
        if self.right:
            self.right.height -= 1
            self.right.downgrade_height()

    def update_node_val(self):
        if self.left and self.right:
            con = self.left.val.hexdigest() + self.right.val.hexdigest()
            self.children_counter = self.left.children_counter + self.right.children_counter + 2
            self.val = hashlib.sha256(con.encode('utf-8'))
            # self.val = con

    def is_leaf(self):
        if not self.left and not self.right:
            return True
        else:
            return False

    def upgrade_parents(self):
        if self:
            self.update_node_val()
            if self.parent:
                self.parent.upgrade_parents()

    def print_node(self):
        print(self.val.hexdigest())
        #print(self.val)

def where_insert(node):
    if node.left and node.right:
        if node.left.children_counter == node.right.children_counter:
            return node
    if node.is_leaf():
        return node
    return where_insert(node.right)


def add_node(root, val):
    insert_here = where_insert(root)
    # case we build new level
    if insert_here.is_finished:
        right_node = Node(val, insert_here.height)
        left_node = insert_here
        new_parent = Node(left_node.val.hexdigest() + right_node.val.hexdigest(), insert_here.height + 1)
    # case we downgrade levels:
    else:
        right_node = Node(val, insert_here.height - 1)
        left_node = insert_here
        left_node.height -= 1
        new_parent = Node(left_node.val.hexdigest() + right_node.val.hexdigest(), insert_here.height)
        left_node.downgrade_height()
    # update origin parent
    if insert_here.parent:
        insert_here.parent.right = new_parent
        new_parent.parent = insert_here.parent
    # update new nodes parent
    right_node.parent = new_parent
    left_node.parent = new_parent

    # update new parent children
    new_parent.left = left_node
    new_parent.right = right_node
    root.update_is_finished()
    new_parent.upgrade_parents()
    if new_parent.parent:
        return root
    else:
        return new_parent


def just_test_print(node):
    if node:
        node.print_node()
        just_test_print(node.left)
        just_test_print(node.right)


if __name__ == '__main__':
    isTreeInit = False
    root = None
    while True:
        # get user input
        value = input()

        # extract command and extra input if it is exist
        if value.__contains__(" "):
            command, extra = value.split(" ", 1)
        else:
            command = value
            extra = None

        if command == '1':
            # check if tree initialized
            if not isTreeInit and extra is not None:
                root = Node(extra, 0)
                isTreeInit = True
            # case the tree initialized
            elif extra is not None:
                root = add_node(root, extra)
            root.update_is_finished()
        if command == '2':
            just_test_print(root)

