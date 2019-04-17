
#ifndef PIBOT_CLIENT_H_
#define PIBOT_CLIENT_H_

#include "IClient.h"
#include <winsock2.h>


class PibotClient : public IClient
{
public:
    PibotClient();
    ~PibotClient();
    
    bool init(char* ip, unsigned short port);

    bool getRobotPose(float pose[3]);
    bool getRobotSpeed(float spped[3]);

    bool setRobotPose(float pose[3]);
    bool setRobotSpeed(float spped[3]);
	bool recvThread();
private:
	static DWORD WINAPI ThreadFunc(LPVOID p);
	int sendData(const char* data, unsigned int len);
private:
    float pose[3];
    float speed[3];
	HANDLE m_hThread;
	SOCKET m_socket;
};

#endif