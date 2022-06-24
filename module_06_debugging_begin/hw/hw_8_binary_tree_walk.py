"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional


logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                    f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                    f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)
    return queue

counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)

    node_right = get_tree(max_depth - 1, level=level + 1)

    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    with open(path_to_log_file, 'r') as file:
        val = re.findall(r"[\d]{6}", file.readline())[0]
        node = BinaryTreeNode(val, left=False, right=False)
        nodes_list = [node]
        current_node = None
        for row in file.readlines():
            if re.match(r'INFO.*', row):
                val = re.findall(r"[\d]{6}", row)[0]
                current_node = [i for i in nodes_list if i.val == val][0]
            elif re.match(r'.*left.*', row):
                val = re.findall(r"[\d]{6}", row)[1]
                if node.left is False and current_node is None:
                    node.left = BinaryTreeNode(val)
                    nodes_list.append(node.left)
                else:
                    current_node.left = BinaryTreeNode(val)
                    nodes_list.append(current_node.left)
            else:
                val = re.findall(r"[\d]{6}", row)[1]
                if node.right is False and current_node is None:
                    node.right = BinaryTreeNode(val)
                    nodes_list.append(node.right)
                else:
                    current_node.right = BinaryTreeNode(val)
                    nodes_list.append(current_node.right)
        return node

if __name__ == "__main__":
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s:%(message)s",
            filename="hw_8_walk_log_5.txt",
    )

    root = get_tree(7)
    walk(root)
    restored_root= restore_tree("hw_8_walk_log_5.txt")
    if root.__sizeof__() == restored_root.__sizeof__():
        print('Успешно восстановлено')
    else:
        print('Что-то пошло не так')