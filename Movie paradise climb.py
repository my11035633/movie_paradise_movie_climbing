from lxml import etree
import requests

HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}
URL_BASE="https://www.dy2018.com/"

#获得当前页下面的所有电影标题的href
def get_url_detail(url):
    response=requests.get(url,headers=HEADERS)
    text=response.text
    html=etree.HTML(text)
    urls=html.xpath("//table[@class='tbspan']//a[@class='ulink']/@href")
    for url in urls:    #剔除多余的href链接
        if url=="/html/gndy/jddy/"or url=="/html/gndy/dyzz/":
            urls.remove(url)
    url_hrefs=map(lambda url:URL_BASE+url,urls)  #返回迭代器，需要for循环拿出每个url链接
    return url_hrefs

#获得电影详情信息
def detail_url(url_detail):
    movie = {}
    response = requests.get(url_detail, headers=HEADERS)
    text = response.content.decode("gbk")
    html = etree.HTML(text)
    images = html.xpath("//div[@id='Zoom']//img/@src")
    Movie_poster = images[0]
    Movie_capture = images[1]
    movie["Movie_poster"] = Movie_poster
    movie["Movie_capture"] = Movie_capture
    infors= html.xpath("//div[@id='Zoom']//p/text()")    #电影详细信息，是将每行信息作为一个元素放到列表中
    actors=[]
    for index,infor in enumerate(infors): #infor代表一个电影的一行信息，枚举便于后续的演员信息提取
        if infor.startswith("◎片　　名"):
            name=infor.replace("◎片　　名","").strip()
            movie["name"]=name
        elif infor.startswith("◎年　　代"):
            s=infor.replace("◎年　　代","").strip()
            movie["s"]=s
        elif infor.startswith("◎产　　地"):
            address=infor.replace("◎产　　地","").strip()
            movie["address"]=address
        elif infor.startswith("◎上映日期"):
            release_time=infor.replace("◎上映日期","").strip()
            movie["release_time"]=release_time
        elif infor.startswith("◎豆瓣评分"):
            score=infor.replace("◎豆瓣评分","").strip()
            movie["score"]=score
        elif infor.startswith("◎导　　演"):
            director=infor.replace("◎导　　演","").strip()
            movie["director"]=director
        elif infor.startswith("◎主　　演　"):
            actor=infor.replace("◎主　　演　","").strip()
            actors.append(actor)
            for x in range(index+1,100):    #这里用枚举从上一个位置之后开始循环取出演员信息，因为直接判断以什么开头行不通了
                actor_name=infors[x].strip()
                if actor_name.startswith("◎"):
                    break
                else:
                    actors.append(actor_name)
            movie["actor"]=actors
    Dowload_link = html.xpath("//tbody//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie["Dowload_link"]=Dowload_link
    return movie

#主函数
def get_infor():
    base_url="https://www.dy2018.com/4/index_{}.html"
    for x in range(2,10):  #用来取多少也数据
        url=base_url.format(x)
        url_hrefs=get_url_detail(url)   #拿出当前页面下所有href
        for url_detail in url_hrefs:
            movie=detail_url(url_detail)  #调用函数拿到一个电影的所有详情
            print(movie)



if __name__=="__main__":
    get_infor()

#步骤：
    #格式化字符串拿到多页url，然后对其for循环，调用函数拿到每个url页面下所有的电影url
    #再对电影的url进行for循环，进入电影详情页面，拿到一页的所有电影信息





