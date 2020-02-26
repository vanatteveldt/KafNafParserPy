from typing import Iterator, Union, Iterable

from lxml import etree


class KafNafElement:
    """Superclass for KafNaf elements (terms, spans, etc.) """
    element_name = None  # XML element name of this element (e.g. term)
    naf_identifier = None  # Identifier for NAF (e.g. id)
    kaf_identifier = None  # Identifier for NAF (e.g. tid)

    def __init__(self, node: etree.Element = None, type:str = 'NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element(self.element_name)
        else:
            self.node = node

    def get_node(self) -> etree.Element:
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def get_id(self) -> str:
        """
        Returns the term identifier
        @rtype: string
        @return: the term identifier
        """
        if self.type == 'NAF':
            return self.node.get(self.naf_identifier)
        elif self.type == 'KAF':
            return self.node.get(self.kaf_identifier)

    def set_id(self, i: str):
        """
        Sets the identifier for the term
        @type i: string
        @param i: chunk identifier
        """
        if self.type == 'NAF':
            self.node.set(self.naf_identifier, i)
        elif self.type == 'KAF':
            self.node.set(self.kaf_identifier, i)


class KafNafElements(KafNafElement):
    """
    Superclass for KafNafElements, e.g. the layer containing individual elements
    """
    child_element_name = None  # XML element name of the child elements contained in this node, e.g. term
    child_class = None  # Python class of the child elements, e.g. Cterm

    def __init__(self, node: etree.Element = None, type: str = 'NAF'):
        super().__init__(node, type)
        self.idx = {}
        for child_node in self.__get_child_nodes():
            term_obj = self.child_class(child_node, self.type)
            self.idx[term_obj.get_id()] = child_node

    def __get_child_nodes(self):
        return self.node.findall(self.child_element_name)

    def __iter__(self) -> Iterator[KafNafElement]:
        for child_node in self.__get_child_nodes():
            yield self.child_class(child_node, self.type)

    def to_kaf(self):
        """
        Converts the object to KAF (if it is NAF)
        """
        if self.type == 'NAF':
            self.type = 'KAF'
            for node in self.__get_child_nodes():
                node.set(self.kaf_identifier, node.get(self.naf_identifier))
                del node.attrib[self.naf_identifier]

    def to_naf(self):
        """
        Converts the object to NAF (if it is KAF)
        """
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_child_nodes():
                node.set(self.naf_identifier, node.get(self.kaf_identifier))
                del node.attrib[self.naf_identifier]

    def get_child(self, id: str) -> Union[KafNafElement, None]:
        """
        Returns the child object for the supplied identifier
        """
        if id in self.idx:
            return self.child_class(self.idx[id], self.type)
        else:
            return None

    def add_child(self, child: KafNafElement) -> None:
        """
        Adds a child object to the layer
        """
        if child.get_id() in self.idx:
            raise ValueError(f"Term with id {child.get_id()} already exists!")
        self.node.append(child.get_node())
        self.idx[child.get_id()] = child.get_node()
        # NOTE: original added the child instead of node, but that seems inconsistent with initial construction of .idx

    def remove_children(self, list_term_ids: Iterable[str]):
        """
        Removes a list of children from the layer based on their ids
        """
        nodes_to_remove = set()
        for child in self:
            if child.get_id() in list_term_ids:
                nodes_to_remove.add(child.get_node())
                # For removing the previous comment
                prv = child.get_node().getprevious()
                if prv is not None:
                    nodes_to_remove.add(prv)
        for node in nodes_to_remove:
            self.node.remove(node)

