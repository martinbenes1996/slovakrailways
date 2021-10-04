
class Link:
    _links = {}
    @classmethod
    def create_key(cls, node1, node2):
        """"""
        return hash(min(node1.uic, node2.uic) + max(node1.uic, node2.uic))

    @classmethod
    def get(cls, node1, node2, *args, **kw):
        """"""
        link_key = cls.create_key(node1, node2)
        if link_key not in cls._links:
            cls._links[link_key] = cls(node1, node2, *args, **kw)
        return cls._links[link_key]

    @classmethod
    def disconnect(cls, node1, node2):
        """"""
        link_key = cls.create_key(node1, node2)
        if link_key in cls._links:
            del cls._links[link_key]
        else:
            print(f"Disconnecting {node1.uic} and {node2.uic}, that are not connected.")

    @classmethod
    def print_links(cls):
        """"""
        s = ""
        for link_key,link in cls._links.items():
            s += f"{link_key}) {link.node1.uic} *-* {link.node2.uic}" + "\n"
        return s

    def __init__(self, node1, node2, data={}, bidirectional=True):
        """Link constructor.
        
        Args:
            node1 (Node):
            node2 (Node):
            data ():
            bidirectional (bool):
        """
        self.node1 = node1
        self.node2 = node2
        self.data = data
        self._bidirectional = bidirectional

class Node:
    _nodes = {}
    @classmethod
    def get(cls, uic, *args, **kw):
        """Node object getter."""
        if uic not in cls._nodes:
            cls._nodes[uic] = cls(uic, *args, **kw)
        return cls._nodes[uic]

    def __init__(self, uic, data={}):
        """Create a Node.
        
        Args:
            uic (str): UIC code.
            data (dict): Station data.
        """
        self.uic = uic
        self._data = data

    def key(self):
        """"""
        return self._data.get('key',None)
    def name(self):
        """"""
        return self._data.get('name',None)
    def description(self):
        """"""
        return self._data.get('description',None)
    def coordinates(self):
        """"""
        return self._data.get('coordinates',[None,None])
    def latitude(self):
        """"""
        return self.coordinates()[0]
    def longitude(self):
        """"""
        return self.coordinates()[1]
    
    def connect(self, node, *args, **kw):
        """"""
        link = Link.get(self, node, *args, **kw)
        return link
    def disconnect(self, node):
        """"""
        Link.disconnect(self, node)
        
__all__ = ["Node","Link"]