# Ido Tavron, 316222512, Tal Dabran, 316040898

import hashlib


class Node:
    def __init__(self, val, height):
        #self.val = hashlib.sha256(val.encode('utf-8'))
        self.val = val
        self.parent = None
        self.left = None
        self.right = None
        if height == 0:
            self.is_complete = True
        else:
            self.is_complete = False
        self.height = height

    def update_node_val(self):
        if self.left and self.right:
            con = self.left.val + self.right.val
            #self.val = hashlib.sha256(con.encode('utf-8'))
            self.val = con


    def upgrade_parents(self):
        if self:
            self.update_node_val()
            self.parent.update_node_val()

    def is_leaf(self):
        if not self.left and not self.right:
            return True
        else:
            return False

    def print_node(self):
        #print(self.val.hexdigest())
        print(self.val)


    def add_node(self, val):
        # case leaf need to be added beside
        if self.is_complete:
            right_node = Node(val, self.height)
            #new_parent = Node(self.val.hexdigest() + right_node.val.hexdigest(), self.height + 1)
            new_parent = Node(self.val + right_node.val, self.height + 1)
            new_parent.left = self
            new_parent.right = right_node
            # update parents
            self.parent = new_parent
            right_node.parent = new_parent
            if right_node.is_complete:
                new_parent.is_complete = True
            else:
                new_parent.is_complete = False
            # return the new root
            return new_parent
        # case leaf need to be added below
        else:
            insert_here = find_where_insert(self)
            if not insert_here:
                insert_here = self
            right_node = Node(val, insert_here.height - 1)
            #new_parent = Node(insert_here.val.hexdigest() + right_node.val.hexdigest(), insert_here.height)
            new_parent = Node(insert_here.val + right_node.val, insert_here.height)
            insert_here.height -= 1
            # add children to new node
            new_parent.left = insert_here
            new_parent.right = right_node
            # update parent to point node's new parent
            if insert_here.parent.left.val == insert_here.val:
                insert_here.parent.left = new_parent
            else:
                insert_here.parent.right = new_parent
            # update parents to new nodes
            new_parent.parent = insert_here.parent
            insert_here.parent = new_parent
            right_node.parent = new_parent
            # update children
            insert_here.down_grade_children()
            # return the root
            new_parent.upgrade_parents()
            return self

    # down grade all the children below change is_complete if after downgrade sub-tree became complete
    def down_grade_children(self):
        if self.is_leaf() or self.is_complete:
            return True
        le, ri = False, False
        if self.left:
            self.left.height = self.height - 1
            le = self.left.down_grade_children()
        if self.right:
            self.right.height = self.height - 1
            ri = self.right.down_grade_children()
        self.is_complete = le and ri
        return le and ri

    def update_is_complete(self):
        if self.is_complete:
            return True
        if self.height == 0:
            self.is_complete = True
            return True
        le, ri = False, False
        if self.left:
            le = self.left.update_is_complete()
        if self.right:
            ri = self.right.update_is_complete()
        if le and ri:
            self.is_complete = True
        return le and ri

# left order scanning to know where to insert the new node
def find_where_insert(node):
    if node.is_leaf():
        if not node.is_complete:
            return node
        else:
            return None
    if node.is_complete:
        return None
    left_ret = find_where_insert(node.left)
    if not left_ret:
        right_ret = find_where_insert(node.right)
        if not right_ret:
            return node
        else:
            return right_ret
    else:
        return left_ret

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
                root = root.add_node(extra)
            root.update_is_complete()
            if root.is_complete:
                a = 7

        if command == '2':
            just_test_print(root)
