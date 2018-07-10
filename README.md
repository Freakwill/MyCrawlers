# MyCrawlers
My Crawlers for Movies、Information、Encyclopedia...


## jiani

A module for fetching information of movies from douban.

A girl who named Jiani asked me to help her to write a program fetching information of moives from douban. So far, she has not mastered the skill of programming. She said it is important for her, since she will get a job with the program after graduate. She really needs it. I do not know how to reject a girl's request, but I hope that she can learn coding. Hence, I develope the module and named it jiani.

The code is simple (or naive) anyway. It will be improved if I get more skills.


### Requirement

    wordcloud
    jieba
    

### Example
```python
    # at the beginning, you have to import requests and BeautifulSoup
    import jiani
    url = DOUBAN_MOVIE_URL + '/subject/26816017'  # 居里夫人 Marie Curie -> url ???
    resp = requests.get(url, headers=header_dict)
    bs = BeautifulSoup(resp.content.decode('utf-8'), "lxml")
    movie = jiani.Movie.fromSoup(bs)
    print(movie)
    print(movie.stat())
    movie.wordCould()  # generate word cloud
```

![](https://github.com/Freakwill/MyCrawlers/blob/master/居里夫人%20Marie%20Curie(2016).png?raw=true)

I will try to define a mapping 'keyword -> urls' where urls are the result of searching with some keyword.

## baidupedia

a module for fetching information from baidu baike


## taobao

get products from taobao under certain conditions.
just run the file.

## pybrainyquote

get quotes from pybrainyquote

try it with `Quote.today()`

## myweb

It is just an excercise.


## zol

find information on http://detail.zol.com.cn

```python
iceboxes = IceBoxes.read_url()
df =pd.DataFrame([p.toDict() for p in iceboxes])
df.to_excel('iceboxes.xls')
```

![](https://github.com/Freakwill/MyCrawlers/blob/master/zol/icebox_price.png?raw=true)
