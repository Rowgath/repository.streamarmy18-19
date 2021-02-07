#########################################
############CODE BY @NEMZZY668, DEOBFUSCATION BY ROWGATH###########
#########################################
import urllib,os,re,sys,json,requests,resolveurl
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
from bs4 import BeautifulSoup
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
#########################################
addon_id            = 'plugin.video.fanime'
selfAddon           = xbmcaddon.Addon(id=addon_id)
AddonTitle          = '[COLOR magenta][B]FANime[/COLOR][/B]'
Addonfanart         = translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
Addonicon           = translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
AddonDesc           = '[COLOR magenta][B]FANime Was Created By @Nemzzy668 ( Follow On Twitter )[/COLOR][/B]'
dialog              = xbmcgui.Dialog()
#########################################
def GetMenu():
	addDir('[COLOR magenta][B]Recent Releases[/COLOR][/B]','https://www5.gogoanimehub.tv/anime-list.html',2,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]A to Z[/COLOR][/B]','https://www5.gogoanimehub.tv/anime-list.html',3,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]Genres[/COLOR][/B]','https://www5.gogoanimehub.tv/',5,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]New Seasons[/COLOR][/B]','https://www5.gogoanimehub.tv/new-season.html',6,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]Ongoing Series[/COLOR][/B]','https://www5.gogoanimehub.tv/',7,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]Recently Added Series[/COLOR][/B]','https://www5.gogoanimehub.tv/',8,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]Movies[/COLOR][/B]','https://www5.gogoanimehub.tv/anime-movies.html',6,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR magenta][B]Popular[/COLOR][/B]','https://www5.gogoanimehub.tv/popular.html',6,Addonicon,Addonfanart,AddonDesc)
	addDir('[COLOR aqua][B]SEARCH[/COLOR][/B]','url',9,Addonicon,Addonfanart,AddonDesc)
def Search():
	string =''
	SearchUrl = ('https://www5.gogoanimehub.tv///search.html?keyword=%s')
	keyboard = xbmc.Keyboard(string, '[COLOR magenta][B]What Would You Like To Search For?[/B][/COLOR]')
	keyboard.doModal()
	if keyboard.isConfirmed():
		string = keyboard.getText()
		if len(string)>1:
			string = string.replace(' ','-')
			Search = (SearchUrl %string)
			MainContent(Search)
		else: dialog.notification(AddonTitle, '[COLOR gold]No Term Entered[/COLOR]', Addonicon, 2500)
	else: dialog.notification(AddonTitle, '[COLOR gold]Search Cancelled[/COLOR]', Addonicon, 2500)
def Recent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find('nav', class_={'menu_recent'})
	base_domain = 'https://www5.gogoanimehub.tv/'
	for i in data.find_all('li'):
		name = i.a['title']
		name = name.encode("utf8") if PY2 else name
		url2 = i.a['href']
		url2 = base_domain+url2 if url2.startswith('/') else url2
		icon = i.find('div', class_={'thumbnail-recent'})
		icon = re.findall(r'''(http.*?)['"]''',str(icon))[0]
		epi = i.p.text
		epi = epi.encode("utf8") if PY2 else epi
		addDir('[COLOR magenta][B]%s | %s[/COLOR][/B]' % (name,epi),url2,20,icon,Addonfanart,description='')
def ATOZ(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find_all('li', class_={'first-char'})
	base_domain = 'https://www5.gogoanimehub.tv/'
	for i in data:
		name = i.a.text
		url2 = i.a['href']
		url2 = base_domain+url2 if url2.startswith('/') else url2
		addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,4,Addonicon,Addonfanart,AddonDesc)
def ATOZContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	if not '?page=' in url: url = ('%s?page=1' %url)
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find('ul', class_={'listing'})
	base_domain = 'https://www5.gogoanimehub.tv/'
	for i in data:
		try:
			name = i.a['title']
			if name =='': name = i.a.text
			name = name.encode("utf8") if PY2 else name
			url2 = i.a['href']
			url2 = base_domain+url2 if url2.startswith('/') else url2
			try: icon = re.findall(r'''img\s+src=['"](.*?)['"]''',str(i))[0]
			except: icon = Addonicon
			addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,10,icon,Addonfanart,AddonDesc)
		except: pass
	try:
		Getpage = url.split('?page=')[1]
		BasePage = url.split('?page=')[0]
		GenNext = int(Getpage) + 1
		NextPage = ('%s?page=%s' %(BasePage,GenNext))
		addDir('[COLOR gold][B]Next Page -->[/COLOR][/B]',NextPage,4,Addonicon,Addonfanart,'Next Page')
	except: pass
def GetShowContent(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	base_domain = 'https://www5.gogoanimehub.tv/'
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	try: ShowIcon = soup.find("meta",  property="og:image")['content']
	except: ShowIcon = Addonicon
	ShowDescription = soup.find_all('p', class_={'type'})
	DescText = ''
	EpiID = re.findall(r'''value=['"](.*?)['"]\sid=['"]movie_id''',link)[0]
	AjaxUrl = ('https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=1&ep_end=1000&id=%s' % EpiID)
	for d in ShowDescription:
		try:
			DescText = DescText + d.text+('\n')
		except: DescText = 'No Description Available'
		DescText = DescText.encode("utf8") if PY2 else DescText
	GetEpisodes = requests.get(AjaxUrl,headers=headers).text
	soup2 = BeautifulSoup(GetEpisodes,'html.parser')
	content = soup2.find_all('a')
	for i in content:
		name = i.text
		name = name.replace('\n',' ').strip()
		name = name.encode("utf8") if PY2 else name
		url2 = i['href'].strip()
		url2 = base_domain+url2 if url2.startswith('/') else url2
		addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,20,ShowIcon,Addonfanart,DescText)
def Genre(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	base_domain = 'https://www5.gogoanimehub.tv/'
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find("li",  class_={'movie genre hide'})
	for i in data.find_all('a'):
		try:
			name = i['title']
			name = name.encode("utf8") if PY2 else name
			url2 = i['href']
			url2 = base_domain+url2 if url2.startswith('/') else url2
			addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,6,Addonicon,Addonfanart,AddonDesc)
		except: pass
def MainContent(url):
	name = ''
	if not '?page=' in url and not 'search.html' in url: url = ('%s?page=1' %url)
	if 'search.html' in url and not '&page=' in url: url = ('%s&page=1' %url)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	base_domain = 'https://www5.gogoanimehub.tv/'
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find("ul",  class_={'items'})
	for i in data.find_all('li'):
		name = i.a['title']
		name = name.encode("utf8") if PY2 else name
		url2 = i.a['href']
		url2 = base_domain+url2 if url2.startswith('/') else url2
		icon = i.img['src']
		addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,10,icon,Addonfanart,description='')
	try:
		Getpage = url.split('?page=')[1]
		BasePage = url.split('?page=')[0]
		GenNext = int(Getpage) + 1
		NextPage = ('%s?page=%s' %(BasePage,GenNext))
		addDir('[COLOR gold][B]Next Page -->[/COLOR][/B]',NextPage,6,Addonicon,Addonfanart,'Next Page')
	except: pass
	if 'search.html' in url:
		try:
			Getpage = url.split('&page=')[1]
			BasePage = url.split('&page=')[0]
			GenNext = int(Getpage) + 1
			NextPage = ('%s&page=%s' %(BasePage,GenNext))
			addDir('[COLOR gold][B]Next Page -->[/COLOR][/B]',NextPage,6,Addonicon,Addonfanart,'Next Page')
		except: pass
	if 'search.html' in url and name == '':
		name = 'Sorry No Items Found'
		addLink('[COLOR magenta][B]%s[/COLOR][/B]' % name,'url2',9999,Addonicon,Addonfanart,description='')
def OnGoing(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	base_domain = 'https://www5.gogoanimehub.tv/'
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find("div",  class_={'overview'})
	for i in data.find_all('li'):
		name = i.a['title']
		name = name.encode("utf8") if PY2 else name
		url2 = i.a['href']
		url2 = base_domain+url2 if url2.startswith('/') else url2
		addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,10,Addonicon,Addonfanart,description='')
def RecentlyAdded(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	base_domain = 'https://www5.gogoanimehub.tv/'
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find("div",  class_={'added_series_body final'})
	for i in data.find_all('li'):
		name = i.a['title']
		name = name.encode("utf8") if PY2 else name
		url2 = i.a['href']
		url2 = base_domain+url2 if url2.startswith('/') else url2
		addDir('[COLOR magenta][B]%s[/COLOR][/B]' % name,url2,10,Addonicon,Addonfanart,description='')
def LinkGetter(name,url,iconimage,description):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	link = requests.get(url,headers=headers).text
	soup = BeautifulSoup(link,'html.parser')
	data = soup.find('div', class_={'anime_muti_link'})
	found = 0
	for i in data.find_all('a'):
		sources = i['data-video']
		sources = 'https:'+sources if sources.startswith('//') else sources
		if resolveurl.HostedMediaFile(sources):
			found += 1
			name = ('Source %s' % found)
			addLink('[COLOR magenta][B]%s[/COLOR][/B]' % name,sources,99,iconimage,Addonfanart,description)
def PLAYLINK(name,link,iconimage):
	dialog.notification(AddonTitle, '[COLOR yellow]Hunting Link Now Be Patient[/COLOR]', Addonicon, 2500)
	try:
		hmf = resolveurl.HostedMediaFile(url)
		if hmf.valid_url(): link = hmf.resolve()
		if not 'user-agent' in link.lower(): link = link+'|User-Agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=link))
		quit()
	except Exception as e:
		dialog.notification(AddonTitle,"[B][COLOR yellow]%s[/B][/COLOR]" % e,Addonicon,5000)
		quit()

def addDir(name,url,mode,iconimage,fanart,description=''):
	u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({"thumb": iconimage})
	liz.setInfo('video', {'Plot': description})
	view=xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
def addLink(name, url, mode, iconimage, fanart, description='',family=''):
	u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({"thumb": iconimage})
	liz.setInfo('video', {'Plot': description})
	liz.setProperty('IsPlayable', 'true')
	StartParty="%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(url), '3000', quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
	liz.addContextMenuItems([('[COLOR yellow][B]Start A Watch Party For %s[/COLOR]' %name, 'xbmc.RunPlugin('+StartParty+')')])
	view=xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
def addStandardLink(name, url, mode, iconimage, fanart, description,family=''):
	if not description: description = ''
	u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({"thumb": iconimage})
	liz.setInfo('video', {'Plot': description})
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
def Pin():
	pin = selfAddon.getSetting('pin')
	if pin == '': pin = 'EXPIRED'
	if pin == 'EXPIRED':
		selfAddon.setSetting('pinused','False')
		dialog.ok(AddonTitle,"[COLOR yellow]NEW SITE NO MORE POP UPS! Please visit [COLOR lime]https://pinsystem.co.uk[COLOR yellow] to generate an Access Token For [COLOR magenta]FANime[COLOR yellow] then enter it after clicking ok[/COLOR]")
		string =''
		keyboard = xbmc.Keyboard(string, '[COLOR red]Please Enter Pin Generated From Website(Case Sensitive)[/COLOR]')
		keyboard.doModal()
		if keyboard.isConfirmed():
			string = keyboard.getText()
			if len(string)>1:
				term = string.title()
				selfAddon.setSetting('pin',term)
				Pin()
			else: quit()
		else:
			quit()
	if not 'EXPIRED' in pin:
		pinurlcheck = ('https://pinsystem.co.uk/service.php?code=%s&plugin=RnVja1lvdSE' % pin)
		link = requests.get(pinurlcheck).text
		if len(link) <=2 or 'Pin Expired' in link:
			selfAddon.setSetting('pin','EXPIRED')
			Pin()
		else:
			registerpin = selfAddon.getSetting('pinused')
			if registerpin == 'False':
				try:
					requests.get('https://pinsystem.co.uk/checker.php?code=99999&plugin=FANime').text
					selfAddon.setSetting('pinused','True')
				except: pass
			else: pass
params = dict(parse_qsl(sys.argv[2].replace("?", "")))
site = params.get("site", "0")
url = params.get("url", "0")
name = params.get("name", "0")
mode = int(params.get("mode", "0"))
iconimage = params.get("iconimage", "0")
fanart = params.get("fanart", "0")
description = params.get("description", "0")
Pin()

if mode==0 or url=="0" or len(url)<1: GetMenu()
elif mode==1:GetContent(name,url,iconimage,fanart)
elif mode==2:Recent(url)
elif mode==3:ATOZ(url)
elif mode==4:ATOZContent(url)
elif mode==5:Genre(url)
elif mode==6:MainContent(url)
elif mode==7:OnGoing(url)
elif mode==8:RecentlyAdded(url)
elif mode==9:Search()
elif mode==10:GetShowContent(url)
elif mode==20:LinkGetter(name,url,iconimage,description)
elif mode==99:PLAYLINK(name,url,iconimage)
if mode==None or url==None or len(url)<1: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
else: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)
