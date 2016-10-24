import nxppy
mifare=nxppy.Mifare()

while True:
    try:
        uid = mifare.select()
        print "Read uid", uid
        for i in range(0,8):
            data = mifare.read_block(i)
            print "read data", data
        
    except nxppy.SelectError:
        pass   
