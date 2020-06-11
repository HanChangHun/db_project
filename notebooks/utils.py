import sqlalchemy
import logging

logger = logging.getLogger(__name__)

logging._defaultFormatter = logging.Formatter(u"%(message)s")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./queries.log')

streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.setLevel(level=logging.INFO)


def connect(user='postgres', password='1234', db='projectDB', host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    logger.info("SERVER COMNNECTED")
    return con


def read_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_string = f.read()
    return sql_string


def change_query_str(query):
    return query.replace('\n', ' ').strip()


def execute_query(conn, query):
    try:
        conn.execute(query)
        logger.info("COMPLETE QUERY : {}".format(change_query_str(query)))
    except Exception as e:
        logger.info("FAIL QUERY : {}\nERROR : {}".format(change_query_str(query), e))

        
def execute_queries(conn, queries):
    for q in queries.split(';')[:-1]:
        execute_query(conn, q)

        
def initializ_db(conn):
    for table in conn.table_names():
        drop_query = "drop table {}".format(table)
        execute_query(conn, drop_query)
    for e in ['allergy', 'veg', 'gen']:
        drop_query = "drop type {}".format(e)
        execute_query(conn, drop_query)
