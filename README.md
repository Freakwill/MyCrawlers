# MyCrawlers
My Crawlers for Movies、Information、Encyclopedia...



## jiani

A module for fetching information of movies from douban.
A girl who named Jiani asked me to help her to write a program fetching information of moives from douban.
She said it is important for her, since she will have a job with the program. Hence, I name the module jiani.

The code is simple or naive anyway. It will be improved if I get more skills.


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

## baidupedia

a module for fetching information from baidu baike


## taobao

get products from taobao under certain conditions.
just run the file.
