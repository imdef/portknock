# 	https://github.com/samyk/pwnat
# JIO OneBB Full Cone 	
# UDP spam because connection-less

#### Steps
# 1. Send boops from both sides and receive them simultaneously till one of them revieves it
# 2. Reciever sends a particular msg to the non receiver so boops stop
# 3. Both parties forward the sockets to local ports.

##### Important 
# Both cannot be the clients in CS 1.6 usecase. So MULTIPLE PORTS FOR MULTIPLE CLIENTS... -_-

#### Approaches
# 1. Two sockets

import socket, time, select, threading, os

external = ("jio", 12001)
internal = ("127.0.0.1", 27015)

# ("home", 53153) 12001 -> 52825 ,50001 -> 52617

external_socc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
external_socc.bind(('', 12000))
external_socc.settimeout(0.5)

def makeConnection(socc):
	while True:
		try:
			message, address = socc.recvfrom(4096)
			print(message.decode())
			if (message.decode() != "ACK_"):
				socc.sendto("ACK_".encode(), external)
			break
		except:
			print("Nope")
			socc.sendto(b"boop",external)
			time.sleep(0.5)


makeConnection(external_socc)
external_socc.settimeout(105)

internal_socc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# time.sleep(90)
# external_socc.sendto("Connection is made".encode(), external)

def ext_recv():
	''' Receive from external source and forward to internal sink '''
	while True:
		try:
			msg, ip = external_socc.recvfrom(4096)
			internal_socc.sendto(msg, internal)
		except:
			continue

def int_recv():
	''' Receive from internal source and forward to external sink '''
	while True:
		try:
			msg, ip = internal_socc.recvfrom(4096)
			external_socc.sendto(msg, external)
		except:
			continue

x = threading.Thread(target=ext_recv)
y = threading.Thread(target=int_recv)
x.start()
y.start()

##### Notes
# - 90 Second delay works!!!!! NAT Mapping alive for 90 sec