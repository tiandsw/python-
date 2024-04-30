import requests
from lxml import etree
import pandas 

class Douban(object):
    def __init__(self) -> None:
        self.move = 'https://movie.douban.com/top250?start='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        self.df =pandas.DataFrame(columns=['电影top','链接','导演','上映日期','评分','评价人数','评论'])
    def get_page(self):
        newurl = [self.move + str(i) for i in range(0, 251, 25)]
        return newurl
    def get_text(self,list):
        try:
            return list[0].strip()
        except:
            return ''   
    
    def get_url(self,page):
        for i in page:            
            res=requests.get(url=i,headers=self.headers)
            yield res.content.decode('utf-8')
        
    def data(self,dat):
        count = 0
        for a in dat:
            data =etree.HTML(a)
            data=data.xpath('//*[@id="content"]/div/div[1]/ol/li')
            for all in data:
                movename=self.get_text(all.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
                link=self.get_text(all.xpath('./div/div[2]/div[1]/a/@href'))
                daoyan=self.get_text(all.xpath('./div/div[2]/div[2]/p[1]/text()[1]'))
                times=self.get_text(all.xpath('./div/div[2]/div[2]/p[1]/text()[2]'))
                socre=self.get_text(all.xpath('./div/div[2]/div[2]/div/span[2]/text()'))
                pingjia=self.get_text(all.xpath('./div/div[2]/div[2]/div/span[4]/text()'))
                inq=self.get_text(all.xpath('./div/div[2]/div[2]/p[2]/span/text()'))
                print(movename,link,daoyan,times,socre,pingjia,inq)
                self.df = pandas.concat([self.df, pandas.DataFrame({'电影top': [movename], '链接': [link], '导演': [daoyan], '上映日期': [times], '评分': [socre], '评价人数': [pingjia], '评论': [inq]})], ignore_index=True)
                # self.df = pandas.concat([movename,link,daoyan,times,socre,pingjia,inq])
                count +=1
                print(count)
    def excel(self,filename):
        self.df.to_excel(filename,index=False)
        
    def run(self):
        
    
        page=self.get_page()
        dat=self.get_url(page)
        self.data(dat)

if __name__ == '__main__':
    douban=Douban()
    douban.run()
    douban.excel('doubantop250.xlsx')
