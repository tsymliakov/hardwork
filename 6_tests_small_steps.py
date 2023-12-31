"""
Из этого занятия я вынес следующее:
1) Тесты необходимы;
2) Комитить код можно только, если все тесты пройдены,
в ином случае- следует избавляться от написанного кода;
3) Чтобы не было жалко избавляться от кода- следует вести разработку малыми шагами.

Причем ведение разработки малыми шагами катастрофически важно!

На интуитивном уровне я это понимал и успешно применял этот подход при работе
над курсами по алгоритмам и структурам данных.
"""


# Часть тестов для алгоритма обхода графа в ширину

def test_wide_empty():
    tree = BST(None)
    assert tree.WideAllNodes() == ()


def test_wide_only_root():
    root = BSTNode(10, 1, None)
    tree = BST(root)
    assert tree.WideAllNodes() == (root,)


# Тесты для алгоритма обхода графа в глубину

def test_deep_in_order_empty():
    tree = BST(None)
    assert tree.DeepAllNodes(0) == ()


def test_deep_in_order_root():
    root = BSTNode(10, 1, None)
    tree = BST(root)
    assert tree.DeepAllNodes(0) == (root,)
