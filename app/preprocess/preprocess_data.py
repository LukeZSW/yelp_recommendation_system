# -*- encoding: utf-8 -*-
# preprocess yelp dataset;
# get data in Las Vegas;
# choose businesses have more than 5 rating
# and users have more than 20 rating;
# get rating.json save user_id business_id and star

import pandas as pd
import os

if __name__ == '__main__':
    # load original data
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    current_parent_path = os.path.dirname(current_dir_path)
    res_dir = os.path.join(current_parent_path, 'res')
    df_business = pd.read_json(os.path.join(res_dir, 'yelp_academic_dataset_business.json'), encoding="utf-8", lines=True)
    df_user = pd.read_json(os.path.join(res_dir, 'yelp_academic_dataset_user.json'), encoding="utf-8", lines=True)
    df_review = pd.read_json(os.path.join(res_dir, 'yelp_academic_dataset_review.json'), encoding="utf-8", lines=True)
    # choose data in Las Vegas
    df_business_las_vegas = df_business[df_business['city'] == 'Las Vegas']
    df_business_las_vegas = df_business_las_vegas[df_business_las_vegas['is_open'] == 1]
    df_business_las_vegas['businessidindex'] = df_business_las_vegas.index
    df_user['useridindex'] = df_user.index
    df_business_las_vegas_idindex = df_business_las_vegas[['business_id', 'businessidindex']]
    df_review_las_vegas0 = pd.merge(df_review, df_business_las_vegas_idindex,
                                    left_on='business_id', right_on='business_id')
    df_user_idindex = df_user[['user_id', 'useridindex']]
    df_review_las_vegas = pd.merge(df_review_las_vegas0, df_user_idindex,
                                   left_on='user_id', right_on='user_id')
    lvuser = df_review_las_vegas['useridindex'].unique()
    df_user_las_vegas = df_user[df_user['useridindex'].isin(lvuser)]

    # df_user_las_vegas.to_json(os.path.join(res_dir, 'user_las_vegas.json'))
    # df_review_las_vegas.to_json(os.path.join(res_dir, 'review_las_vegas.json'))
    # df_business_las_vegas.to_json(os.path.join(res_dir, 'business_las_vegas.json'))
    #
    # df_business_las_vegas = pd.read_json(os.path.join(res_dir, 'user_las_vegas.json'), encoding="utf-8")
    # df_user_las_vegas = pd.read_json(os.path.join(res_dir, 'review_las_vegas.json'), encoding="utf-8")
    # df_review_las_vegas = pd.read_json(os.path.join(res_dir, 'business_las_vegas.json'), encoding="utf-8")

    select_columns = ['useridindex', 'businessidindex', 'stars']
    df_rating0 = df_review_las_vegas[select_columns]

    # choose small part
    print(df_rating0.shape)
    # choose rating number > 20 user
    df_rating_user = df_rating0.useridindex.unique()
    df_rating_user0 = df_rating_user[df_rating0['useridindex'].value_counts() > 20]
    df_rating = df_rating0[df_rating0['useridindex'].isin(df_rating_user0)]
    # choose rating number > 5 item
    df_rating_item = df_rating.businessidindex.unique()
    df_rating_item0 = df_rating_item[df_rating['businessidindex'].value_counts() > 5]
    df_rating = df_rating[df_rating['businessidindex'].isin(df_rating_item0)]
    print(df_rating.shape)

    n_users = df_rating.useridindex.unique().shape[0]
    n_items = df_rating.businessidindex.unique().shape[0]
    print('Number of users = ' + str(n_users))
    print('Number of businesses = ' + str(n_items))
    id = df_rating.useridindex.unique()
    order = range(n_users)
    dict_userid2order = dict(zip(id, order))
    dict_order2userid = dict(zip(order, id))
    id = df_rating.businessidindex.unique()
    order = range(n_items)
    dict_itemid2order = dict(zip(id, order))
    dict_order2itemid = dict(zip(order, id))
    df_rating['userorder'] = df_rating['useridindex'].map(lambda x: dict_userid2order[x])
    df_rating['itemorder'] = df_rating['businessidindex'].map(lambda x: dict_itemid2order[x])
    df_rating_ave = df_rating.groupby(['useridindex', 'businessidindex']).mean()
    print(df_rating_ave.shape)
    sparsity = 1.0 - len(df_rating_ave) / (n_users * n_items)
    print('The sparsity level: ' + str(sparsity * 100) + '%')

    user_small = df_rating.useridindex.unique()
    df_user_small = df_user_las_vegas[df_user_las_vegas['useridindex'].isin(user_small)]
    item_small = df_rating.businessidindex.unique()
    df_item_small = df_business_las_vegas[df_business_las_vegas['businessidindex'].isin(item_small)]
    df_user_small.shape, df_item_small.shape

    df_user_small['userorder'] = df_user_small['useridindex'].map(lambda x: dict_userid2order[x])
    df_item_small['itemorder'] = df_item_small['businessidindex'].map(lambda x: dict_itemid2order[x])

    df_user_small.to_json(os.path.join(res_dir, 'user.json'))
    df_item_small.to_json(os.path.join(res_dir, 'item.json'))
    df_rating.to_json(os.path.join(res_dir, 'rating.json'))
