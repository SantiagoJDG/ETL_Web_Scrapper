import logging
logging.basicConfig(level=logging.INFO)
import subprocess #Nos permite manipular directamente archivos de terminal en python

logger = logging.getLogger(__name__)

news_sites_ids = ['eluniversal', 'revistaanfibia']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    logging.info('Starting extract process')
    for news_sites_id in news_sites_ids:
        subprocess.run(['python3', 'main.py', news_sites_id], cwd='./extract')  #Corremos el scrapper, nos dara un archivo con la data suci
        subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_id), #Buscamos el archivo que empiece con el news_sites_id
                        '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_sites_id), #Se le cambia el nombre al archivo   
                        ';'], cwd='./extract')

def _transform():
    logging.info('Starting transform process')
    for news_sites_id in news_sites_ids:
        dirty_data_filename = '{}_.csv'.format(news_sites_id)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python3', 'main.py', dirty_data_filename], cwd='./transform')
        subprocess.run(['rm', dirty_data_filename], cwd='./transform')
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_sites_id)], cwd='./transform')

def _load():
    logging.info('Starting load process')
    for news_sites_id in news_sites_ids:
        clean_data_filename = '{}'.format(news_sites_id)
        subprocess.run(['python3', 'main.py', clean_data_filename], cwd='./load')
        subprocess.run(['rm', clean_data_filename], cwd='./load')

    

if __name__ == '__main__':
    main()
