import xlrd
from pyecharts import WordCloud, Pie, Parallel, Bar3D


def excel2dict(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    keys = sheet.row_values(0)
    result = {}
    for i in range(1, sheet.nrows):
        for j in range(len(keys)):
            item = keys[j]
            if item not in result:
                result[item] = []
            result[item].append(sheet.row_values(i)[j])
    return keys, result


headers, data = excel2dict(r"D:\personal\projects\HLZK_IMDBCrawler\data\2018年科幻出版图书汇总.xlsx")

# data["作者"] = [item.split("/") for item in data["作者"]]
# result = {}
# for i in range(len(data["作者"])):
#     item = data["作者"][i]
#     if data['是否有早期版本'][i] == '':# and data["来自国家/地区"][i] == '中国':
#         for author in item:
#             if author not in result and author != '饶忠华':
#                 result[author] = 0
#             if author != '饶忠华':
#                 result[author] += 1
# name = [key for key in result]
# value = [result[key] for key in result]
# wordcloud = WordCloud(width = 1280, height = 720)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()


# result = {}
# for region in data['来自国家/地区']:
#     if region != '中国' and region not in result:
#         result[region] = 0
#     if region != '中国':
#         result[region] += 1
# name = [key for key in result]
# print(name)
# value = [result[key] for key in result]
# wordcloud = WordCloud(width = 1280, height = 720)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()

# data["主题"] = [item.split("/") for item in data["主题"]]
# result = {}
# for item in data["主题"]:
#     for theme in item:
#         if theme not in result and theme != '':
#             result[theme] = 0
#         if theme != '':
#             result[theme] += 1
# name = [key for key in result]
# value = [result[key] for key in result]
# wordcloud = WordCloud(width = 1280, height = 720)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()

# data["译者"] = [item.split("/") for item in data["译者"]]
# result = {}
# for item in data["译者"]:
#     for translator in item:
#         if translator not in result and translator != '':
#             result[translator] = 0
#         if translator != '':
#             result[translator] += 1
# name = [key for key in result]
# value = [result[key] for key in result]
# wordcloud = WordCloud(width = 1920, height = 1080)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()

# result = {}
# for item in data["图书类型"]:
#     if item not in result and item != '':
#         result[item] = 0
#     if item != '':
#         result[item] += 1
# name = [key for key in result]
# value = [result[key] for key in result]
# wordcloud = WordCloud(width = 1280, height = 720)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()

# data["出版社"] = [item.split("/") for item in data["出版社"]]
# count_publisher = {}
# for i in range(len(data["出版社"])):
#     item = data["出版社"][i]
#     if data["出品方"][i] == '':
#         for publisher in item:
#             if publisher not in count_publisher and publisher != '':
#                 count_publisher[publisher] = 0
#             if publisher != '':
#                 count_publisher[publisher] += 1
# name = [key for key in count_publisher]
# value = [count_publisher[key] for key in count_publisher]
# wordcloud = WordCloud(width = 1920, height = 1080)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()
#
# data["出品方"] = [item.split("/") for item in data["出品方"]]
# count_producer = {}
# for item in data["出品方"]:
#     for producer in item:
#         if producer not in count_producer and producer != '':
#             count_producer[producer] = 0
#         if producer != '':
#             count_producer[producer] += 1
# name = [key for key in count_producer]
# value = [count_producer[key] for key in count_producer]
# wordcloud = WordCloud(width = 1280, height = 720)
# wordcloud.add("", name, value, shape = "circle", word_size_range = [10, 100])
# wordcloud.render()
#
# # data["出版社"] = [item.replace("\xa0", "").replace(" ", "").replace("\t", "").replace("|", "").split("/") for item in data["出版社"]]
# # data["出品方"] = [item.replace("\xa0", "").replace(" ", "").replace("\t", "").replace("|", "").split("/") for item in data["出品方"]]
# result = {}
# for i in range(len(data["出版社"])):
#     for j in range(len(data["出版社"][i])):
#         for k in range(len(data["出品方"][i])):
#             if data["出版社"][i][j] != '' and data["出品方"][i][k] != '':
#                 if data["出版社"][i][j] not in result:
#                     result[data["出版社"][i][j]] = {}
#                 if data["出品方"][i][k] not in result[data["出版社"][i][j]]:
#                     result[data["出版社"][i][j]][data["出品方"][i][k]] = 0
#                 result[data["出版社"][i][j]][data["出品方"][i][k]] += 10
# nodes = [key for key in result]
# categories = ["出版社" for key in result]
# links = []
# for publisher in result:
#     for producer in result[publisher]:
#         if producer not in nodes:
#             nodes.append(producer)
#             categories.append("出品方")
#         links.append({"source": publisher, "target": producer, "value": 25 - result[publisher][producer]})
# nodes = [{"name": node, "symbolSize": 10} for node in nodes]
# for i in range(len(categories)):
#     nodes[i]["category"] = {"出版社": 0, "出品方": 1}[categories[i]]
#     if categories[i] == '出版社':
#         nodes[i]["symbolSize"] = 10
#     else:
#         nodes[i]["symbolSize"] = count_producer[nodes[i]["name"]] + 10
# categories = ["出版社", "出品方"]
#
# print(nodes)
# print(links)
# print(categories)
#
# from pyecharts import Graph
#
# graph = Graph(width = 1920, height = 1080)
# graph.add(
#     "",
#     nodes,
#     links,
#     categories = categories,
#     label_pos="right",
#     graph_repulsion = 500,
#     is_legend_show = False,
#     is_label_show = True
# )
# graph.render()

def discretion(number):
    if number >= 5000:
        return "≥5000"
    if 1000 <= number <5000:
        return "1000~5000"
    if 500 <= number < 1000:
        return "500~1000"
    if 100 <= number < 500:
        return "100~500"
    return "<100"


name = [discretion(number) for number in [0, 100, 500, 1000, 5000]]
result = {}
for n in name:
    result[n] = 0
for number in data["总关注人数"]:
    result[discretion(int(number))] += 1

name = [key for key in result]
value = [result[key] for key in result]

from pyecharts import Pie
pie = Pie()
pie.add("", name, value, is_label_show = True)
pie.show_config()
pie.render()