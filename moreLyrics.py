""" 
1. 	loop thru a to z
2. 	loop thur 1-N: http://www.songlyrics.com/a/[1,..N]:
		<a href="/a/2/" title="Page 3">3</a>
3. 	find all artist in http://www.songlyrics.com/a/1: 
			<a href="http://www.songlyrics.com/a-b-the-sea-lyrics/" title="A B &amp; The Sea Lyrics">A B &amp; The Sea</a> 
4.	check an artist page: to see if it has Genre
		<p>Genre: <a href="http://www.songlyrics.com/rock-lyrics.php" title="Rock Lyrics">Rock</a></p>
		if assinged genre info, then check each song:
			<a href="http://www.songlyrics.com/a-balladeer/mary-had-a-secret-lyrics/" title="Mary Had A Secret Lyrics A Balladeer">Mary Had A Secret</a>
"""
# to exit:   	ctrl + shift + \ 
import urllib2, requests, re,io
from bs4 import BeautifulSoup as BS
from url2string import url2string
import time, MySQLdb
#=====================================================================================================================================
char='/a'			# query the page: http://www.songlyrics.com/a/
insertDB=True
# TABLE NAME HAS FIXED TO lyrics_a_to_z in cursor.execute(). Need to update therein manually
if insertDB:	
	dataBaseName ='lyrics'
	#tableName='lyrics_a_to_z'
	db = MySQLdb.connect(host='localhost', user='root',passwd='?????', db=dataBaseName)
	cursor = db.cursor()
#=====================================================================================================================================
def get_Artist_Title_Genre_Lyric(link='http://www.songlyrics.com/adele/someone-like-you-lyrics/'):
	ans=url2string(link)
	return link.rsplit('/')[-3], link.rsplit('/')[-2][:-7], ans[0],ans[1]
#=====================================================================================================================================
baseURL='http://www.songlyrics.com'
charURL=baseURL+char
r = requests.get(charURL)
soup = BS(r.content)
pageCharID=[]
pageCharID.append(baseURL+char)
#for page in soup.find_all('a',title=re.compile('Page \d*'), href=re.compile('\/a\/\d*')): 
	#print page['href']
	#pageCharID.append(baseURL+page['href'])
for page in soup.find_all('a',title=re.compile('Page \d*'), href=re.compile('\/'+char[1]+'\/\d*')):
	print page['href']
	pageCharID.append(baseURL+page['href'])
#=====================================================================================================================================
# now quote each page, e.g. http://www.songlyrics.com/a/1, to find all artist in the page:
#=====================================================================================================================================
artistList=[]
print("get artist url")
for id, i in enumerate(pageCharID):
	print("Processing {} page".format(id))
	r = requests.get(i)
	soup = BS(r.content)
	for artistURL in soup.find_all('a',title=True, href=re.compile('http\:\/\/www\.songlyrics\.com\/.+\-lyrics\/')):
		artist=artistURL['href']
		artistList.append(artist)
print("--------Got {} of artists.------".format(len(artistList)))
#=====================================================================================================================================
# now check each artist
filename='lyrics_'+char[1]
myfile=open(filename,'a')
for t, artistURL in enumerate(artistList):
	print("Processing artist {}".format(t))
	# check if the artist has assigned genre
	try:# query an artist
		r = requests.get(artistURL)
		soup = BS(r.content)
		i = soup.find('a',href=re.compile('http\:\/\/www\.songlyrics\.com\/.+\-lyrics\.php'))	
		# not empty if the artist has genre assigned
		if i is not None and len(i)==1:	# artist has genre
			print("artist #: {}, name: {}, genre: {}.".format(t, i['href'][25:-4],i.getText()))
			for (j, link) in enumerate(soup.find_all('a', title=True, href=re.compile('http\:\/\/www.songlyrics\.com\/.+\/.+\-lyrics\/'))):
				try:# query a lyric 
					artist, title, genre, content = get_Artist_Title_Genre_Lyric(link['href'])		
					# extract lyric, and will give exception if there is no valid lyric field 
					print("artist={}, title={}, genre={}".format(artist, title, genre))
					myfile.write(content+'\n')
					if insertDB:
						cursor.execute("""INSERT INTO lyrics_a_to_z (artist, title, lyric, url, genre) VALUES (%s,%s,%s,%s, %s)""", 
					(artist, title, content, link['href'], genre))
					if t%10==0:
						db.commit()
				except:# lyric page connction error or no lyric field
					print "[lyric] connection Error -OR- no lyric filed" + link['href']
					pass
		else: # artist has no genre
			print("[Omitted],  artist={} : genre = Null".format(artistURL))
	
	except: # artist connection error
		print("[artist]={} : connection Error".format(artistURL))
		pass
myfile.close()
if insertDB:
	db.commit()
	
	
	
