from pathlib import Path 
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from tqdm.notebook import tqdm
import pandas as pd
import json


veg_prd_sup = {'돼지고기': [1, 1, 1, 1, 1, 1],
               '쇠고기': [1, 1, 1, 1, 1, 1],
               '가금류': [1, 1, 1, 1, 1, 0],
               '생선': [1, 1, 1, 1, 0, 0],
               '고기': [1, 1, 1, 1, 0, 0],
               '난류': [1, 1, 0, 0, 0, 0],
               '우유': [1, 0, 1, 0, 0, 0]}

veg_raw_sup = {'돼지': [1, 1, 1, 1, 1, 1],
               '쇠고기': [1, 1, 1, 1, 1, 1],
               '닭': [1, 1, 1, 1, 1, 0],
               '조개': [1, 1, 1, 1, 0, 0],
               '게': [1, 1, 1, 1, 0, 0],
               '새우': [1, 1, 1, 1, 0, 0],
               '고등어': [1, 1, 1, 1, 0, 0],
               '오징어': [1, 1, 1, 1, 0, 0],
               '고기': [1, 1, 1, 1, 0, 0],
               '난류': [1, 1, 0, 0, 0, 0],
               '우유': [1, 0, 1, 0, 0, 0]}


def main():
    with open('service_key.json', 'r') as f:
        service_key = json.load(f)
        service_key = service_key['key']
    update_date = datetime.now().strftime("%y%m%d%H%M%S")

    datasets_dir = Path("../datasets/")
    output_file = Path("haccp_dataset_{}.csv".format(update_date))
    if not Path.is_dir(datasets_dir):
        Path.mkdir(datasets_dir)
    output_path = datasets_dir / output_file

    url = "http://apis.data.go.kr/B553748/CertImgListService/getCertImgListService?\
    ServiceKey={service_key}&\
    returnType=xml&\
    pageNo={page_no}&\
    numOfRows={num_row}"

    data = urlopen(url.format(service_key=service_key, page_no=1, num_row=1)).read()
    soup = BeautifulSoup(data, "html.parser")
    num_page = int(soup.find('totalcount').text) // 100 + 1

    tags = [tag.name for tag in soup.find('item').find_all()]
    tags_dict = {'{}'.format(tag): [] for tag in tags}

    for i in tqdm(range(1, num_page + 1)):
        data = urlopen(url.format(service_key=service_key, page_no=i, num_row=100)).read()
        soup = BeautifulSoup(data, "html.parser")
        items = soup.find("items")

        for item in items.findAll("item"):
            for tag in tags:
                res = item.find(tag)
                val = res.text.strip() if res != None else "None"
                tags_dict[tag].append(str(val))

    df = pd.DataFrame.from_dict(tags_dict)
    df.to_csv(output_path, encoding='utf-8-sig', index=False)

    super_raw_path = datasets_dir / "SuperRaw.json"
    super_raw_all_path = datasets_dir / "SuperRawAll.json"
    super_raw_veg_path = datasets_dir / "SuperRawVeg.json"

    with open(super_raw_path, encoding='utf-8') as f:
        super_raw = json.load(f)
    with open(super_raw_veg_path, encoding='utf-8') as f:
        super_raw_veg = json.load(f)
    with open(super_raw_all_path, encoding='utf-8') as f:
        super_raw_all = json.load(f)

    raw_all_dst_dir = datasets_dir / "AllergyRawMtrl_{}.csv".format(update_date)
    raw_veg_dst_dir = datasets_dir / "VegRawMtrl_{}.csv".format(update_date)

    final_sup_raw_veg = []
    for sup, raw in super_raw.items():
        if sup in super_raw_veg.keys():
            veg_info = veg_raw_sup[sup]
        else:
            veg_info = [0, 0, 0, 0, 0, 0]
        for r in raw[0]:
            final_sup_raw_veg.append([r] + veg_info)

    raw_veg_cols = ["RawKind", "vegan", "lactoVeg", "ovoVeg", "lactoOvoVeg", "pescoVeg", "polloVeg"]
    final_df = pd.DataFrame(final_sup_raw_veg, columns=raw_veg_cols)
    final_df.to_csv(raw_veg_dst_dir, encoding="utf-8-sig", index=False)

    final_sup_raw_all = []
    for sup, raw in super_raw.items():
        if sup in super_raw_all.keys():
            all_info = [sup, 0, 'null', 'null']
        elif raw[1] == 1:
            all_info = [raw[2], 'true', raw[2], raw[3]]
        else:
            all_info = ['null', 0, 'null', 'null']
        for r in raw[0]:
            final_sup_raw_all.append([r] + all_info)

    raw_all_cols = ["rawMtrl", "allergy", "isCrossReact", "parentAllergy", "probablility"]
    final_df = pd.DataFrame(final_sup_raw_all, columns=raw_all_cols)
    final_df.to_csv(raw_all_dst_dir, encoding="utf-8-sig", index=False)


if __name__ == '__main__':
    main()