import nxppy, webbrowser, requests, time
# Matching IP material
ips = {'ULTR': '192.168.43.16',
       'FLEX': '192.168.43.16',
       'PETG': '192.168.43.17'}

mifare=nxppy.Mifare()
oldData = ''
oldIp = ''
lastTime = 0


def switchOff(ip):
    if ip != '':
        print "switch off "+ip
        try:
            requests.get("http://"+ip+"/gpio/0")
        except Exception, e:
            print "request error %s", e
            pass

while True:
    try:
        mifare.select()
        #print "read NFC"
        data = mifare.read_block(7)
        #print "Read data "+data + " oldData "+oldData
        if data != oldData:
            lastTime = 0
            print "New tag "+data
            #print "Read reset lastTime "+str(lastTime)
            # switch off previous led
            if oldIp != ips[data]:
                switchOff(oldIp)
            #if oldIp != '':
            #    print "switch off "+oldIp
            #    requests.get("http://"+oldIp+"/gpio/0")
            oldData = data
            oldIp = ips[data]
        #   webbrowser.open("http://addlab.decathlon.net?mat=" + data, 0, True)
        #    webbrowser.open("http://192.168.43.16/gpio/1")
            #print ips[data]
            requests.get("http://"+ips[data]+"/gpio/1")
            
         #   requests.get(192.168.43.16/gpio/1")
        
    except nxppy.SelectError:
        # if no NFC since 30 secs stop last led
        #print "Error lastTime "+str(lastTime)
        if lastTime == 0:
            lastTime = time.time()
            #print "init lastime "+ str(lastTime)
            
        currentTime = time.time()
        #print "Error time difference" + str(currentTime-lastTime)
        if currentTime-lastTime > 3 and oldIp != '':
            #print "stop "+str(currentTime)+ " "+str(currentTime-lastTime)
            switchOff(oldIp)
            oldIp = ''
        oldData = ''
        data = ''
        pass   
    except Exception, e:
        print "unexpected error %s", e
        pass   

