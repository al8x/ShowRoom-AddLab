import nxppy
import random
import string
import cherrypy
import os 

mifare=nxppy.Mifare()


class DisplayUID(object):
    @cherrypy.expose
    def index(self):
        return uid
    
while True:
    try:
        uid = mifare.select()
        print "Read uid", uid
        if __name__ == '__main__':
            cherrypy.quickstart(DisplayUID())
            os.startfile('index.html')
        
        
    except nxppy.SelectError:
        pass   

                 

