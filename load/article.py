from sqlalchemy import Column, String, Integer
from base import Base

class Article(Base):

    __tablename__='articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    n_valid_tokens_title = Column(Integer)
    n_valid_tokens_body = Column(Integer)
    url = Column(String, unique=True)

    def __init__(self,
                uid,
                body,
                host, 
                title, 
                newspaper_uid,
                n_valid_tokens_title,
                n_valid_tokens_body,
                url):
    
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self.newspaper_uid = newspaper_uid, 
        self.n_valid_tokens_title = n_valid_tokens_title
        self.n_valid_tokens_body = n_valid_tokens_body
        self.url = url
