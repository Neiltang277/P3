# OpenStreetMap Project : Data Wrangling with MongoDB

** Author: TANG Haoxiang**

** Date: 2017/09/30 **

---

> Map Area: San Francisco, United States**  
> https://www.openstreetmap.org/relation/111968  
> https://mapzen.com/data/metro-extracts/metro/san-francisco_california/

## Syllabus

1. 制定目标
2. 数据导入流程
3. 遇到的问题
    - Python2 和 Python3的语法差异
    - 字典内部多层嵌套的操作
    - 数据标签的含义理解
    - 老版本数据的格式化
4. 数据概览
5. 补充问题分析
    - 建筑类型概览
    - 使用MongoDB操作的环节
6. 结论

---

#### 1. 明确项目目的

1) 将osm内数据进行筛选，清洗，最终导入到数据库内。
2) 根据已经导入的数据得到基本的数据仓库信息
3）利用已经导入的数据，提出假设，并通过数据分析操作得出结论

#### 2. 数据清洗，导入数据库流程

1） 生成Sample数据，通过对抽样数据的样本观察，归纳数据集合的规律
2） 尝试对当前样本数据进行操作，并将结果打印到控制台，观察抽样数据集合的筛选结果是否符合预期
3） 控制台打印数据如通过验收，则将样本数据导入到数据库内
4） 对数据的基本信息进行收集和整理，并尝试对样本数据库进行抽样检测
5） 样本数据库的数据集验收通过后，将测试数据集删除，正式对目标数据集进行操作
6） 对结果进行抽样检验，发现是否有数据库内数据是否存在问题你
7） 利用数据库对提出的问题进行分析



#### 3. Problems Encountered in the Map
1. python2 和python3的语法差异
1. dic.has_key()
可以替换成 if key in distinct

2. 关于子数组添加的问题



数据导入步骤
1. 了解osm数据结构
osm: 跟标签

node:
    tag: 对于该坐标点的描述, k为类型, v为值

way: 路的范围
    nd: 路的节点, ref属性为参考
    tag: 路的属性, k为类型, v为值

relations: 关联区域
    member: 子节点，
    tag: 区域属性

2. 数据录入
导入数据库的格式样例：
```
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
```

#### 3. Problems Encountered in the Map

1) name标签处理问题
1) 英文名 多个, 用/粉哥
2) 不同语种的名字

json二级字段的处理问题
重复复制, 判断

2)tiger标签, gnis标签
经过查询，tiger标签是一种早起由美国tiger数据库导入的标签，属于历史遗留标签，但是在07年之后逐渐在去除tiger标签的使用，但是在San Francisco数据库中依然存在多处使用tiger标签，

County FIPS code

More than one county in the US has a FIPS code of "001".

3) county标签
Santa Clara, CA

<tag k="addr:city" v="San Francisco" />
<tag k="addr:state" v="CA" />

<tag k="addr:state" v="ca" />


#### 4. Data Overview
**File sizes**
san-francisco_california.osm ...... 1.41 GB

###  Number of documents
```
> db.char.find().count()
1555851

```
### Number of nodes

```
> db.char.find({"type":"node"}).count()
1471349
```

### Number of wayss
```
> db.char.find({"type":"way"}).count()
84502
```

### Number of unique users
```
> db.char.distinct({"created.user"}).length
336
```

### Top 1 contributing user
```
> db.char.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
{"$sort":{"count":1}}, {"$limit":1}])
[ { "_id" : "jumbanho", "count" : 823324 } ]
```

#### 5. Additional Ideas


#### 6. Conclusion


---
## Reference:

2. **Mongodb documentation** : https://docs.mongodb.com/manual/reference/method/
3. **Pymongo documentation** : http://api.mongodb.com/python/current/tutorial.html
4. **Python documentation**: https://docs.python.org/3.6/contents.html
5. **OpenStreetMap**: http://www.openstreetmap.org/#map=17/36.95186/-79.04773
5. **Mapzen**: https://mapzen.com/data/metro-extracts/
1. **OpenStreetMap Wiki** : http://wiki.openstreetmap.org/wiki/Key:amenity
