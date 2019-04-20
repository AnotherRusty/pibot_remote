#include "PibotClient.h"
#include <iostream>
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include "DataStore.h"
#include "Messages.h"
#include "PibotTransport.h"

#pragma comment (lib, "Ws2_32.lib")

#define MAX_RECV_BUFF_LEN 1024

PibotClient::PibotClient()
{
	m_socket = INVALID_SOCKET;
	m_transport = new PibotTransport();
}

PibotClient::~PibotClient()
{
	if (m_transport)
		delete m_transport;
}

void PibotClient::register_trans(ITransport* transport)
{
	m_transport = transport;
}

DWORD WINAPI PibotClient::ThreadFunc(LPVOID p)
{   
	char recvbuf[MAX_RECV_BUFF_LEN]={0};
	int iResult = 0;
	PibotClient* client = (PibotClient*)p;
	do {
		memset(recvbuf, 0, sizeof(recvbuf));
		iResult = recv(client->m_socket, recvbuf, MAX_RECV_BUFF_LEN, 0);
		if ( iResult > 0 ){
			//std::cout << "Bytes received: " << iResult << std::endl;
			client->m_transport->data_recv(recvbuf, iResult);
		}
		else if ( iResult == 0 )
			std::cout << "Connection closed" << std::endl;
		else
			std::cout << "ecv failed with error: " << WSAGetLastError() << std::endl;

	} while( iResult > 0 );

	return 0;
}

bool PibotClient::init(char* ip, unsigned short port)
{
	WSADATA wsaData;
	static struct sockaddr_in server_in;
	int iResult;

	iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
	if (iResult != 0) {
		std::cout << "WSAStartup failed with error:" << iResult << std::endl;
		return false;
	}

	server_in.sin_family = AF_INET;
	server_in.sin_port = htons(port);
	server_in.sin_addr.S_un.S_addr = inet_addr(ip);
	m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (m_socket == INVALID_SOCKET) {
		printf("socket failed with error: %ld\n", WSAGetLastError());
		WSACleanup();
		return false;
	}

	iResult = connect( m_socket, (struct sockaddr *)&server_in, sizeof(server_in));
	if (iResult == SOCKET_ERROR) {
		closesocket(m_socket);
		m_socket = INVALID_SOCKET;
		return false;
	}

	DWORD  threadId;
    m_hThread = CreateThread(NULL, 0, PibotClient::ThreadFunc, this, 0, &threadId);

    return true;
}

int PibotClient::sendData(const char* data, unsigned int len)
{
	int iResult = send( m_socket, data, len, 0 );
	if (iResult == SOCKET_ERROR) {
		std::cout << "send failed with error:"  << WSAGetLastError() << std::endl;
		closesocket(m_socket);
		WSACleanup();
		return -1;
	}

	return iResult;
}

bool PibotClient::getRobotPose(float pose[3])
{
	DataStore* ds = DataStore::get();
	pose[0] = ds->pose.x;
	pose[1] = ds->pose.y;	
	pose[2] = ds->pose.yaw;
	return true;
}

bool PibotClient::getRobotSpeed(float speed[3])
{
	DataStore* ds = DataStore::get();
	speed[0] = ds->speed.vx;
	speed[1] = ds->speed.vy;
	speed[2] = ds->speed.vw;
    return true;
}

bool PibotClient::setRobotPose(float pose[3])
{
	MsgSetPose msg(pose[0], pose[1], pose[2]);
	char buf[MAX_LEN]={0};
	unsigned int len;
	if (m_transport->pack_message(&msg, buf, len)) 
	{
		sendData(buf, len);
    	return true;
	}
	return false;
}

bool PibotClient::setRobotSpeed(float speed[3])
{
	MsgSetSpeed msg(speed[0], speed[1], speed[2]);
	char buf[MAX_LEN]={0};
	unsigned int len;
	if (m_transport->pack_message(&msg, buf, len)) 
	{
		sendData(buf, len);
    	return true;
	}
	return false;
}

IClient* CreateClient()
{
    return new PibotClient();
}

void DestroyClient(IClient* client)
{
    delete client;
    client = 0;
}

