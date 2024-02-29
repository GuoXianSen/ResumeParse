import os
import pickle as pkl
import random

import dgl

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset


# Split data into train/eval/test
def split_data(hg, etype_name):
    src, dst = hg.edges(etype=etype_name) #tensor(xxxx,1)
    user_item_src = src.numpy().tolist()  #list(xxxx)
    user_item_dst = dst.numpy().tolist()  #list()


    num_link = len(user_item_src)
    pos_label = [1] * num_link
    pos_data = list(zip(user_item_src, user_item_dst, pos_label))  #正向数据 list 每个元素都是一个三元组

    ui_adj = np.array(hg.adj(etype=etype_name).to_dense())#邻接矩阵 ndarray
    full_idx = np.where(ui_adj == 0) #统计那些没有边的节点 二元组

    sample = random.sample(range(0, len(full_idx[0])), num_link)  #list从没有节点的里面选出一些边 作为负向边
    neg_label = [0] * num_link    #负向边
    neg_data = list(zip(full_idx[0][sample], full_idx[1][sample], neg_label)) #负向数据 list 每个元素都是一个三元组

    full_data = pos_data + neg_data   #整个数据  list 每个元素都是一个三元组
    random.shuffle(full_data) #打乱序列里面的元素，并随机排列的。

    train_size = int(len(full_data) * 0.9)
    eval_size = int(len(full_data) * 0.05)
    test_size = len(full_data) - train_size - eval_size
    train_data = full_data[:train_size]
    eval_data = full_data[train_size : train_size + eval_size]
    test_data = full_data[
        train_size + eval_size : train_size + eval_size + test_size
    ]
    train_data = np.array(train_data)
    eval_data = np.array(eval_data)
    test_data = np.array(test_data)

    return train_data, eval_data, test_data


def process_amazon(root_path):
    # User-Item 3584 2753 50903 UIUI
    # Item-View 2753 3857 5694 UIVI
    # Item-Brand 2753 334 2753 UIBI
    # Item-Category 2753 22 5508 UICI

    # Construct graph from raw data.
    # load data of amazon
    data_path = os.path.join(root_path, "Amazon")
    if not (os.path.exists(data_path)):
        print(
            "Can not find amazon in {}, please download the dataset first.".format(
                data_path
            )
        )

    # item_view
    item_view_src = []
    item_view_dst = []
    with open(os.path.join(data_path, "item_view.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            item, view = int(_line[0]), int(_line[1])
            item_view_src.append(item)
            item_view_dst.append(view)

    # user_item
    user_item_src = []
    user_item_dst = []
    user_item_rate = []
    with open(os.path.join(data_path, "user_item.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split("\t")
            user, item, rate = int(_line[0]), int(_line[1]), int(_line[2])
            # if rate > 0:
            user_item_src.append(user)
            user_item_dst.append(item)
            user_item_rate.append(rate)


    # item_brand
    item_brand_src = []
    item_brand_dst = []
    with open(os.path.join(data_path, "item_brand.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            item, brand = int(_line[0]), int(_line[1])
            item_brand_src.append(item)
            item_brand_dst.append(brand)

    # item_category
    item_category_src = []
    item_category_dst = []
    with open(os.path.join(data_path, "item_category.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            item, category = int(_line[0]), int(_line[1])
            item_category_src.append(item)
            item_category_dst.append(category)

    # build graph
    hg = dgl.heterograph(
        {
            ("item", "iv", "view"): (item_view_src, item_view_dst),
            ("view", "vi", "item"): (item_view_dst, item_view_src),
            ("user", "ui", "item"): (user_item_src, user_item_dst),
            ("item", "iu", "user"): (user_item_dst, user_item_src),
            ("item", "ib", "brand"): (item_brand_src, item_brand_dst),
            ("brand", "bi", "item"): (item_brand_dst, item_brand_src),
            ("item", "ic", "category"): (item_category_src, item_category_dst),
            ("category", "ci", "item"): (item_category_dst, item_category_src),
        }
    )


    print("Graph constructed.")

    # Split data into train/eval/test
    train_data, eval_data, test_data = split_data(hg, "ui")

    # delete the positive edges in eval/test data in the original graph
    train_pos = np.nonzero(train_data[:, 2])
    train_pos_idx = train_pos[0]
    user_item_src_processed = train_data[train_pos_idx, 0]
    user_item_dst_processed = train_data[train_pos_idx, 1]
    edges_dict = {
        ("item", "iv", "view"): (item_view_src, item_view_dst),
        ("view", "vi", "item"): (item_view_dst, item_view_src),
        ("user", "ui", "item"): (
            user_item_src_processed,
            user_item_dst_processed,
        ),
        ("item", "iu", "user"): (
            user_item_dst_processed,
            user_item_src_processed,
        ),
        ("item", "ib", "brand"): (item_brand_src, item_brand_dst),
        ("brand", "bi", "item"): (item_brand_dst, item_brand_src),
        ("item", "ic", "category"): (item_category_src, item_category_dst),
        ("category", "ci", "item"): (item_category_dst, item_category_src),
    }
    nodes_dict = {
        "user": hg.num_nodes("user"),      #返回图中user节点的数量
        "item": hg.num_nodes("item"),
        "view": hg.num_nodes("view"),
        "brand": hg.num_nodes("brand"),
        "category": hg.num_nodes("category"),
    }
    hg_processed = dgl.heterograph(
        data_dict=edges_dict, num_nodes_dict=nodes_dict
    )
    print("Graph processed.")

    # save the processed data
    with open(os.path.join(root_path, "amazon_hg.pkl"), "wb") as file:
        pkl.dump(hg_processed, file)
    with open(os.path.join(root_path, "amazon_train.pkl"), "wb") as file:
        pkl.dump(train_data, file)
    with open(os.path.join(root_path, "amazon_test.pkl"), "wb") as file:
        pkl.dump(test_data, file)
    with open(os.path.join(root_path, "amazon_eval.pkl"), "wb") as file:
        pkl.dump(eval_data, file)

    return hg_processed, train_data, eval_data, test_data


def process_movielens(root_path):
    # User-Movie 943 1682 100000 UMUM
    # User-Age 943 8 943 UAUM
    # User-Occupation 943 21 943 UOUM
    # Movie-Genre 1682 18 2861 UMGM

    data_path = os.path.join(root_path, "Movielens")
    if not (os.path.exists(data_path)):
        print(
            "Can not find movielens in {}, please download the dataset first.".format(
                data_path
            )
        )

    # Construct graph from raw data.
    # movie_genre
    movie_genre_src = []
    movie_genre_dst = []
    with open(os.path.join(data_path, "movie_genre.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split("\t")
            movie, genre = int(_line[0]), int(_line[1])
            movie_genre_src.append(movie)
            movie_genre_dst.append(genre)

    # user_movie
    user_movie_src = []
    user_movie_dst = []
    with open(os.path.join(data_path, "user_movie.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split("\t")
            user, item, rate = int(_line[0]), int(_line[1]), int(_line[2])
            if rate > 3:
                user_movie_src.append(user)
                user_movie_dst.append(item)

    # user_occupation
    user_occupation_src = []
    user_occupation_dst = []
    with open(os.path.join(data_path, "user_occupation.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split("\t")
            user, occupation = int(_line[0]), int(_line[1])
            user_occupation_src.append(user)
            user_occupation_dst.append(occupation)

    # user_age
    user_age_src = []
    user_age_dst = []
    with open(os.path.join(data_path, "user_age.dat")) as fin:
        for line in fin.readlines():
            _line = line.strip().split("\t")
            user, age = int(_line[0]), int(_line[1])
            user_age_src.append(user)
            user_age_dst.append(age)

    # build graph
    hg = dgl.heterograph(
        {
            ("movie", "mg", "genre"): (movie_genre_src, movie_genre_dst),
            ("genre", "gm", "movie"): (movie_genre_dst, movie_genre_src),
            ("user", "um", "movie"): (user_movie_src, user_movie_dst),
            ("movie", "mu", "user"): (user_movie_dst, user_movie_src),
            ("user", "uo", "occupation"): (
                user_occupation_src,
                user_occupation_dst,
            ),
            ("occupation", "ou", "user"): (
                user_occupation_dst,
                user_occupation_src,
            ),
            ("user", "ua", "age"): (user_age_src, user_age_dst),
            ("age", "au", "user"): (user_age_dst, user_age_src),
        }
    )

    print("Graph constructed.")

    # Split data into train/eval/test
    train_data, eval_data, test_data = split_data(hg, "um")

    # delete the positive edges in eval/test data in the original graph
    train_pos = np.nonzero(train_data[:, 2])
    train_pos_idx = train_pos[0]
    user_movie_src_processed = train_data[train_pos_idx, 0]
    user_movie_dst_processed = train_data[train_pos_idx, 1]
    edges_dict = {
        ("movie", "mg", "genre"): (movie_genre_src, movie_genre_dst),
        ("genre", "gm", "movie"): (movie_genre_dst, movie_genre_src),
        ("user", "um", "movie"): (
            user_movie_src_processed,
            user_movie_dst_processed,
        ),
        ("movie", "mu", "user"): (
            user_movie_dst_processed,
            user_movie_src_processed,
        ),
        ("user", "uo", "occupation"): (
            user_occupation_src,
            user_occupation_dst,
        ),
        ("occupation", "ou", "user"): (
            user_occupation_dst,
            user_occupation_src,
        ),
        ("user", "ua", "age"): (user_age_src, user_age_dst),
        ("age", "au", "user"): (user_age_dst, user_age_src),
    }
    nodes_dict = {
        "user": hg.num_nodes("user"),
        "movie": hg.num_nodes("movie"),
        "genre": hg.num_nodes("genre"),
        "occupation": hg.num_nodes("occupation"),
        "age": hg.num_nodes("age"),
    }
    hg_processed = dgl.heterograph(
        data_dict=edges_dict, num_nodes_dict=nodes_dict
    )
    print("Graph processed.")

    # save the processed data
    with open(os.path.join(root_path, "movielens_hg.pkl"), "wb") as file:
        pkl.dump(hg_processed, file)
    with open(os.path.join(root_path, "movielens_train.pkl"), "wb") as file:
        pkl.dump(train_data, file)
    with open(os.path.join(root_path, "movielens_test.pkl"), "wb") as file:
        pkl.dump(test_data, file)
    with open(os.path.join(root_path, "movielens_eval.pkl"), "wb") as file:
        pkl.dump(eval_data, file)

    return hg_processed, train_data, eval_data, test_data

def process_jobmatch(root_path):
    # User-Item 3584 2753 50903 UIUI
    # Item-View 2753 3857 5694 UIVI
    # Item-Brand 2753 334 2753 UIBI
    # Item-Category 2753 22 5508 UICI

    # Construct graph from raw data.
    # load data of amazon
    data_path = os.path.join(root_path, "ready")
    if not (os.path.exists(data_path)):
        print(
            "Can not find amazon in {}, please download the dataset first.".format(
                data_path
            )
        )

    # user_degree
    user_degree_src = []
    user_degree_dst = []
    with open(os.path.join(data_path, "uid_degree.csv")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            user, degree = int(_line[0]), int(_line[1])
            user_degree_src.append(user)
            user_degree_dst.append(degree)

    # user_skill
    user_skill_src = []
    user_skill_dst = []
    with open(os.path.join(data_path, "uid_skill.csv")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            user, skill = int(_line[0]), int(_line[1])
            # if rate > 0:
            user_skill_src.append(user)
            user_skill_dst.append(skill)

    # user_major
    user_major_src = []
    user_major_dst = []
    with open(os.path.join(data_path, "uid_major.csv")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            user, major = int(_line[0]), int(_line[1])
            user_major_src.append(user)
            user_major_dst.append(major)

    # user_position
    user_position_src = []
    user_position_dst = []
    with open(os.path.join(data_path, "uid_position.csv")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            user, position = int(_line[0]), int(_line[1])
            user_position_src.append(user)
            user_position_dst.append(position)

    # position_skill
    position_skill_src = []
    position_skill_dst = []
    with open(os.path.join(data_path, "position_skill.csv")) as fin:
        for line in fin.readlines():
            _line = line.strip().split(",")
            position, skill = int(_line[0]), int(_line[1])
            position_skill_src.append(position)
            position_skill_dst.append(skill)

    # build graph
    hg = dgl.heterograph(
        {
            ("user", "ud", "degree"): (user_degree_src, user_degree_dst),
            ("degree", "du", "user"): (user_degree_dst, user_degree_src),
            ("user", "us", "skill"): (user_skill_src, user_skill_dst),
            ("skill", "su", "user"): (user_skill_dst, user_skill_src),
            ("user", "um", "major"): (user_major_src, user_major_dst),
            ("major", "mu", "user"): (user_major_dst, user_major_src),
            ("user", "up", "position"): (user_position_src, user_position_dst),
            ("position", "pu", "user"): (user_position_dst, user_position_src),
            ("position", "ps", "skill"): (position_skill_src, position_skill_dst),
            ("skill", "sp", "position"): (position_skill_dst, position_skill_src),
        }
    )
    print("Graph constructed.")

    # Split data into train/eval/test
    train_data, eval_data, test_data = split_data(hg, "up")

    # delete the positive edges in eval/test data in the original graph
    train_pos = np.nonzero(train_data[:, 2])
    train_pos_idx = train_pos[0]
    user_position_src_processed = train_data[train_pos_idx, 0]
    user_position_dst_processed = train_data[train_pos_idx, 1]
    edges_dict = {
        ("user", "ud", "degree"): (user_degree_src, user_degree_dst),
        ("degree", "du", "user"): (user_degree_dst, user_degree_src),
        ("user", "us", "skill"): (user_skill_src, user_skill_dst),
        ("skill", "su", "user"): (user_skill_dst, user_skill_src),
        ("user", "um", "major"): (user_major_src, user_major_dst),
        ("major", "mu", "user"): (user_major_dst, user_major_src),
        ("user", "up", "position"): (user_position_src_processed, user_position_dst_processed),
        ("position", "pu", "user"): (user_position_dst_processed, user_position_src_processed),
        ("position", "ps", "skill"): (position_skill_src, position_skill_dst),
        ("skill", "sp", "position"): (position_skill_dst, position_skill_src),
    }
    nodes_dict = {
        "user": hg.num_nodes("user"),      #返回图中user节点的数量
        "degree": hg.num_nodes("degree"),
        "skill": hg.num_nodes("skill"),
        "major": hg.num_nodes("major"),
        "position": hg.num_nodes("position"),
    }
    hg_processed = dgl.heterograph(
        data_dict=edges_dict, num_nodes_dict=nodes_dict
    )
    print("Graph processed.")

    # save the processed data
    with open(os.path.join(root_path, "jobmatch_hg.pkl"), "wb") as file:
        pkl.dump(hg_processed, file)
    with open(os.path.join(root_path, "jobmatch_train.pkl"), "wb") as file:
        pkl.dump(train_data, file)
    with open(os.path.join(root_path, "jobmatch_test.pkl"), "wb") as file:
        pkl.dump(test_data, file)
    with open(os.path.join(root_path, "jobmatch_eval.pkl"), "wb") as file:
        pkl.dump(eval_data, file)

    return hg_processed, train_data, eval_data, test_data

class MyDataset(Dataset):
    def __init__(self, triple):
        self.triple = triple
        self.len = self.triple.shape[0]     #设置为triple中的样本数量

    def __getitem__(self, index):
        return (
            self.triple[index, 0],   #self.triple的第index行的第一个元素
            self.triple[index, 1],
            self.triple[index, 2].float(),
        )

    def __len__(self):
        return self.len   #返回数据集中的样本总数


def load_data(dataset, batch_size=128, num_workers=10, root_path="./data"):
    if os.path.exists(os.path.join(root_path, dataset + "_train.pkl")):
        g_file = open(os.path.join(root_path, dataset + "_hg.pkl"), "rb")
        hg = pkl.load(g_file)
        g_file.close()
        train_set_file = open(
            os.path.join(root_path, dataset + "_train.pkl"), "rb"
        )
        train_set = pkl.load(train_set_file)
        train_set_file.close()
        test_set_file = open(
            os.path.join(root_path, dataset + "_test.pkl"), "rb"
        )
        test_set = pkl.load(test_set_file)
        test_set_file.close()
        eval_set_file = open(
            os.path.join(root_path, dataset + "_eval.pkl"), "rb"
        )
        eval_set = pkl.load(eval_set_file)
        eval_set_file.close()
    else:
        if dataset == "movielens":
            hg, train_set, eval_set, test_set = process_movielens(root_path)
        elif dataset == "amazon":
            hg, train_set, eval_set, test_set = process_amazon(root_path)
        elif dataset == "jobmatch":
            hg, train_set, eval_set, test_set = process_jobmatch(root_path)
        else:
            print("Available datasets: movielens, amazon.")
            raise NotImplementedError

    if dataset == "movielens":
        meta_paths = {
            "user": [["um", "mu"]],
            "movie": [["mu", "um"], ["mg", "gm"]],
        }
        user_key = "user"
        item_key = "movie"
    elif dataset == "amazon":
        meta_paths = {
            "user": [["ui", "iu"]],
            "item": [["iu", "ui"], ["ic", "ci"], ["ib", "bi"], ["iv", "vi"]],
        }
        user_key = "user"
        item_key = "item"
    elif dataset == "jobmatch":
        meta_paths = {
            "user": [["ud", "du"],["us","su"],["um","mu"]],
            "position": [["ps","sp"]],
        }
        user_key = "user"
        item_key = "position"
    else:
        print("Available datasets: movielens, amazon.")
        raise NotImplementedError


    train_set = torch.Tensor(train_set).long()     #Tensor(189,3)
    eval_set = torch.Tensor(eval_set).long()                   #Tensor(63,3)
    test_set = torch.Tensor(test_set).long()               #Tensor(64,3)

    train_set = MyDataset(train_set)
    train_loader = DataLoader(
        dataset=train_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    eval_set = MyDataset(eval_set)
    eval_loader = DataLoader(
        dataset=eval_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    test_set = MyDataset(test_set)
    test_loader = DataLoader(
        dataset=test_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )

    return (
        hg,        # Graph(num_nodes={'brand': 5, 'category': 2, 'item': 2646, 'user': 6157, 'view': 13},
                   # num_edges={('brand', 'bi', 'item'): 5, ('category', 'ci', 'item'): 9, ('item', 'ib', 'brand'): 5, ('item', 'ic', 'category'): 9, ('item', 'iu', 'user'): 104, ('item', 'iv', 'view'): 13, ('user', 'ui', 'item'): 104, ('view', 'vi', 'item'): 13},
                    # metagraph=[('brand', 'item', 'bi'), ('item', 'brand', 'ib'), ('item', 'category', 'ic'), ('item', 'user', 'iu'), ('item', 'view', 'iv'), ('category', 'item', 'ci'), ('user', 'item', 'ui'), ('view', 'item', 'vi')])
        train_loader,        #Dataloader:2    dataset={Mydataset:189}  triple ={Tensor:(189,3)}   tensor([[ 214, 2070,    1],
                                                                                                        # [ 799,  624,    0],
                                                                                                        # [3504, 2399,    1],
                                                                                                        # [3371, 2037,    0],
                                                                                                        # [1320, 2616,    1],
                                                                                                        # [ 387, 1170,    1],
                                                                                                        # [ 217, 2070,    1],   ）
        eval_loader,             #Dataloader:1      dataset={Mydataset:63}  triple ={Tensor:(63,3)}     tensor([[6156, 1769,    1],
                                                                                                            # [1822,  709,    0],
                                                                                                            # [5127, 1430,    0],
                                                                                                            # [  40, 2070,    1],
        test_loader,             #Dataloader:1     dataset={Mydataset:64}  triple ={Tensor:(64,3)}   tensor([[  97,  430,    0],
                                                                                                            # [5375,  883,    0],
                                                                                                            # [4379, 2645,    1],
                                                                                                            # [1070, 1769,    1],
        meta_paths,            #dict    {'user': [['ui', 'iu']], 'item': [['iu', 'ui'], ['ic', 'ci'], ['ib', 'bi'], ['iv', 'vi']]}
        user_key,             #str:user
        item_key,             #str:item
    )
