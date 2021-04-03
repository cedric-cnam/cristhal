from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index
from elasticsearch_dsl import Text, Integer, Document
from elasticsearch_dsl.query import  Match

import json
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class ReferentielIndex(Document):
    '''
        Object indexed in Elastic search, as a subclass of ES Document
    '''
    ref_locale = Text()
    title = Text()
    type = Text()
    source = Text()
    description_source = Text()
    rank = Text()
    
    class Index:
        name = settings.ES_INDEX_REF

class IndexWrapper:
    """A class to interact with ElasticSearch"""

    def __init__(self, auth_login=None, auth_password=None) :
        if auth_login is None:
            self.elastic_search = Elasticsearch(host=settings.ELASTIC_SEARCH["host"], 
                                            port=settings.ELASTIC_SEARCH["port"],
                                            index=settings.ELASTIC_SEARCH["index"])
        else:
            self.elastic_search = Elasticsearch(host=settings.ELASTIC_SEARCH["host"], 
                                            port=settings.ELASTIC_SEARCH["port"],
                                            index=settings.ELASTIC_SEARCH["index"],
                                            http_auth=(auth_login, auth_password))
            
        # Open, and possibly create the index
        self.index = Index (settings.ES_INDEX_REF,using=self.elastic_search)
        
        if not self.index.exists(using=self.elastic_search):
            # Create the index, and the mapping to Referentiel docs
            self.index.create(using=self.elastic_search)
            self.index.settings(number_of_shards=1, number_of_replicas=0)

        self.index.open(using=self.elastic_search)
        self.query_dir = settings.ES_QUERY_DIR


    def get_index_info (self):
        return self.index.get()

    def search(self, keywords, type_ref):
        """Create the search object with ElasticSearch DSL"""
        #print ("Search with keywords " +  keywords + " and type " + type_ref)
        search = self.index.search()
        #search = search.params (size=settings.MAX_ITEMS_IN_RESULT)
        
        search = search.query("match", ft_field=keywords)  
        search = search.query("match", type=type_ref)  
        #search.extra(explain=True)
        search.execute()
        return search

    def store_ref (self, ref):
        """ Receive a Referentiel Django model instance, send it to ElasticSearch"""
        
        ref_index = ReferentielIndex(
                ref_locale=str(ref.ref_locale),
                title=ref.titre,
                acronym=ref.acronyme,
                ft_field=ref.champ_plein_texte,
                source=ref.source.type_source,
                description_source=ref.source.description,
                type=ref.type,
                rank=ref.classement
            )
        
        ref_index.save(using=self.elastic_search,id=ref.ref_locale)

    def delete_ref (self, ref):
        """ Receive a Referentiel Django model instance, remove from ElasticSearch"""
        search = self.index.search()
        search=search.query("match", ref_locale=ref.ref_locale)
        search.delete()
    