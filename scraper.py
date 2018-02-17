python2
from __future__ import division
from bs4 import BeautifulSoup
from BeautifulSoup import SoupStrainer
import pandas as pd
import urllib,re,csv,os,urllib2,requests,itertools,pdfkit,time
import smtplib
import math
from selenium import webdriver
import requests.packages.urllib3
import requests
requests.packages.urllib3.disable_warnings()


start_time = time.time()

os.chdir('DIRECTORY')


orgs = []
smo_ids = []
terms = []
sites = []
year_start = []
year_end = []
year_i = []
numbers = range(100001)
numbers = numbers[0::200]
#headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

f = open("SEARCHDOC_1.csv",'rbU')
search = csv.reader(f,delimiter=',',quotechar='"')




################################################################################
#ARTICLE DOWNLOAD PROCEDURE
################################################################################



#use the 'AN() search column and YR() search column' column in each row of the csv file
for row in search:
	#org = row[1]
	#smo_id = row[0]
	#split years to read in each year as a separate search
	year = row[49]
	year = year.split('-')
	startyear = int(year[0])
	endyear = int(year[1])
	for year_studied in range(startyear,endyear+1):
		org = row[1]
		smo_id = row[0]
		fullsearchterm = "(" + row[48] + ")+AND+PUB(" + row[15] + ")+AND+DTYPE(" + row[16] + ")+AND+YR(" + str(year_studied) + ")+AND+NOT+STYPE(" + row[18] + ")"
		url = "http://search.proquest.com/results/53e5e2824f3a3504PQ/1/$5bqueryType$3dbasic:OS$3b+sortType$3dDateAsc$3b+searchTerms$3d$5b$3cAND$7ccitationBodyTags:" + fullsearchterm + "$3e$5d$3b+searchParameters$3d$7bNAVIGATORS$3dnavsummarynav,sourcetypenav,pubtitlenav,objecttypenav,languagenav$28filter$3d200$2f0$2f*$29,decadenav$28filter$3d110$2f0$2f*,sort$3dname$2fascending$29,yearnav$28filter$3d1100$2f0$2f*,sort$3dname$2fascending$29,yearmonthnav$28filter$3d120$2f0$2f*,sort$3dname$2fascending$29,monthnav$28sort$3dname$2fascending$29,daynav$28sort$3dname$2fascending$29,+RS$3dOP,+chunkSize$3d20,+QT_PIPELINE$3denfrdees,+instance$3dprod.academic,+ftblock$3d740842+1+660848+670831+194104+194001+670829+194000+660843+660840+104,+removeDuplicates$3dtrue$7d$3b+metaData$3d$7bUsageSearchMode$3dQuickSearch,+dbselections$3darts$7cscience$7cliterature$7chealth$7cbusiness$7cdissertations$7cnews$7chistory$7csocialsciences$7c10000187,+SEARCH_ID_TIMESTAMP$3d1403677625474$7d$5d?accountid=USERID"
		orgs.append(org)
		smo_ids.append(smo_id)
		terms.append(fullsearchterm)
		sites.append(url)
		year_start.append(startyear)
		year_end.append(endyear)
		year_i.append(year_studied)


orgs.pop(0)
smo_ids.pop(0)
terms.pop(0)
sites.pop(0)
year_start.pop(0)
year_end.pop(0)
year_i.pop(0)

orgs.pop(0)
smo_ids.pop(0)
terms.pop(0)
sites.pop(0)
year_start.pop(0)
year_end.pop(0)
year_i.pop(0)



fulls = zip(orgs, terms, sites, smo_ids, year_i, year_start, year_end)




orgs2 = []
terms2 = []
sites2 = []
results2 = []
smo_ids2 = []
article_number = []
years2 = []


##########
#article numbers for download
##########

start_time = time.time()

startpoint = 1
for full in fulls:
	site = full[2]
	org = full[0]
	smo_id = full[3]
	term = full[1]
	year = full[4]
	driver = webdriver.Chrome("CHROMEDRIVER DIRECTORY") 
	driver.get(site) #get original site info
	source = driver.page_source
	#text = requests.get(site).text #text version of getting requests
	#soup = BeautifulSoup(text) #use text version to get site soup
	soup = BeautifulSoup(source, "html.parser")
	soup2 = soup.encode("utf-8")
	try:
		#resultno = re.findall('English</a><span class="resultscount"> (.*?)\xe2\x80\x8e</span>',soup2)
		#resultno = re.findall('<h1 id="pqResultsCount">\n(.*?) results\n</h1>',soup2)
		resultno = re.findall('<h1 id="pqResultsCount">\n(.*?) result',soup2)
		resultno = ''.join(resultno)
		resultno = resultno.translate(None, "(){}<>,")
		resultno = int(resultno)
	except ValueError, e:
		 resultno = int(0)
	no_pages = int(math.ceil(resultno/20))
	#encrypt = re.findall('href="https://search.proquest.com/docview/(.*?)/',soup2)
	an = re.findall('{"(.*?)markedlistcheckbox:markallitems',soup2)
	an = ''.join(an)
	an = re.findall('markAll":false,"formats":{(.*?)},"markURL"',an)
	an = ''.join(an)
	an = re.sub(r'":.+?,"', '', an)
	an = an.translate(None, '"')
	an = an.split(':', 1)[0]
	an = an.split('MSTAR_')
	an.pop(0)
	for i in an:
		article_number.append(i)
		years2.append(year)
		sites2.append(site)
		orgs2.append(org)
		smo_ids2.append(smo_id)
		terms2.append(term)
	#begin encryption search
	encrypt = re.findall('id="searchForm"(.*?)/></div>',soup2)
	encrypt = ''.join(encrypt)
	encrypt
	#t_ac = re.findall('<div class="t-invisible"><input name="t:ac" type="hidden" value="(.*?)/',encrypt)
	t_ac = re.findall('name="t:ac" type="hidden" value="(.*?)/',encrypt)
	t_ac = ''.join(t_ac)
	t_ac
	#if len(t_ac) == 0:
	#	t_ac = re.findall('name="t:ac" type="hidden" value="(.*?)/',encrypt)
	#	t_ac = ''.join(t_ac)
	#	t_ac
	t_formdata = re.findall('name="t:formdata" type="hidden" value="(.*?)"',encrypt)
	t_formdata = ''.join(t_formdata)
	t_formdata
	#start page 2 stuff
	for page in range(2,no_pages+1):
		site_ = "https://search.proquest.com/results.bottompagelinks:gotopage/" + str(page) + "?t:ac=" + t_ac + "/?t:formdata=" + t_formdata + ""
		#driver = webdriver.Chrome("/home/bvann/Downloads/chromedriver") 
		#driver.get(site) #get original site info
		driver.get(site_) #get subsequent page info
		source = driver.page_source # Here is your populated data for the page source
		#text_ = requests.get(source).text
		#text_
		#soup_ = BeautifulSoup(text_)
		soup_ = BeautifulSoup(source, "html.parser")
		soup2_ = soup_.encode("utf-8")
		an_ = re.findall('{"(.*?)markedlistcheckbox:markallitems',soup2_)
		an_ = ''.join(an_)
		an_ = re.findall('markAll":false,"formats":{(.*?)},"markURL"',an_)
		an_ = ''.join(an_)
		an_ = re.sub(r'":.+?,"', '', an_)
		an_ = an_.translate(None, '"')
		an_ = an_.split(':', 1)[0]
		an_ = an_.split('MSTAR_')
		an_.pop(0)
		for i_ in an_:
			article_number.append(i_)
			years2.append(year)
			sites2.append(site)
			orgs2.append(org)
			smo_ids2.append(smo_id)
			terms2.append(term)
	driver.quit()
	#last = _
	elapsed_time = time.time() - start_time
	#elapsed_time = elapsed_time/60
	#elapsed_time = int(elapsed_time)+((elapsed_time-int(elapsed_time))*.60)
	#print elapsed_time
	m, s = divmod(elapsed_time, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)
	print "%d: Page %d is complete" % (startpoint, startpoint)
	if startpoint in numbers:
		print "Sleeping for 60 seconds"
		time.sleep(60)
	startpoint += 1



article_info = zip(article_number, years2, sites2, orgs2, smo_ids2, terms2)


csvfile = "INFO.csv"


with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["Article Number", "Year", "Link to Article", "Organization", "SMO ID", "Search Terms"])
    writer.writerows(article_info)



##########
#article numbers into list
##########

g = open("INFO.csv",'rbU')
search2 = csv.reader(g,delimiter=',',quotechar='"')


artfinds_art = []
artfinds_yr = []
artfinds_art_term =[]
artfinds_yr_term = []
artfinds_url = []
artfinds_org = []

#for row in article_info:
for row in search2:
	article = row[0]
	yr = row[1]
	art_term = "AN(" + article + ")"
	yr_term = "YR(" + str(yr) + ")"
	url = "http://search.proquest.com/results/53e5e2824f3a3504PQ/1/$5bqueryType$3dbasic:OS$3b+sortType$3dDateAsc$3b+searchTerms$3d$5b$3cAND$7ccitationBodyTags:" + art_term + "+AND+" + yr_term + "$3e$5d$3b+searchParameters$3d$7bNAVIGATORS$3dnavsummarynav,sourcetypenav,pubtitlenav,objecttypenav,languagenav$28filter$3d200$2f0$2f*$29,decadenav$28filter$3d110$2f0$2f*,sort$3dname$2fascending$29,yearnav$28filter$3d1100$2f0$2f*,sort$3dname$2fascending$29,yearmonthnav$28filter$3d120$2f0$2f*,sort$3dname$2fascending$29,monthnav$28sort$3dname$2fascending$29,daynav$28sort$3dname$2fascending$29,+RS$3dOP,+chunkSize$3d20,+QT_PIPELINE$3denfrdees,+instance$3dprod.academic,+ftblock$3d740842+1+660848+670831+194104+194001+670829+194000+660843+660840+104,+removeDuplicates$3dtrue$7d$3b+metaData$3d$7bUsageSearchMode$3dQuickSearch,+dbselections$3darts$7cscience$7cliterature$7chealth$7cbusiness$7cdissertations$7cnews$7chistory$7csocialsciences$7c10000187,+SEARCH_ID_TIMESTAMP$3d1403677625474$7d$5d?accountid=UNC_USERID"
	org_a = row[3]
	artfinds_art.append(article)
	artfinds_yr.append(yr)
	artfinds_art_term.append(art_term)
	artfinds_yr_term.append(yr_term)
	artfinds_url.append(url)
	artfinds_org.append(org_a)


artfinds_art.pop(0)
artfinds_yr.pop(0)
artfinds_art_term.pop(0)
artfinds_yr_term.pop(0)
artfinds_url.pop(0)
artfinds_org.pop(0)

artfinds = zip(artfinds_url, artfinds_org, artfinds_yr_term, artfinds_art_term, artfinds_yr, artfinds_art)


##########
#article downloads
##########


newids3 = []
orgs3 = []
sites3 = []
years3 = []
art_titles3 = []
art_pages3 =[]
art_years3 =[]
art_locs3 = []
art_countries3 = []
art_sources3 = []
art_dates3 = []


start_time = time.time()
startpoint = 1
for row in artfinds:
	try:
		site = row[0]
		org = row[1]
		year = row[4]
		text = requests.get(site).text
		soup = BeautifulSoup(text, "html.parser")
		linktoABS = soup(id="addFlashPageParameterformat_fulltextPDF")[0]['href'] #go on page to find the text of the href linking to article
		#grab the new PQ ID
		ABS = linktoABS.encode("utf-8") #convert to plaintext
		list_id = re.findall('docview/(.*?)/fulltextPDF',ABS)
		newid = ",".join(str(x) for x in list_id)
		ABS2 = ABS.replace("fulltextPDF", "citation")
		ABS2 = requests.get(ABS2).text
		art_title = re.findall('citationDocTitleLink" title="(.*?)"',text)
		art_title = art_title[0].encode('ascii', 'ignore')
		art_page = re.findall('Pages </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
		art_page = ",".join(str(x) for x in art_page)
		art_year = re.findall('Publication year </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
		art_year = ",".join(str(x) for x in art_year)
		art_loc = re.findall('Place of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
		art_loc = ",".join(str(x) for x in art_loc)
		art_country = re.findall('Country of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
		art_country = ",".join(str(x) for x in art_country)
		art_source = re.findall('Database </div><div class="display_record_indexing_data">(.*?)</div></div>',ABS2)
		art_source = ",".join(str(x) for x in art_source)
		#no systematic publication date across articles, use year
		#art_date = re.findall('Adate=(.*?)&amp;ic',ABS2)
		#art_date = art_date.pop()
		#art_date = re.sub(r'%2C', ' ', art_date)
		#art_date = re.sub(r'\+', ' ', art_date)
		#art_date = re.sub(r'  ', ', ', art_date)
		#art_date = [str(x) for x in art_date.split(',')]
		#art_date = ",".join(str(x) for x in art_date)
		newid_url = "http://search.proquest.com/docview/" + newid + "/fulltextPDF/D41685BBFD384046PQ/1?accountid=UNC_USERID"
		text2 = requests.get(newid_url).text
		soup2 = BeautifulSoup(text2, "html.parser")
		linktoDL = soup2(id="downloadPDFLink")[0]['href']
		#download the PDF
		testfile=urllib.URLopener()
		testfile.retrieve(linktoDL, "downloads/" + org + "_" + newid + ".pdf")
		newids3.append(newid)
		orgs3.append(org)
		sites3.append(site)
		years3.append(year)
		art_titles3.append(art_title)
		art_pages3.append(art_page)
		art_years3.append(art_year)
		art_locs3.append(art_loc)
		art_countries3.append(art_country)
		art_sources3.append(art_source)
		#art_dates3.append(art_date)
		print "('downloads/%s_%s.pdf')" % (org, newid)
		#testfile.retrieve(linktoDL, org + "/" + org + "_" + newid + ".pdf")
	except IndexError, e:
		try:
			print(e)
			site = row[0]
			org = row[1]
			year = row[4]
			text = requests.get(site).text
			soup = BeautifulSoup(text, "html.parser")
			linktoABS = soup(id="addFlashPageParameterformat_fulltext")[0]['href']
			#grab the new PQ ID
			ABS = linktoABS.encode("utf-8")
			list_id = re.findall('docview/(.*?)/fulltext',ABS)
			newid = ",".join(str(x) for x in list_id)
			ABS2 = ABS.replace("fulltext", "citation")
			ABS2 = requests.get(ABS2).text
			art_title = re.findall('citationDocTitleLink" title="(.*?)"',text)
			art_title = art_title[0].encode('ascii', 'ignore')
			art_page = re.findall('Pages </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
			art_page = ",".join(str(x) for x in art_page)
			art_year = re.findall('Publication year </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
			art_year = ",".join(str(x) for x in art_year)
			art_loc = re.findall('Place of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
			art_loc = ",".join(str(x) for x in art_loc)
			art_country = re.findall('Country of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
			art_country = ",".join(str(x) for x in art_country)
			art_source = re.findall('Database </div><div class="display_record_indexing_data">(.*?)</div></div>',ABS2)
			art_source = ",".join(str(x) for x in art_source)
			#no systematic publication date across articles, use year
			#art_date = re.findall('Adate=(.*?)&amp;ic',ABS2)
			#art_date = art_date.pop()
			#art_date = re.sub(r'%2C', ' ', art_date)
			#art_date = re.sub(r'\+', ' ', art_date)
			#art_date = re.sub(r'  ', ', ', art_date)
			#art_date = [str(x) for x in art_date.split(',')]
			#art_date = ",".join(str(x) for x in art_date)
			newid_url = "http://search.proquest.com/docview/" + newid + "/fulltext/D41685BBFD384046PQ/1?accountid=UNC_USERID"
			#newids.append(newid)
			config = pdfkit.configuration(wkhtmltopdf='WKHTMLTOPDF DIRECTORY/main.py')
			pdfkit.from_url(newid_url, "downloads/" + org + "_" + newid + "_web.pdf")
			newids3.append(newid)
			orgs3.append(org)
			sites3.append(site)
			years3.append(year)
			art_titles3.append(art_title)
			art_pages3.append(art_page)
			art_years3.append(art_year)
			art_locs3.append(art_loc)
			art_countries3.append(art_country)
			art_sources3.append(art_source)
			#art_dates3.append(art_date)
			print "('downloads/%s_%s_web.pdf')" % (org, newid)
			#pdfkit.from_url(newid_url, org + "/" + org + "_" + newid + "_web.pdf")
			#print "('%s/%s_%s_abs.pdf')" % (org, org, newid)
		except IndexError, e:
			try:
		 		#print(e)
				site = row[0]
				org = row[1]
				year = row[4]
				text = requests.get(site).text
				soup = BeautifulSoup(text, "html.parser")
				linktoABS = soup(id="addFlashPageParameterformat_abstract")[0]['href']
				ABS = linktoABS.encode("utf-8")
				list_id = re.findall('docview/(.*?)/abstract',ABS)
				newid = ",".join(str(x) for x in list_id)
				ABS2 = ABS.replace("abstract", "citation")
				ABS2 = requests.get(ABS2).text
				art_title = re.findall('citationDocTitleLink" title="(.*?)"',text)
				art_title = art_title[0].encode('ascii', 'ignore')
				art_page = re.findall('Pages </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_page = ",".join(str(x) for x in art_page)
				art_year = re.findall('Publication year </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_year = ",".join(str(x) for x in art_year)
				art_loc = re.findall('Place of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_loc = ",".join(str(x) for x in art_loc)
				art_country = re.findall('Country of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_country = ",".join(str(x) for x in art_country)
				art_source = re.findall('Database </div><div class="display_record_indexing_data">(.*?)</div></div>',ABS2)
				art_source = ",".join(str(x) for x in art_source)
				#no systematic publication date across articles, use year
				#art_date = re.findall('Adate=(.*?)&amp;ic',ABS2)
				#art_date = art_date.pop()
				#art_date = re.sub(r'%2C', ' ', art_date)
				#art_date = re.sub(r'\+', ' ', art_date)
				#art_date = re.sub(r'  ', ', ', art_date)
				#art_date = [str(x) for x in art_date.split(',')]
				#art_date = ",".join(str(x) for x in art_date)
				newid_url = "http://search.proquest.com/docview/" + newid + "/abstract/D41685BBFD384046PQ/1?accountid=UNC_USERID"
				#newids.append(newid)
				config = pdfkit.configuration(wkhtmltopdf='WKHTMLTOPDF DIRECTORY/main.py')
				pdfkit.from_url(newid_url, "downloads/" + org + "_" + newid + "_abs.pdf")
				newids3.append(newid)
				orgs3.append(org)
				sites3.append(site)
				years3.append(year)
				art_titles3.append(art_title)
				art_pages3.append(art_page)
				art_years3.append(art_year)
				art_locs3.append(art_loc)
				art_countries3.append(art_country)
				art_sources3.append(art_source)
				print "('downloads/%s_%s_abs.pdf')" % (org, newid)
			except IndexError, e:
				#print(e)
			 	site = row[0]
				org = row[1]
				year = row[4]
				text = requests.get(site).text
				soup = BeautifulSoup(text)
				linktoABS = soup(id="addFlashPageParameterformat_citation")[0]['href']
				ABS = linktoABS.encode("utf-8")
				list_id = re.findall('docview/(.*?)/citation',ABS)
				newid = ",".join(str(x) for x in list_id)
				ABS2 = ABS.replace("citation", "citation")
				ABS2 = requests.get(ABS2).text
				art_title = re.findall('citationDocTitleLink" title="(.*?)"',text)
				art_title = art_title[0].encode('ascii', 'ignore')
				art_page = re.findall('Pages </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_page = ",".join(str(x) for x in art_page)
				art_year = re.findall('Publication year </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_year = ",".join(str(x) for x in art_year)
				art_loc = re.findall('Place of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_loc = ",".join(str(x) for x in art_loc)
				art_country = re.findall('Country of publication </div><div class="display_record_indexing_data"><span class="subjectField-postProcessingHook">(.*?)</span></div></div><div',ABS2)
				art_country = ",".join(str(x) for x in art_country)
				art_source = re.findall('Database </div><div class="display_record_indexing_data">(.*?)</div></div>',ABS2)
				art_source = ",".join(str(x) for x in art_source)
				#art_date = re.findall('Adate=(.*?)&amp;ic',ABS2)
				#art_date = art_date.pop()
				#art_date = re.sub(r'%2C', ' ', art_date)
				#art_date = re.sub(r'\+', ' ', art_date)
				#art_date = re.sub(r'  ', ', ', art_date)
				#art_date = [str(x) for x in art_date.split(',')]
				#art_date = ",".join(str(x) for x in art_date)
				newid_url = "http://search.proquest.com/docview/" + newid + "/citation/D41685BBFD384046PQ/1?accountid=UNC_USERID"
				newids3.append(newid)
				orgs3.append(org)
				sites3.append("NULL")
				years3.append(year)
				art_titles3.append(art_title)
				art_pages3.append(art_page)
				art_years3.append(art_year)
				art_locs3.append(art_loc)
				art_countries3.append(art_country)
				art_sources3.append(art_source)
				#art_dates3.append(art_date)
				print "('downloads/%s_%s_NULL.pdf')" % (org, newid)
	#last = _
	elapsed_time = time.time() - start_time
	#elapsed_time = elapsed_time/60
	#elapsed_time = int(elapsed_time)+((elapsed_time-int(elapsed_time))*.60)
	#print elapsed_time
	m, s = divmod(elapsed_time, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)
	print "%d: Number %d is complete" % (startpoint, startpoint)
	if startpoint in numbers:
		print "Sleeping for 60 seconds"
		time.sleep(60)
	startpoint += 1




#export a CSV file with the Old ID, the link to the website for the document, and the New ID

final = zip(art_titles3, orgs3, sites3, newids3, years3, art_years3, art_pages3, art_locs3, art_countries3, art_sources3)


csvfile = "DOWNLOADS.csv"


with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(["Article Titles", "Organization", "Link to Article", "New Proquest ID", "Year", "Article Year", "Pages", "Location", "Country", "News Source"])
    writer.writerows(final)














