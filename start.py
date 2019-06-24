'''
	Simple socket server using threads
'''

import socket
import sys
import time
import os

# import thread module
import threading

HOST = '35.234.112.150'  # Symbolic name, meaning all available interfaces
PORT = 5006  # Arbitrary non-privileged port
FILE_PORT = 5005  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fileSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


fileName = "video_038.mp4"
statinfo = os.stat(fileName)
fileSize = statinfo.st_size

print 'Command Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind COMMAND failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Command Socket created'

# Bind socket to local host and port
try:
    fileSocket.bind((HOST, FILE_PORT))
except socket.error as msg:
    print 'Bind FILES failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
fileSocket.listen(10)
print 'Socket now listening'

def getDeviceInfo():
    conn.send('getDeviceInfo\r\n')
    #time.sleep(2)
    conn.send('{\"sku\":\"78186\",\"serialNumber\":781024227,\"softwareVersion\":\"00.00.012\",\"hardwareVersion\":\"AFD006.002\",\"magnification\":1.0,\"APIVersion\":2,\"Parameters\":{\"Brightness\":{\"mode\":\"rw\",\"min\":0,\"max\":20,\"step\":1},\"Contrast\":{\"mode\":\"rw\",\"min\":0,\"max\":20,\"step\":1},\"RecMode\":{\"mode\":\"rw\",\"values\":[0,1]},\"Units\":{\"mode\":\"rw\",\"values\":[0,1]},\"AutoOff\":{\"mode\":\"rw\",\"values\":[0,1,2,3]},\"Language\":{\"mode\":\"rw\",\"values\":[0,1,2,3,4]},\"TimeFormat\":{\"mode\":\"rw\",\"values\":[0,1]},\"DateTime\":\"yyyy-mm-ddHH:MM:SS\",\"IR\":{\"mode\":\"rw\",\"min\":0,\"max\":3000,\"step\":1000},\"AccessLevel\":{\"mode\":\"ro\",\"values\":[0,1]},\"Battery\":{\"mode\":\"ro\",\"min\":0,\"max\":100,\"step\":1},\"ExtDC\":{\"mode\":\"ro\",\"values\":[0,1]},\"IRStatus\":{\"mode\":\"ro\",\"values\":[0,1,2]},\"RecStatus\":{\"mode\":\"ro\",\"min\":0,\"max\":1,\"step\":1},\"RecTime\":{\"mode\":\"ro\",\"min\":0,\"max\":350,\"step\":1}},\"Commands\":[\"start_video\",\"pause_video\",\"stop_video\",\"snapshot\",\"fw_update\",\"format\",\"factory_reset\",\"download\",\"delete\",\"ls\",\"stop_operation\"],\"Events\":[\"ev_saved_videofile\",\"ev_saved_snapshot\",\"ev_removed_file\",\"ev_access_media\",\"ev_disk_almost_full\"]}\r\n')
    #time.sleep(2)

def getParams():
    conn.send('getParams\r\n')
    #time.sleep(2)
    conn.send('{\"Parameters\":{\"Brightness\":10,\"Contrast\":10,\"RecMode\":1,\"IR\":0,\"TimeFormat\":0,\"DateTime\":\"2019-04-1515:43:18\",\"Units\":0,\"AutoOff\":3,\"Language\":0,\"AccessLevel\":0,\"Battery\":88,\"ExtDC\":0,\"IRStatus\":1,\"RecStatus\":1,\"RecTime\":118}}\r\n')
    #time.sleep(2)

def getFolderList():
    conn.send('ls?path=1:/\r\n')
    #time.sleep(2)
    conn.send('{\"curdir\":\"1:/\",\"filelist\":[{\"folder\":\"img_0000\",\"size\":0,\"date\":\"28.07.13 00:00\"}]}\r\n')
    #time.sleep(2)

def getFileList():
    conn.send('ls\r\n')
    #time.sleep(2)
    conn.send('{\"curdir\":\"1:/img_0000\",\"filelist\":[{\"file\":\"video_001.avi\",\"size\":' + str(fileSize) + ',\"date\":\"14.01.16 07:54\"}]}\r\n')
    #time.sleep(2)

def handleCommand(command):
    if 'getDeviceInfo' in command:
        getDeviceInfo()
    elif 'getParams' in command:
        getParams()
    elif 'ls?path=1:/img_0000' in command:
        getFileList()
    elif 'ls?path=1:/' in command:
        getFolderList()
    elif 'ls' in command:
        getFileList()
    elif 'download?path=1:/img_0000/video_001.avi' in command:
        conn.send('download\r\nOK\r\n')
    else:
        return False
    return True

def handleFiles(filesSocket):
    print 'FILES W8 CLIENT'

    while 1:
        conn, addr = filesSocket.accept()
        print 'FILES CLIENT OK'

        f = open(fileName, "r")
        leftBytes = fileSize

        while leftBytes:
            bytes = f.read(8192)

            if conn:
                try:
                    send = conn.send(bytes)
                except:
                    leftBytes = 0
            else:
                leftBytes = 0

            leftBytes -= send
            #print 'left bytes'
            #print leftBytes

        print 'File client closed'


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()

    t = threading.Thread(target=handleFiles, args=(fileSocket,))
    t.daemon = True
    t.start()

    while 1:
        print 'READ COMMAND'
        command = conn.recv(100)

        print command
        if not handleCommand(command):
            print 'FAIL'
            break
    break

s.close()