from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

# OSM_FILE = "data/san-francisco_california.osm"  # Replace this with your osm file
# SAMPLE_FILE = "data/san-francisco_california_sample.osm"
OSM_FILE = "data/hangzhou_china.osm"  # Replace this with your osm file
SAMPLE_FILE = "data/hangzhou_china_sample.osm"
# SAMPLE_SF_FILE = "data/san-francisco_california_sample.osm"

k = 1000 # Parameter: take every k-th top level element

class MongoConnect(object):
    """docstring for MongoConnect."""
    def __init__(self):
        super(MongoConnect, self).__init__()
        self.client = MongoClient("mongodb://myapi:abc1234@127.0.0.1/apiDB")
        self.db = self.client['apiDB']

    def get_one(self):
        ''' 查询一条数据 '''
        return self.db.sanfrancisco.find_one()

    def add_one(self,item):
        ''' 新增数据 '''
        return self.db.sanfrancisco.insert_one(item)

    # data overview
    def count_all(self):
        ''' 查询一条数据 '''
        return self.db.sanfrancisco.count()

    def count_by_type(self,type):
        return self.db.sanfrancisco.find({'type':type}).count()

    def count_unique_users(self):
        return self.db.sanfrancisco.distinct('created.user').length

    # def count_unique_users(self):
    #     return self.db.sanfrancisco.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
    #     {"$sort":{"count":1}}, {"$limit":1}])



class GetSample(object):
    """docstring for GetSample."""
    def __init__(self):
        super(GetSample, self).__init__()

    def get_element(self,OSM_FILE, tags=('node', 'way', 'relation')):
        context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag in tags:
                yield elem
                root.clear()

    def save_sample(self):
        print(SAMPLE_FILE)
        with open(SAMPLE_FILE, 'wb') as output:
            output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n',encoding='utf-8'))
            output.write(bytes('<osm>\n  ',encoding='utf-8'))

            # Write every kth top level element
            for i, element in enumerate(self.get_element(OSM_FILE)):
                if i % k == 0:
                    output.write(ET.tostring(element, encoding='utf-8'))
            output.write(bytes('</osm>',encoding='utf-8'))

    def to_json(self,i, element):

        # if i % k == 0:
        # 处理node/way/realations等标签属性
        data = {'type':element.tag}
        value =element.attrib
        temp = {}
        pos = [0,0]
        for key in value:
            if key == 'lat':
                pos[0]= value[key]
            elif key == 'lon':
                pos[1]= value[key]
            else :
                temp[key] = value[key]
        data['created'] = temp
        if pos!= [0,0]:
            data['pos'] = pos

        # 处理标签内二级标签
        for item in element.iter("tag"):
            # print(item.tag)
            if item.tag == 'tag':
                kv = item.attrib
                # print(item.attrib)
                # 是否是: 分割字符串
                isColon = self.is_colon(kv['k'])
                if isColon:
                    if isColon[0] in data:
                        if type(data[isColon[0]])== type('string'):
                            # print(data[isColon[0]])
                            data[isColon[0]] = {
                                'default': data[isColon[0]],
                                isColon[1] : kv['v']
                            }
                        else:
                            temp= data[isColon[0]].copy()
                            temp[isColon[1]] = kv['v']
                            print(temp)
                            data[isColon[0]] = temp
                    else:
                        data[isColon[0]] = {
                            isColon[1] : kv['v']
                        }
                else:
                    data[kv['k']] = kv['v']

        # print(data)
        return data
        data = {}

    def is_colon(self, testiment):
        rest = testiment.split(':')
        if len(rest) > 1:
            return rest
        else:
            return False


    # def commbine_colon_string(self, target):
    #     target



def main():
    # print('hello')
    # obj = MongoConnect()
    # rest  = obj.get_one()
    # print(rest)

    getSample = GetSample()

    getSample.save_sample()

    # for i, element in enumerate(getSample.get_element(SAMPLE_SF_FILE)):
    #     item = getSample.to_json(i, element)
    #     # if i == 7:
    #     obj.add_one(item)
    #     # print('----')
    # print(obj.count_all())




if __name__ == '__main__':
    main()
