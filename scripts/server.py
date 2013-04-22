from socket import *
import thread
import serial
import logging
import sys
import RPi.GPIO as GPIO

ser = serial.Serial()
ser.port = "/dev/ttyACM0"
ser.baudrate = 9600
ser.open()

def response(key):
    return 'Server response: ' + key

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)

	data.strip('\n')
	data.strip('\r')

	obj, cmd = data.split(":",1)

	#print 'obj:' + str(obj) + ' cmd:' + str(cmd)
 
        if not data: break

        print str(addr) + ' recv:' + str(data)

	if obj == "moveRobot" or obj == "moveTurret":
		print str(obj) + ':' + str(cmd)
		ser.write(chr(int(cmd)))
				



        clientsock.send(response(data))
        print repr(addr) + ' sent:' + repr(response(data))
        if "close" == data.rstrip(): break # type 'close' on client console to close connection from the server side

    clientsock.close()
    print addr, "- closed connection" #log on console

if __name__=='__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)

    GPIO.output(11,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(15,GPIO.HIGH)
    
    BUFF =4096
    HOST = ''# must be input parameter @TODO
    PORT = 1234 # must be input parameter @TODO
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    #serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind((ADDR))
    serversock.listen(5)
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))
