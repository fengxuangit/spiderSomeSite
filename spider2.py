#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib2
import csv
import os
import sys
import threading
from bs4 import BeautifulSoup

#gridView_sgdw$ctl23$ctl00$ctl05=4
#http://221.224.251.251/SZConsProTradingCenterINWPage/Web_Cxzq/Cxzq_Sgdw_Jbxx.aspx?qyID=32050100000002504
class Spider:
	conn = None
	header = {"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0"}
	data = None
	numurl = "http://www.szcetc.com.cn/SZConsProTradingCenterINWPage/Web_Cxzq/Cxzq_Sgdw_List.aspx"
	def __init__(self):
		with open('/Users/apple/code/test/post.conf') as f:
			self.data = f.read()

	def post(self, num):
		datas = "{0}gridView_sgdw$ctl23$ctl00$ctl05={1}".format(self.data, num)
		req = urllib2.Request(self.numurl, data=datas)
		req.add_header('User-Agent', self.header)
		html = urllib2.urlopen(req)
		result = html.read().decode('utf-8')
		html.close()
		return result

	def get(self, url):
		print "[!] spider {0}".format(url)
		req = urllib2.Request(url)
		req.add_header('User-Agent', self.header)
		result = urllib2.urlopen(req).read()
		return result.decode('utf-8')

	def GetPageList(self, num):
		soup = BeautifulSoup(self.post(num), "lxml")
		result = []
		for line in soup.find_all('a'):
			if line['href'].startswith('http://'):
				result.append(line['href'].replace('View', 'Jbxx'))
		print "[!]Get Page List ok!  "
		return result

	def SoupHtml(self, html):
		soup = BeautifulSoup(html, "lxml")
		spans = soup.find_all("span")
		label = soup.find("label", id="DBText34").text
		text = []
		for sp in spans:
			text.append(sp.text.encode('utf-8'))
		text.append(label.encode('utf-8'))
		print "[*] soup html complete! "
		self.Write2Excel(text)

	def Gethtml(self, result):
		for line in result:
			html = self.SoupHtml(self.get(line))
			

	def Write2Excel(self, rows):
		csvfile = csv.writer(file('/Users/apple/code/test/result.csv', 'ab'))
		csvfile.writerow(rows)
		print "[*] wirte csv file ok !  \n"

	def main(self):
		for num in range(1, 274):
			lists = self.GetPageList(num)
			self.Gethtml(lists)
			break


if __name__ == '__main__':
	a = Spider()
	sys.exit(a.main())