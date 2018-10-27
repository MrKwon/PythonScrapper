# -*- coding: utf-8 -*-
# 검색 키워드에 맞게 뉴스 검색 결과를 따오는 스크래퍼

from urllib.parse import quote_plus
import urllib.request
from bs4 import BeautifulSoup, NavigableString
import re	# id가 sp로 시작하는 것들을 find 하기 위해 import
import csv	# csv파일로 저장하기 위해 import

# funct_declaration
# 언론사명의 글자 따오기 위한 함수
def get_string(parent):
	l = []
	for tag in parent:
		if isinstance(tag, NavigableString):
			l.append(tag.string)
		else:
			l.extend(get_string(tag))
		return l

# scrapper 함수, output은 '뉴스제목', '뉴스링크', '언론사명' 순으로 이루어진 list를 return
def crawl_info(Url):
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib.request.Request(Url, headers = hdr)
	html = urllib.request.urlopen(req)
	bsObj = BeautifulSoup(html, "html.parser")
	for li in bsObj.find("ul", {"class" : "type01"}).findAll("li", {"id" : re.compile('(sp)')}):
		link = li.find("dt").find("a")
		tmplist = [ link.text, get_string(li.find('dd'))[0], link['href'] ]
	return tmplist

# 검색 keyword를 이용하여 Url을 만들어주는 함수 3개(GetMainKey(), GetSubKey(), Url_form(str, list))
def GetMainKey():
	MainKey = input("main 키워드를 입력하세요 : ")
	return MainKey

def GetSubKey() :
	SubKeys = []
	print("sub 키워드를 입력하세요.(여러개인 경우 Enter로 구분, 더 이상 없으면 입력 없이 Enter)")
	while True:
		ToGetKeyword = input()
		if ToGetKeyword != "":
			SubKeys.append(ToGetKeyword)
		else :
			print("주어진 키워드로 크롤링을 시작합니다.")
			return SubKeys

def Url_form(keyword, word_list):
	#keyword(띄어쓰기가 있는 index에는 +을 넣어 대체하여 저장)
	Key4Url = keyword.replace(' ', '+')
	#word_list의 항목 하나하나를 변환
	ind = 0
	string4list = []
	string4list.append(Key4Url)
	while ind < len(word_list):
		Sub4Url = "+\""+word_list[ind]+"\""
		Sub4Url = Sub4Url.replace(' ', '+')
		string4list.append(Sub4Url)
		ind += 1
	#최종적으로 url 형식에 맞게 return, 아직 맨 뒤에 바뀌어야 될 페이지 숫자는 없음
	return "https://search.naver.com/search.naver?&where=news&query=" +quote_plus(''.join(string4list))+ "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=34&start="

#pagenum 수정이 필요해서 만든 함수
def ControlPagenum(url, pagenum):
	return url + str(pagenum)

#출력파일경로와 파일명을 지정할 수 있는 함수


# main_body
filename = input("출력 파일 명을 지정해주세요 (________.csv) : ")

csvFile = open("C:"+ filename + ".csv", 'w+', encoding = 'euc-kr')
writer = csv.writer(csvFile)

#사용자로부터 Keyword를 입력받는 부분
MainKeyword = GetMainKey()
SubKeywords = GetSubKey()
print("main키워드 : " + MainKeyword)
print("sub키워드 : " + ', '.join(SubKeywords))

tmpurl = Url_form(MainKeyword, SubKeywords)

try:
	print("진행중 입니다. 기다려주세요. \n ############ ctrl + c 입력시 중단 및 종료 ###########")
	writer.writerow(('title', 'press', 'url'))
	page_num = 1
	while page_num < 3992 : # 검색결과는 4000개까지 보여줌
		if page_num == 1:
			crawlurl = ControlPagenum(tmpurl, page_num)
			tmprow = crawl_info(crawlurl)
		else :
			crawlurl = ControlPagenum(tmpurl, page_num)
			tmprow = crawl_info(crawlurl)
		page_num_str = str(page_num + 10)
		print("[" + page_num_str[0 : len(page_num_str) - 1] + "] 페이지 진행중")
		writer.writerow(tmprow)
		page_num += 10	# page_num은 10단위로 바뀌므로 10을 계속 더해준다.

finally:
	print("크롤링 완료!")
	print("파일은 Scrapper.py 가 속한 디렉터리에 [" + filename + ".csv] 로 저장됩니다.")
	csvFile.close()
	inputToEnter = input("Enter 입력시 종료됩니다.")

