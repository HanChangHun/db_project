import sqlalchemy
import logging


file_log, stream_log = True, False

logger = logging.getLogger(__name__)

logging._defaultFormatter = logging.Formatter(u"%(message)s")
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

if file_log:
    fileHandler = logging.FileHandler('./queries.log', mode='a', encoding='utf-8')
    logger.addHandler(fileHandler)
    fileHandler.setFormatter(formatter)

if stream_log:
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

logger.setLevel(level=logging.INFO)


def connect(user='postgres', password='0000', db='projectDB', host='localhost', port=5433):
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


def execute_query(conn, query, log=True):
    try:
        conn.execute(query)
        if log:
            logger.info("COMPLETE QUERY : {}".format(change_query_str(query)))
    except Exception as e:
        if log:
            logger.info("FAIL QUERY : {}\nERROR : {}".format(change_query_str(query), e))


def execute_queries(conn, queries):
    for q in queries.split(';')[:-1]:
        execute_query(conn, q)


def initializ_db(conn):
    for v in ["Allergytrigger", "Vegtrigger"]:
        drop_query = "drop trigger {} on foodinfo".format(v)
        execute_query(conn, drop_query)
    for table in conn.table_names():
        drop_query = "drop table {}".format(table)
        execute_query(conn, drop_query)
    for e in ['allergy', 'veg', 'gen']:
        drop_query = "drop type {}".format(e)
        execute_query(conn, drop_query)
