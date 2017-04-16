import socket
import time
import mysql.connector
import threading,time
def tcplink(sock,addr):
	print('accept new connection from %s:%s'%addr)
	sock.send(b'welcome')
	while True:
		data1 =sock.recv(1024)
		time.sleep(1)
		cursor = conn.cursor()
		if data1.decode('utf-8')=='exit'or len(data1)==0:
			break
		data=data1.decode('utf-8')
		tt=data.split(' ')
		if tt[0]=='login':
			try:
				cursor.execute('select password from userlogin where name= %s',(tt[1],))
				value=cursor.fetchall()
				cursor.close()
				for i in value:
					for m in i:	
						sock.send(i.__str__().encode('utf-8'))
			except Exception as e:
				sock.send('wrong!'.encode('utf-8'))
				break
		if tt[0] =='new':
			print('new')
			print(tt[1],tt[2])
			try:
				cursor.execute('insert into userlogin values(0,%s,%s)',(tt[1],tt[2]))
				print(cursor.rowcount)
				conn.commit()
				cursor.close()
				s.send('ok!'.encode('utf-8'))
			except Exception as e :
				sock.send('wrong'.encode('utf-8'))
	sock.close()
	print('connection from %s:%s closed'%addr)
if __name__ == '__main__':
	conn = mysql.connector.connect(user ='root',password='123',database='test')
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('10.131.164.143',9999))
	s.listen(5)
	print('waiting for conneting')
	while True:
		sock,addr=s.accept()
		t=threading.Thread(target=tcplink,args=(sock,addr))
		t.start()
