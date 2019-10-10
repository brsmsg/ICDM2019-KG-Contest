# -*-coding:Latin-1 -*
import pandas as pd
from relation_extract import ERE


def read_write():
    """
    read texts from the dataset and write result into submission file
    """
    df = pd.read_csv('data/icdm_contest_data.csv', encoding='utf_8_sig')
    result_list = []
    for i in range(len(df['content'])):
        ERE1 = ERE(df['content'][i])
        for ere in ERE1:
            result_dict = {}
            result_dict['industry'] = df['industry'][i]
            result_dict['index'] = df['index'][i]
            result_dict['s1'] = ere[0]
            result_dict['r'] = ere[1]
            result_dict['s2'] = ere[2]
            result_list.append(result_dict)

    df2 = pd.DataFrame(result_list, columns=['industry', 'index', 's1', 'r', 's2'])
    df2.to_csv('data/best_now2.csv', encoding='utf_8_sig', index=False)


if __name__ == '__main__':
    read_write()
