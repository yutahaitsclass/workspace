# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

# 入力設定
id=input('調べたいid(@なし)：')
follow=input('調べたいのは？1.フォロー,2.フォロワー (1 or 2)：')
while int(follow)!=1 and int(follow)!=2:
    print('Please type 1 or 2')
    follow=input('調べたいのは？1.フォロー,2.フォロワー (1 or 2)：')
if int(follow)==1:
    follow='following'
elif int(follow)==2:
    follow='followers'


# スクレイピング開始
n=1
more='/'+id+'/'+follow
url='https://mobile.twitter.com'+more
html = requests.get(url)
soup = BeautifulSoup(html.content,'lxml')
file=id+'_'+follow+'.csv'
print(f'\n【START】\n出力ファイル：{file}\n\nスクレイピング中...(時間かかるよ)')
with open(file,  mode='w', encoding='utf-8') as f:
    f_c = csv.writer(f, lineterminator='\n')
    f_c.writerow(['Nmber', '名前', 'id','プロフィール'])
    while more !=None:
        followers_td=soup.findAll('td',class_="info fifty screenname")
        for follower in followers_td:
            url='https://mobile.twitter.com/'+follower.a["name"]
            html = requests.get(url)
            soup = BeautifulSoup(html.content,'lxml')
            comment=soup.find('div',class_='dir-ltr')
            if comment!=None:
                f_c.writerow([n, follower.strong.text, f'@{follower.a["name"]}',comment.text])
            else:
                f_c.writerow([n, follower.strong.text, f'@{follower.a["name"]}','NONE'])
            n+=1
        url='https://mobile.twitter.com'+more
        print(f'{n-20}~{n-1}-------------------------------------------\n{url}')
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'lxml')
        div = soup.find('div',class_='w-button-more')
        sleep(25)
        if div!= None:
            more=div.a.get('href')
        else:
            more=None
print('FINISH ALL')