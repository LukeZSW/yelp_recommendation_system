# -*- coding: UTF-8 -*-
# collaborative filtering

import numpy as np


def MAE(x, y):
    return np.average(abs(y - x))


def pearson_cor(x, y):
    denominator = (((x - x.mean()) ** 2).sum() ** 0.5) * (((y - y.mean()) ** 2).sum() ** 0.5)
    if denominator == 0:
        return 0.0
    else:
        return ((x - x.mean()) * (y - y.mean())).sum() / denominator


def user_cf(E, user_id, ave_all, k=10, com_item_shed=50):
    """
    :param E: user-item matrix
    :param user_id: user id
    :param ave_all: average of all ratings
    :param k: choose k neighbor
    :param com_item_shed: if common item number lower than watershed, the weight of correlation will reduce
    :return:  prediction rating for all items of chosen user id
    """
    num_user, num_item = E.shape
    weight = np.zeros(num_user)  # correlation value
    common_item = np.zeros(num_item)  # the number of common items
    for i in range(num_item):
        temp = (E[i] > 0) & (E[user_id] > 0)
        common_num = temp.sum()  # get common item number
        if common_num == 0:
            weight[i] = 0.0
        else:
            common_item[i] = common_num
            weight[i] = pearson_cor(E[i][temp], E[user_id][temp])  # Pearson correlation
        if common_num < com_item_shed:
            weight[i] *= common_num / com_item_shed
    weight_max_order = np.argsort(weight)
    k_index_order = weight_max_order[- k - 1: -1]  # top k correlation value
    ave = np.zeros(num_user)
    for i in range(num_user):
        if (E[i] != 0).sum() == 0:
            ave[i] = ave_all
        else:
            ave[i] = E[i].sum() / (E[i] != 0).sum()
    k_weight_sum = 0
    for i in range(k):
        k_weight_sum += weight[k_index_order[i]]
    prediction = np.ones(num_item) * ave[user_id]   # predict rating
    if k_weight_sum != 0:
        for i in range(k):
            temp = E[k_index_order[i]].copy()
            temp[temp == 0] = ave[k_index_order[i]]
            prediction += weight[k_index_order[i]] * (temp - ave[k_index_order[i]]) / k_weight_sum
    return prediction
