import argparse
from pathlib import Path
import pandas as pd
from tqdm import tqdm

from utils import *


parser = argparse.ArgumentParser(description='2020-1 database project 40db.')
parser.add_argument('--user', required=True, help='input your user name.')
parser.add_argument('--pwd', required=True, help='input your password')
parser.add_argument('--db', required=True, help='input your database name')
parser.add_argument('--host', required=False, default='localhost', help='input your host name')
parser.add_argument('--port', required=True, help='input your port number')
args = parser.parse_args()

user = args.user
pwd = args.pwd
db = args.db
host = args.host
port = args.port

replace_dict = {
    '(': ' ',
    ')': ' ',
    '%': '%%',
    "'": '',
    '\n': ' ',
    '\r': ' '
}


def main():
    conn = connect(user=user, password=pwd, db=db, host=host, port=port)
    initializ_db(conn)  # remove all table , enum('allergy', 'veg', 'gen') and triggers("Allergytrigger", "Vegtrigger")

    queries_dir = Path('queries/')
    enum_query = read_sql(queries_dir / "1.enum_query.sql")
    table_query = read_sql(queries_dir / "2.table_query.sql")
    trigger_query = read_sql(queries_dir / "3.trigger_query.sql")

    execute_queries(conn, enum_query)
    execute_queries(conn, table_query)
    execute_query(conn, trigger_query)

    datasets_dir = Path("../datasets/")
    haccp_dataset_path = list(datasets_dir.glob("haccp_dataset_*"))[-1]
    veg_rawmtrl_path = list(datasets_dir.glob("VegRawMtrl_*"))[-1]
    all_rawmtrl_path = list(datasets_dir.glob("AllergyRawMtrl_*"))[-1]

    haccp_dataset = pd.read_csv(haccp_dataset_path)
    haccp_dataset = haccp_dataset.drop(['rnum', 'productgb', 'prdkindstate'], axis=1)

    veg_rawmtrl = pd.read_csv(veg_rawmtrl_path)
    all_rawmtrl = pd.read_csv(all_rawmtrl_path)

    print("start upload VegRawMtrl table. \n")
    for data in tqdm(veg_rawmtrl.values):
        new_data = []
        for s in data:
            if type(s) == str:
                for org, dst in replace_dict.items():
                    s = s.replace(org, dst)
            new_data.append(s)
        rawMtrl, vegan, lactoVeg, ovoVeg, lactoOvoVeg, pescoVeg, polloVeg = new_data
        val = "'{}', '{}', '{}', '{}',' {}', '{}', '{}'".format(rawMtrl, vegan, lactoVeg, ovoVeg, lactoOvoVeg, pescoVeg, polloVeg)
        insert_query = "INSERT INTO VegRawMtrl VALUES({})".format(val)
        execute_query(conn, insert_query, log=False)
    print("complete upload VegRawMtrl table. \n")

    print("start upload AllergyRawMtrl table. \n")
    for data in tqdm(all_rawmtrl.values):
        new_data = []
        for s in data:
            if type(s) == str:
                for org, dst in replace_dict.items():
                    s = s.replace(org, dst)
            new_data.append(s)
        rawMtrl, allergy, isCrossReact, parentAllergy, probablility = new_data
        val = "'{}', '{}', '{}', '{}', '{}'".format(rawMtrl, allergy, isCrossReact, parentAllergy, probablility)
        insert_query = "INSERT INTO AllergyRawMtrl VALUES({})".format(val)
        execute_query(conn, insert_query, log=False)
    print("complete upload AllergyRawMtrl table. \n")

    print("start upload FoodInfo table. \n")
    for data in tqdm(haccp_dataset.values):
        new_data = []
        for s in data:
            if type(s) == str:
                for org, dst in replace_dict.items():
                    s = s.replace(org, dst)
            new_data.append(s)
        reportno, prdnm, rawmtrl, allergy, nutrient, barcode, prdkind, manu, seller, capa, img1, img2 = new_data
        try:
            barcode = int(barcode)
        except ValueError:
            barcode = 0
        val = "{reportno}, '{prdnm}', '{rawmtrl}', '{allergy}', '{nutrient}', {barcode},\
        '{prdkind}', '{manu}', '{seller}', '{capa}', '{img1}', '{img2}'".format(reportno=int(reportno), prdnm=prdnm, rawmtrl=rawmtrl,
                                                                                allergy=allergy, nutrient=nutrient, barcode=int(barcode),
                                                                                prdkind=prdkind, manu=manu, seller=seller, capa=capa, img1=img1, img2=img2)
        insert_query = "INSERT INTO FoodInfo VALUES({})".format(val)
        execute_query(conn, insert_query)
    print("complete upload FoodInfo table. \n")


if __name__ == '__main__':
    main()