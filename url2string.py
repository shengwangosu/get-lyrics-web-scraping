## parse a link url to lyrics in string
## only compatible with lyrics.com html format
## input: url of link
## return lyrics in string
import urllib2, requests, re
from bs4 import BeautifulSoup as BS

def url2string(pageLink):
	
	header_info={'User-Agent': 'My terminal'}
	req = requests.get(pageLink, headers=header_info)
	soup = BS(req.text)
	#lyrics = soup.find_all('div', {'class':re.compile('lyrics')})  	# for genius.om
	#lyrics = soup.find_all('pre', {'id':re.compile('lyric-body-text')}) 	# for lyrics.com
	# ===fetch genre====
	genre=soup.find('a',title=re.compile('.* Lyrics'), href=re.compile('http\:\/\/www.songlyrics\.com\/.+\-lyrics\.php')).getText()
	lyrics = soup.find_all('p', {'id':re.compile('songLyricsDiv')}) 	# for songlyrics.com
	# convert bs object to string
	lyrStr = str(lyrics)
	# remove tags and hyperlinks
	lyrStr=re.sub('<[^>]*>', '', lyrStr)		## remove tags
	lyrStr=re.sub('[\.\,]?(\\\\[rn])+', '. ', lyrStr)	## remove \\n and \\r
	lyrStr=re.sub(r'\\x\w[0-9]','',lyrStr)			#remove utf-8 code \\xe2 
	#lyrStr=re.sub('\[','',lyrStr)			## remove [
	#lyrStr=re.sub('\]','.',lyrStr)			## remove ] and add . at the end
	lyrStr=re.sub(r'\\u2019','\'',lyrStr)	# \u2019 = "
	lyrStr=re.sub(r'\\u2026',r'.',lyrStr)	# \u2026 = ...
	lyrStr=re.sub(r'\\u[0-9]{4}','',lyrStr)
	lyrStr=re.sub(r'\\u[0-9]{2}[a-z]{2}','',lyrStr)
	lyrStr=re.sub(r';br /&gt;','',lyrStr)
	lyrStr=re.sub(r'&lt','',lyrStr)
	lyrStr=re.sub('\.\s\.', '.',lyrStr)
	lyrStr=re.sub('\?\.','?',lyrStr)
	lyrStr=re.sub('(\.)?(\s)?\\u201[cd]','',lyrStr)
	lyrStr=re.sub(r'\\','',lyrStr)
	lyrStr=re.sub(r'\:\.',':',lyrStr)
	lyrStr=re.sub('\=+','',lyrStr)
	lyrStr=re.sub('\s+\.',r'.',lyrStr)
	lyrStr=re.sub('\.\:\.',r':',lyrStr)
	lyrStr=re.sub('\?\.',r'?',lyrStr)
	lyrStr=re.sub('\&(amp)?\;?',r'&',lyrStr)
	lyrStr=re.sub('[Tt]hanks to email.*for.*these lyrics\.*','',lyrStr)
	lyrStr=re.sub('Sorry, we have no.*lyrics at the moment.*\;\.','',lyrStr)
	lyrStr=re.sub('\/\/','',lyrStr)
	lyrStr=re.sub('\-+','',lyrStr)
	return genre, lyrStr[1:len(lyrStr)-1]


