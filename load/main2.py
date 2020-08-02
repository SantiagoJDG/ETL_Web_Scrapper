import argparse 
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd 

from article import Article 
from base import Base, engine, Session 

logger = logging.getLogger(__name__)

def main(filename):
    Base.metadata.create_all(engine) #Nos va a permitir generar nuestro schema en nuestra db
    session = Session() #Inicializamos nuestra sesion
    articles = pd.read_csv(filename)

    for index, row in articles.iterrows(): #iterrows: nos permite generar un loop adentro de cada una de nuestra filas de nuestro db
        logger.info('Loading article uid {} into db'.format(row['id']))
        article = Article(
                          row['id'],
                          row['body'],
                          row['host'],
                          row['newspaper_uid'],
                          row['n_valid_tokens_title'],
                          row['n_valid_tokens_body'],
                          row['title'],
                          row['url']
                          )
        
        session.add(article)


    session.close()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The file you want to load into de db',
                        type=str)
    args = parser.parse_args()

    main(args.filename)
