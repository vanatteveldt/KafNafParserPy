"""
This module parses the term layer of a KAF/NAF object
"""
from __future__ import print_function

from typing import Union, Iterable

from lxml import etree

from .element import KafNafElement, KafNafElements
from .span_data import Cspan
from .external_references_data import CexternalReferences
from .term_sentiment_data import Cterm_sentiment


class Cterm(KafNafElement):
    """
    This class encapsulates a <term> NAF or KAF object
    """
    element_name = 'term'
    naf_identifier = 'id'
    kaf_identifier = 'tid'

    def get_lemma(self) -> str:
        """
        Returns the lemma of the object
        @rtype: string
        @return: the term lemma
        """
        return self.node.get('lemma')

    def set_lemma(self, l: str):
        """
        Sets the lemma for the term
        @type l: string
        @param l: lemma 
        """
        self.node.set('lemma', l)
    
    def get_pos(self):
        """
        Returns the part-of-speech of the object
        @rtype: string
        @return: the term pos-tag
        """
        return self.node.get('pos')
 
    def set_pos(self, p):
        """
        Sets the postag for the term
        @type p: string
        @param p: pos-tag
        """
        self.node.set('pos',p)

    def get_type(self):
        """
        Returns the type of the term
        @rtype: string
        @return: the term type
        """
        return self.node.get('type')
           
    def set_type(self, t):
        """
        Sets the type for the term
        @type t: string
        @param t: type for the term
        """
        self.node.set('type',t)

    def get_case(self):
        """
        Returns the case of the term
        @rtype: string
        @return: the term case
        """
        return self.node.get('case')

    def set_case(self, c):
        """
        Sets the case for the term
        @type c: string
        @param c: case for the term
        """
        self.node.set('case', c)

    def get_head(self):
        """
        Returns the head of the (compound) term
        @rtype: string
        @return: the term head
        """
        return self.node.get('head')

    def set_head(self, h):
        """
        Sets the head for the term
        @type h: string
        @param h: head for the term
        """
        self.node.set('head', h)

    def get_morphofeat(self):
        """
        Returns the morphofeat attribute of the term
        @rtype: string
        @return: the term morphofeat feature
        """
        return self.node.get('morphofeat')
   
    def set_morphofeat(self, m):
        """
        Sets the morphofeat attribute
        @type m: string
        @param m: the morphofeat value
        """
        self.node.set('morphofeat', m)

    def get_span(self):
        """
        Returns the span object of the term
        @rtype: L{Cspan}
        @return: the term span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
        
    def set_span(self, this_span):
        """
        Sets the span for the term
        @type this_span: L{Cspan}
        @param this_span: the term span
        """
        self.node.append(this_span.get_node())

    def get_span_ids(self):
        """
        Returns the span object of the term
        @rtype: List
        @return: the term span as list of wf ids
        """
        node_span = self.node.find('span')
        if node_span is not None:
            mySpan = Cspan(node_span)
            span_ids = mySpan.get_span_ids()
            return span_ids
        else:
            return []

    def set_span_from_ids(self, span_list):
        """
        Sets the span for the term from list of ids
        @type span_list: []
        @param span_list: list of wf ids forming span
        """
        this_span = Cspan()
        this_span.create_from_ids(span_list)
        self.node.append(this_span.get_node())
        
    def get_sentiment(self):
        """
        Returns the sentiment object of the term
        @rtype: L{Cterm_sentiment}
        @return: the term sentiment
        """
        sent_node = self.node.find('sentiment')
        
        if sent_node is None:
            return None
        else:
            return Cterm_sentiment(sent_node)

    def add_sentiment(self, sentiment):
        """
        Sets the sentiment value for the term
        @type this_span: L{Cterm_sentiment}
        @param sentiment: the term sentiment
        """
        self.node.append(sentiment.get_node())
        
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference object to the term
        @type ext_ref: L{CexternalReference}
        @param ext_ref: an external reference object
        """
        ext_refs_node = self.node.find('externalReferences')
        if ext_refs_node is None:
            ext_refs_obj = CexternalReferences()
            self.node.append(ext_refs_obj.get_node())
        else:
            ext_refs_obj = CexternalReferences(ext_refs_node)
            
        ext_refs_obj.add_external_reference(ext_ref)
        
    def add_term_sentiment(self,term_sentiment):
        """
        Adds a sentiment object to the term
        @type term_sentiment: L{Cterm_sentiment}
        @param term_sentiment: an external reference object
        """
        self.node.append(term_sentiment.get_node())
        
    def get_external_references(self):
        """
        Iterator that returns all the external references of the term
        @rtype: L{CexternalReference}
        @return: the external references
        """
        for ext_ref_node in self.node.findall('externalReferences'):
            ext_refs_obj = CexternalReferences(ext_ref_node)
            for ref in ext_refs_obj:
                yield ref
            
    def remove_external_references(self):
        """
        Removes any external reference from the term
        """
        for ex_ref_node in self.node.findall('externalReferences'):
            self.node.remove(ex_ref_node)


class Cterms(KafNafElements):
    """
    This class encapsulates the term layer (collection of term objects)
    """
    child_element_name = 'term'
    child_class = Cterm

    def get_term(self, term_id) -> Union[Cterm, None]:
        """
        Returns the term object for the supplied identifier
        @type term_id: string
        @param term_id: term identifier
        """
        return self.get_child(term_id)

    def add_term(self, term_obj: Cterm) -> None:
        """
        Adds a term object to the layer
        @type term_obj: L{Cterm}
        @param term_obj: the term object
        """
        return self.add_child(term_obj)

    def remove_terms(self, list_term_ids: Iterable[str]):
        """
        Removes a list of terms from the layer
        @type list_term_ids: list
        @param list_term_ids: list of term identifiers to be removed
        """
        self.remove_children(list_term_ids)

    def add_external_reference(self,term_id, external_ref):
        """
        Adds an external reference for the given term
        @type term_id: string
        @param term_id: the term identifier
        @type external_ref: L{CexternalReference}
        @param external_ref: the external reference object
        """
        if term_id in self.idx:
            term_obj = Cterm(self.idx[term_id],self.type)
            term_obj.add_external_reference(external_ref)
        else:
            print('{term_id} not in self.idx'.format(**locals()))


