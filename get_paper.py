import datetime
import requests
import pandas as pd
import json
import os




def get_em_industry():
    url = "http://reportapi.eastmoney.com/report/list?"
    today=datetime.date.today().strftime('%Y-%m-%d')
    #cb=datatable8267652&industryCode=*&pageSize=50&industry=*&rating=*&ratingChange=*&beginTime=2018-11-20&endTime=2020-11-20&pageNo=1&fields=&qType=1&orgCode=&rcode=&_=1605853063297"
    params = {
    "cb": "datatable8267652",
    "industryCode": "*",
    "pageSize": "5000",
    "industry": "*",
    "rating": "*",
    "ratingChange": "*",
    "beginTime": "2018-11-20",
    "endTime":today,
    "pageNo":1,
    "fields":"",
    "qType":1,
    "orgCode":"",
    "rcode":"",
    "_":1607865418961,
    }
    
   
        
    r = requests.get(url, params=params)
    if r.status_code==200:
        data_json = json.loads(r.text[r.text.find("(")+1:-1])
        temp_df = pd.DataFrame(data_json['data'])
        return temp_df


    else:
        print('抓取网页出错',r.status_code)

def short_date(date):
    return date[:10]
        
if __name__ == "__main__":
    df=get_em_industry()
    df['publishDate']=df['publishDate'].apply(short_date)
    
    
    serverJ = os.environ['PUSH_KEY']
    api = "https://sc.ftqq.com/{}.send".format(serverJ)
    publishDate = df[['publishDate','title']].to_dict()['publishDate'][0]
    content = df[['publishDate','title']].to_dict()['title'].values()
    str_text=''
    for text in content:
        str_text=str_text+';'+text
    data = {
       "text":publishDate,
       "desp":text
        
       }
   
    req = requests.post(api,data = data)
