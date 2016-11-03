#!/usr/bin/python
import time, csv
import nxppy, webbrowser, requests, time
#import  webbrowser, requests, time

# fonction qui gere l'affichage en fonction du debug.
def printDebug(wstring):
   if jeDebug==1:
      print wstring


## chenillard
def chenillard(nbLedSimultane,lesUrl,temps):
   printDebug('-- Debut chenillard')
   nbLedOn=0
   for cpt in range(len(lesUrl)):        # je demarre le chenillard
      if nbLedOn >= nbLedSimultane:
	 switchLed(lesUrl[cpt-nbLedSimultane],"0")   # j'eteind la led si trop de led allume.
	 nbLedOn=nbLedOn-1
      switchLed(lesUrl[cpt],'1')         # j'allume la led
      nbLedOn=nbLedOn+1
      time.sleep(tempsLedChenillard)
   printDebug('test--------------')
   for cpt in range(nbLedSimultane,0,-1): # j'eteind les led restante
      switchLed(lesUrl[len(lesUrl)-cpt],'0')
      time.sleep(tempsLedChenillard)

# je switch une led en on ou off.
# attention pour l'alimentation je gere un nombre maximum de led simultanees
def switchLed(ip, state):
   global ledHigh
   global ledHighMax
   if ip != '':
      #je limite le nombre de led allumes simultanement.
      if state=='1':
	 try:
	     if len(ledHigh)==ledHighMax:
		switchLed(ledHigh[0],'0')
		#ledHigh=ledHigh[1:]
		ledHigh.pop(0)
	 except Exception, e:
	    pass
         print ledHigh
         ledHigh.append(ip)  # je memorise que j'allume la Led
      try:
  	 printDebug("switch led "+ip+ " state " +state)
	 requests.get("http://"+ip+"/"+state)
      except Exception, e:
	 printDebug("request error %s" +str(e))
	 pass

###############################################################################"
########
########
########
###############################################################################"


# j'initialise mes variable

oldData = ''
oldIp = ''
lastTime = 0
#ledHigh = 0
jeDebug=1                 # 1 = debug
detect=0

tempsLedChenillard=1      # temps (sleep) entre 2 operation de chenillard
tempsAutoStop=10
ledHighMax=2              # nombre de led max que je peux laisser allume (securite)
ledHigh=[]                # pour memoriser les led allumes


## j'importe les filaprintDebugments ainsi au les url associees
listUrl=[]
ips={}
with open('list.csv') as f:
    i=+1
    reader= dict(filter(None, csv.reader(f)))




# pour faire le chenillard en fonction de l'adresse, j'ai besoin de memoriser toutes les URL
for matiere,url  in reader.items():
   printDebug(matiere + " - " + url)
   ips[matiere] =url
   try:
    	listUrl.index(url)
   except Exception, e: # l'url n'existe pas dans la liste, je l'ajoute.
	listUrl.append(url)
# je trie ma lite d'url
listUrl=sorted(listUrl)


printDebug("----- chenillard")
#chenillard(3,listUrl,2)
printDebug("------------------")


mifare=nxppy.Mifare()
while True:
    time.sleep(0.2)
    #tant que je ne presente pas de badge nfc, je boucle sur l'erreur.
    try:
        mifare.select()
        #print "read NFC"
        data = mifare.read_block(7)
        #printDebug ("Read data "+data + " oldData "+oldData)
    except nxppy.SelectError: # s'il n'y a pas de badge
        data = ''
        pass
    except Exception, e:  # si la lecteur du badge s'est mal passee.
        data = ''
        printDebug(e)
        pass


    if data == '':
        if lastTime == 0:
            lastTime = time.time()
        if time.time()-lastTime > tempsAutoStop and detect==1:
            printDebug('temps atteint j eteind la led')
            switchLed(oldIp,'0')
            oldData = ''
            detect=0
            oldIp = ''
    else:
        if data != oldData:
            detect=1
            lastTime = 0
            switchLed(oldIp,'0')
            try:
                print "open browser"
                #webbrowser.open("http://addlab.decathlon.net?mat=" + data, 0, True)
                printDebug(" j affiche url http://addlab.decathlon.net?mat=" + data)
            except Exception, e:
                printDebug("1 " +e)
                pass
            switchLed(ips[data],'1')
            lastTime = 0
            oldData = data
            oldIp = ips[data]
        else:
            if data == oldData:
                lastTime = 0
