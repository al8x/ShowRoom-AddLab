import nxppy, webbrowser, requests, time
# Matching IP material
ips = {'ULTR': '192.168.43.16',
       'FLEX': '192.168.43.16',
       'PETG': '192.168.43.17'}

mifare=nxppy.Mifare()
oldData = ''
oldIp = ''
lastTime = 0
detect = 0

def switchLed(ip, state):
    if ip != '':
        print "switch led "+ip+ " state"+state
        try:
            requests.get("http://"+ip+"/gpio/"+state)
        except Exception, e:
            print "request error %s", e
            pass

while True:
    try:
        mifare.select()
        #print "read NFC"
        data = mifare.read_block(7)
        #print "Read data "+data + " oldData "+oldData
    except nxppy.SelectError:
        data = ''
        pass
    except Exception, e:
        data = ''
        pass

    if data == '':
        if lastTime == 0:
            lastTime = time.time()
        if time.time()-lastTime > 3 and detect==1:
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
            except Exception, e:    
                pass
            switchLed(ips[data],'1')
            lastTime = 0
            oldData = data
            oldIp = ips[data]
        else:
            if data == oldData:
                lastTime = 0
                
