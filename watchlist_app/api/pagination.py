from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 10
    # page_query_param = 'p'
    #taken from client
    page_size_query_param = 'size' 
    #max these many whill be there in page
    max_page_size = 10
    #to view last page ?p=end
    last_page_strings = 'last'

class WatchListLOPagination(LimitOffsetPagination): 
    default_limit = 5 
    max_limit = 10
    limit_query_param='limit'
    offet_query_param = 'start'

class WatchListCPagination(CursorPagination):
    page_size = 5    
    #whatever field with which we want to keep ordering
    ordering = 'created'
    cursor_query_param = 'record'
 