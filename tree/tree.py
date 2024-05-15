"""
Modul sadrži implementaciju stabla.
"""
from queue import Queue


class TreeNode(object):
    """
    Klasa modeluje čvor stabla.
    """
    __slots__ = 'parent', 'children', 'data'

    def __init__(self, data):
        """
        Konstruktor.

        Argument:
        - `data`: podatak koji se upisuje u čvor
        """
        self.parent = None
        self.children = []
        self.data = data

    def is_root(self):
        """
        Metoda proverava da li je čvor koren stabla.
        """
        return self.parent is None

    def is_leaf(self):
        """
        Metoda proverava da li je čvor list stabla.
        """
        return len(self.children) == 0

    def add_child(self, node):
        """
        Metoda dodaje potomka čvoru.

        Argument:
        - `x`: čvor potomak
        """
        # kreiranje dvosmerne veze između čvorova
        node.parent = self
        self.children.append(node)


class Tree(object):
    """
    Klasa modeluje stablo.
    """
    def __init__(self):
        self.root = None

    def is_empty(self):
        """
        Metoda proverava da li stablo ima elemenata.
        """
        return self.root is None

    def depth(self, node):
        """
        Metoda izračunava dubinu zadatog čvora.

        Argument:
        - `x`: čvor čija dubina se računa
        """
        if node.is_root():
            return 0
        else:
            return 1 + self.depth(node.parent)

    def _height(self, node):
        """
        Metoda izračunava visinu podstabla sa zadatim korenom.

        Argument:
        - `x`: koren posmatranog podstabla
        """
        if node.is_leaf():
            return 0
        else:
            return 1 + max(self._height(child) for child in node.children)

    def height(self):
        return self._height(self.root)

    def preorder(self, node):
        """
        Preorder obilazak po dubini

        Najpre se vrši obilazak roditelja a zatim svih njegovih potomaka.

        Argument:
        - `x`: čvor od koga počinje obilazak
        """
        if not self.is_empty():
            print(node.data)
            for child in node.children:
                self.preorder(child)

    def postorder(self, node):
        """
        Postorder obilazak po dubini

        Najpre se vrši obilazak potomaka a zatim i roditelja

        Argument:
        - `x`: čvor od koga počinje obilazak
        """
        if not self.is_empty():
            for child in node.children:
                self.postorder(child)
            print(node.data)

    def breadth_first(self):
        """
        Metoda vrši obilazak stabla po širini.
        """
        to_visit = Queue()
        to_visit.enqueue(self.root)
        while not to_visit.is_empty():
            e = to_visit.dequeue()
            print(e.data)

            for child in e.children:
                to_visit.enqueue(child)


if __name__ == '__main__':
    # instanca stabla
    t = Tree()
    t.root = TreeNode(0)

    # kreiranje relacija između novih čvorova
    a = TreeNode(1)
    b = TreeNode(2)
    c = TreeNode(3)

    a.add_child(b)
    t.root.add_child(a)
    t.root.add_child(c)

    # visina stabla
    print('Visina = %d' % t.height())

    # dubina čvora
    print('Dubina(a) = %d' % t.depth(a))

    # obilazak po dubini - preorder
    print('PREORDER')
    t.preorder(t.root)

    # obilazak po dubini - postorder
    print('POSTORDER')
    t.postorder(t.root)

    # obilazak po širini
    print('BREADTH FIRST')
    t.breadth_first()
