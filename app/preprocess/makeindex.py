# -*- coding: UTF-8 -*-
# make index for restaurant data
# use whoosh library

from whoosh.index import create_in
from whoosh.fields import *
import os.path
import pandas as pd

if __name__ == "__main__":
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    current_parent_path = os.path.dirname(current_dir_path)
    res_dir = os.path.join(current_parent_path, 'res')
    item_file = os.path.join(res_dir, 'item.json')
    indexdir = os.path.join(res_dir, 'indexdir')
    df = pd.read_json(item_file, encoding='utf-8')
    df.fillna('')
    df['resname'] = df['name']
    selectcolumns = ['itemorder', 'resname', 'categories', 'address', 'postal_code', 'city', 'state',
                     'stars', 'review_count', 'latitude', 'longitude']
    df = df[selectcolumns]
    df = df.dropna()
    numcolumns = ['latitude', 'longitude', 'review_count', 'stars']
    df[numcolumns] = df[numcolumns].astype(float)
    df['itemorder'] = df['itemorder'].astype(int)
    df['itemorder'] = df['itemorder'].astype(str)
    schema = Schema(ID=TEXT(stored=True),
                    resname=TEXT(stored=True),
                    categories=TEXT(stored=True),
                    address=TEXT(stored=True),
                    rating=NUMERIC(stored=True, sortable=True),
                    review_count=NUMERIC(stored=True, sortable=True),
                    latitude=NUMERIC(stored=True),
                    longitude=NUMERIC(stored=True),
                    city=TEXT(stored=True),
                    postal_code=TEXT(stored=True),
                    state=TEXT(stored=True))
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    w = ix.writer()
    for i in range(len(df)):
        l = df.iloc[i]
        w.add_document(ID=l.itemorder,
                       resname=l.resname,
                       categories=l.categories,
                       address=l.address,
                       rating=l.stars,
                       review_count=l.review_count,
                       latitude=l.latitude,
                       longitude=l.longitude,
                       city=l.city,
                       postal_code=l.postal_code,
                       state=l.state)
    w.commit()
