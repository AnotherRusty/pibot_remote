
#ifndef PIBOT_CLIENT_H_
#define PIBOT_CLIENT_H_

#include "IClient.h"
#include <winsock2.h>
#include "ITransport.h"
#include "Messages.h"


class PibotClient : public IClient
{
public:
    PibotClient();
    ~PibotClient();
    
    bool init(char* ip, unsigned short port);

    bool getRobotPose(float pose[3]);
    bool getRobotSpeed(float speed[3]);

    bool setRobotPose(float pose[3]);
    bool setRobotSpeed(float speed[3]);
	bool recvThread();

    void register_trans(ITransport* transport)

private:
	static DWORD WINAPI ThreadFunc(LPVOID p);
	int sendData(const char* data, unsigned int len);
private:
	HANDLE m_hThread;
	SOCKET m_socket;
    ITransport* m_transport;
};

#endif