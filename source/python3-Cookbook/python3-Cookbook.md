# Python3-Cookbook



## 第六章：数据编码和处理

### 6.1读写csv数据
#### 问题：
你想读写一个cvs格式的文件

#### 解决方案：

**可以使用<font color=red>csv</font>库:**

例如：假设你在一个名叫stocks.csv文件中有一些股票市场数据，就像这样：

```cvs
Symbol,Price,Date,Time,Change,Volume
"AA",39.48,"6/11/2007","9:36am",-0.18,181800
"AIG",71.38,"6/11/2007","9:36am",-0.15,195500
"AXP",62.58,"6/11/2007","9:36am",-0.46,935000
"BA",98.31,"6/11/2007","9:36am",+0.12,104800
"C",53.08,"6/11/2007","9:36am",-0.25,360900
"CAT",78.29,"6/11/2007","9:36am",-0.23,225400
```

将这些数据读取为一个元组的序列：

```python
def read_csv():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        for row in f_csv:
            print(row)
```



**使用命名元祖来访问：**

```python
def read_csv_namedtuple():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        Row = namedtuple('Row', headers)
        for r in f_csv:
            row = Row(*r)
            print(row.Symbol)
```

它允许你使用列名如 <font color=red>row.Symbol</font>和 <font color=red>row.Change</font> 代替下标访问。需要注意的是这个只有在列名是合法的Python标识符的时候才生效。如果不是的话， 你可能需要修改下原始的列名(如将非标识符字符替换成下划线之类的)。



**将数据读取到一个字典序列中：**

```python
def read_csv_dict():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.DictReader(f)
    	for row in f_csv:
            print(row['Symbol'])
```



**写入csv数据：**

仍然可以使用csv模块，不过这时候先创建一个<font color=red>writer</font>对象。例如：

```python
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
         ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]

with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
```

如果你有一个字典序列的数据，可以像这样做：

```python
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]

with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
```



**讨论：**

csv产生的数据都是字符串类型的，它不会做任何其他类型的转换。 如果你需要做这样的类型转换，你必须自己手动去实现。

下面是一个在CSV数据上执行其他类型转换的例子：

```python
def read_csv_typeConversion():
    col_types = [str, float, str, str, float, int]
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        for row in f_csv:
            # Apply conversions to the rows
            row = tuple(convert(value) for convert, value in zip(col_types, row))
            print(row)

# 打印信息：
['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800)
('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500)
('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000)
('BA', 98.31, '6/11/2007', '9:36am', 0.12, 104800)
('C', 53.08, '6/11/2007', '9:36am', -0.25, 360900)
('CAT', 78.29, '6/11/2007', '9:36am', -0.23, 225400)
```



最后，如果你读取CSV数据的目的是做数据分析和统计的话， 你可能需要看一看 `Pandas`包。`Pandas` 包含了一个非常方便的函数叫 `pandas.read_csv()` ， 它可以加载CSV数据到一个 `DataFrame` 对象中去。 然后利用这个对象你就可以生成各种形式的统计、过滤数据以及执行其他高级操作了




### 6.2 读写json数据
#### 问题：

你想读写JSON(JavaScript Object Notation)编码格式的数据

#### 解决方案：

<font color=red>json:</font> 字体 模块提供了一种很简单的方式来编码和解码JSON数据

**处理字符串，两个主要的函数：**

* <font color=red>json.dumps():</font>将一个Python数据结构转换为JSON
* <font color=red>json.loads():</font>将一个JSON编码的字符串转换回一个Python数据结构

* 例子：

  ```python
  # 将一个Python数据结构转换为JSON
  import json
  
  data = {
      'name' : 'ACME',
      'shares' : 100,
      'price' : 542.23
  }
  
  json_str = json.dumps(data)
  
  # 将一个JSON编码的字符串转换回一个Python数据结构
  data = json.loads(json_str)
  ```


**处理文件，两个主要的函数：**

* <font color=red>json.dumps()</font>
* <font color=red>json.loads()</font>

* 例子：

  ```python
  # Writing JSON data
  with open('data.json', 'w') as f:
      json.dump(data, f)
  
  # Reading data back
  with open('data.json', 'r') as f:
      data = json.load(f)
  ```

#### 讨论：

**json编码支持的基本数据类型：**

* <font color=red>None, bool, int, float,str</font>

* 及包含这些数据类型的<font color=red>lists,tuples,dictionaries</font> （ 对于dictionaries，keys需要是字符串类型(字典中任何非字符串类型的key在编码时会先转换为字符串)）


**json编码的格式对于Python语法而已几乎是完全一样的:**

下面是一个例子，演示了编码后的字符串效果：

```python
>>> json.dumps(False)
'false'
>>> d = {'a': True,
...     'b': 'Hello',
...     'c': None}
>>> json.dumps(d)
'{"b": "Hello", "c": null, "a": true}'
>>>
```

**json的打印：**

可以考虑使用pprint模块的<font color=red>pprint()</font>函数来代替普通的<font color=red>print()</font>函数。它可以按照字母顺序并以一种更加美观的方式输出。

下面是一个演示如何漂亮的打印输出Twitter上搜索结果的例子:

```python
>>> from urllib.request import urlopen
>>> import json
>>> u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
>>> resp = json.loads(u.read().decode('utf-8'))
>>> from pprint import pprint
>>> pprint(resp)
{'completed_in': 0.074,
'max_id': 264043230692245504,
'max_id_str': '264043230692245504',
'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
'page': 1,
'query': 'python',
'refresh_url': '?since_id=264043230692245504&q=python',
'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
            'from_user': ...
            }
            {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
            'from_user': ...
            }],
'results_per_page': 5,
'since_id': 0,
'since_id_str': '0'}
>>>
```



**json解析成对象：**

通常，json解码会根据提供的数据创建dicts或lists。不过可以通过<font color=red>json.loads()</font>传递<font color=red>object_pairs_hook</font>或<font color=red>object_hook</font>参数，来<font color=red>创建其他类型的对象</font>。

例如，下面是演示如何解码JSON数据并在一个OrderedDict中保留其顺序的例子：

```python
>>> s = '{"name": "ACME", "shares": 50, "price": 490.1}'
>>> from collections import OrderedDict
>>> data = json.loads(s, object_pairs_hook=OrderedDict)
>>> data
OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])
>>>
```



下面是如何将一个JSON字典转换为一个Python对象例子：

````python
>>> class JSONObject:
...     def __init__(self, d):
...         self.__dict__ = d
...
>>>
>>> data = json.loads(s, object_hook=JSONObject)
>>> data.name
'ACME'
>>> data.shares
50
>>> data.price
490.1
>>>
````



**序列化：**

看不大懂，暂时先不研究



