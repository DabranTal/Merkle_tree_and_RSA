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
        self.is_finished = False
        self.children_counter = 0

    def update_node_val(self):
        if self.left and self.right:
            con = self.left.val + self.right.val
            #self.val = hashlib.sha256(con.encode('utf-8'))
            self.val = con


    def upgrade_parents(self):
        if self:
            self.update_node_val()
            if self.parent:
                self.parent.upgrade_parents()

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
            new_parent.children_counter = new_parent.left.children_counter + new_parent.left.children_counter + 2
            # return the new root
            return new_parent
        # case leaf need to be added below
        else:
            insert_here = find_where_insert(self.right)
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
            new_parent.children_counter = new_parent.left.children_counter + new_parent.left.children_counter + 2
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
        if node.parent.left.is_leaf():
            tmp_node = node
            while tmp_node.parent:
                if not tmp_node.parent.is_finished:
                    return tmp_node.parent
                tmp_node = tmp_node.parent
        else:
            return node
    else:
        return find_where_insert(node.right)


def update_is_finished(node):
    if node.left:
        update_is_finished(node.left)
    if node.right:
        update_is_finished(node.right)
    if node.children_counter == pow(node.children_counter, node.height + 1) - 2:
        node.is_finished = True


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
            update_is_finished(root)
        if command == '2':
            just_test_print(root)

        if command == '3':
            root = Node('a', 0)
            root = root.add_node("b")
            root.update_is_complete()
            root = root.add_node("c")
            root.update_is_complete()
            root = root.add_node("d")
            root.update_is_complete()
            root = root.add_node("e")
            root.update_is_complete()
            root = root.add_node("f")
            root.update_is_complete()
            root = root.add_node("g")
            root.update_is_complete()
            root = root.add_node("h")
            root.update_is_complete()
            root = root.add_node("i")
            root.update_is_complete()
            root = root.add_node("j")
            root.update_is_complete()
            root = root.add_node("k")
            root.update_is_complete()
            root = root.add_node("l")
            root.update_is_complete()
            root = root.add_node("m")
            root.update_is_complete()
            root = root.add_node("n")
            update_is_finished(root)
            root = root.add_node("o")
            root.update_is_complete()
            root = root.add_node("p")
            root.update_is_complete()
            isTreeInit = True



