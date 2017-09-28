# OpenStreetMap Project : Data Wrangling with MongoDB

** Author: TANG Haoxiang**

** Date: 2017/09/30 **

---

> Map Area: San Francisco, United States**  
> https://www.openstreetmap.org/relation/111968  
> https://mapzen.com/data/metro-extracts/metro/san-francisco_california/

## Syllabus

1. Make goals
2. Procedure of importing data
3. Problems Encountered in the Map
    - Over­abbreviated Street Names
    - Postal Codes
4. Data Overview
5. Additional Ideas
    - Contributor statistics and gamification suggestion
    - Additional data exploration using MongoDB
6. Conclusion

---

#### 1. 明确项目目的

1) 将osm内数据进行筛选，清洗，最终导入到数据库内。


#### 1. Problems Encountered in the Map
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
