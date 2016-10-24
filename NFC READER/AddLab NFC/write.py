import nxppy
mifare=nxppy.Mifare()

while True:
    try:
        uid = mifare.select()
        print "Read uid", uid
        mifare.write_block(7,'abc_')

    except nxppy.SelectError:
        pass   
