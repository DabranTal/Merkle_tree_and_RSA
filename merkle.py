import hashlib
import base64
import textwrap

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

leaves_array = []
proof_of_inclusion = []


class Node:
    def __init__(self, val, height):
        self.val = hashlib.sha256(val.encode('utf-8'))
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


# insert node to tree
def add_node(current_root, val):
    insert_here = where_insert(current_root)
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
    current_root.update_is_finished()
    new_parent.upgrade_parents()
    if new_parent.parent:
        return current_root
    else:
        return new_parent


# insert node where he dont pain the subs-tree's completeness
def where_insert(node):
    if node.left and node.right:
        if node.left.children_counter == node.right.children_counter:
            return node
    if node.is_leaf():
        return node
    return where_insert(node.right)


# insert leaves to array
def get_leaves_array(current_node):
    if current_node.is_leaf():
        leaves_array.append(current_node)
    if current_node.left:
        get_leaves_array(current_node.left)
    if current_node.right:
        get_leaves_array(current_node.right)


# insert leaves to array
def get_proof_of_inclusion(current_node, direct):
    proof_of_inclusion.append((direct, current_node))
    parent_node = current_node.parent
    # case we already have brother to add the inclusion
    if parent_node.parent:
        if parent_node.parent.left == parent_node:
            if parent_node.parent.right:
                get_proof_of_inclusion(parent_node.parent.right, '1')
        else:
            get_proof_of_inclusion(parent_node.parent.left, '0')


def findPublicAndPrivateKeys():
    alg = serialization.NoEncryption()
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    private_key_hex = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=alg).decode()
    public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    print(private_key_hex)
    print(public_key_hex)


def signatureOnRoot(key, current_root):
    root_val = current_root.val.hexdigest()
    root_bytes = root_val.encode('utf-8')
    realSignature = key.sign(root_bytes, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                         hashes.SHA256())
    signature = base64.b64encode(key.sign(root_bytes, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                         hashes.SHA256())).decode()
    print(signature)


def verification(key, signatureInBytes, message):
    message = message.encode()
    try:
        key.verify(
            signatureInBytes,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(True)
    except:
        print(False)


def getInput(key):
    v = input()
    while(v != ""):
        key += v
        key += "\n"
        v = input()
    return key


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

        # -1- Add node
        if command == '1':
            # check if tree initialized
            if not isTreeInit and extra is not None:
                root = Node(extra, 0)
                isTreeInit = True
            # case the tree initialized
            elif extra is not None:
                root = add_node(root, extra)
            root.update_is_finished()
        # -2- Print root
        elif command == '2':
            if root and not extra:
                root.print_node()
            else:
                print("")
        # -3- Proof of Inclusion
        elif command == '3':
            if extra:
                if extra.__contains__(" "):
                    print("")
                    continue
                get_leaves_array(root)
                if leaves_array[int(extra)]:
                    leaf = leaves_array[int(extra)]
                    # proof_of_inclusion.append(leaf)
                    if leaf.parent:
                        if leaf.parent.left == leaf:
                            if leaf.parent.right:
                                get_proof_of_inclusion(leaf.parent.right, '1')
                        else:
                            get_proof_of_inclusion(leaf.parent.left, '0')
                    root.print_node()
                    for s in proof_of_inclusion:
                        print(s[0], end='')
                        s[1].print_node()
                leaves_array = []
                proof_of_inclusion = []
            else:
                print("")
        # -4- Check Proof of Inclusion
        elif command == '4':
            if extra.__contains__(" "):
                result, rest = extra.split(" ", 1)
                if result:
                    result = hashlib.sha256(result.encode('utf-8'))
                    if rest.__contains__(" "):
                        # extract root from solution
                        check_root, rest = rest.split(" ", 1)
                        if rest.__contains__(" "):
                            # extract evidence
                            inc, rest = rest.split(" ", 1)
                            while inc:
                                if inc[0] == '1':
                                    inc = inc[1:len(inc)]
                                    tmp_string = (result.hexdigest() + inc)
                                else:
                                    inc = inc[1:len(inc)]
                                    tmp_string = (inc + result.hexdigest())
                                result = hashlib.sha256(tmp_string.encode('utf-8'))
                                if rest is None:
                                    inc = None
                                elif rest.__contains__(" "):
                                    inc, rest = rest.split(" ", 1)
                                else:
                                    inc = rest
                                    rest = None
                            if result.hexdigest() == check_root:
                                print(True)
                            else:
                                print(False)
        # -5- Generate public and private key
        elif command == "5":
            findPublicAndPrivateKeys()
        # -6- signature on the root with the private key
        elif command == "6":
            key = extra
            key += "\n"
            key = getInput(key)
            jKey = textwrap.dedent(key).encode()
            oKey = load_pem_private_key(jKey, password=None, backend=default_backend())
            signatureOnRoot(oKey, root)
        # -7- certificate the signature for the root
        elif command == "7":
            key = extra
            key += "\n"
            key = getInput(key)
            jKey = textwrap.dedent(key).encode()
            oKey = load_pem_public_key(jKey, backend=default_backend())
            anInput = input()
            signature, verText = anInput.split()
            signatureInBytes = base64.decodebytes(bytes(signature, "utf-8"))
            verification(oKey, signatureInBytes, verText)
        # un-care command
        else:
            if command != '':
                print("")

