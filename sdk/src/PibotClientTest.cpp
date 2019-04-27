#include <string>
#include <iostream>
#include "IClient.h"
#include <windows.h>

#define CLIENT_COUNT 3

IClient* client[CLIENT_COUNT]={0};
std::string ip[CLIENT_COUNT]={"192.168.2.146","192.168.2.115","192.168.2.247"};
unsigned short port[CLIENT_COUNT] = {8998, 8998, 8998};
int main()
{

	for (int i=0;i<CLIENT_COUNT;i++)
	{
		client[i] =  CreateClient();
		if (!client[i]->init(ip[i].c_str(), port[i]))
		{
			return 0;
		}
	}

	float speed[CLIENT_COUNT]={0};
	float pos[CLIENT_COUNT]={0};
	for (int i=0;i<CLIENT_COUNT;i++)
	{
		//client[i]->setRobotPose(pos);
	}
	//memset(pos, 0, sizeof(pos));
	while(1)
	{
		for (int i=0;i<CLIENT_COUNT;i++)
		{
			//client[i]->setRobotSpeed(speed);
			client[i]->getRobotPose(pos);

			client[i]->getRobotSpeed(speed);

			std::cout << "robot" << i <<":speed[" << speed[0] << ", " << speed[1] << ", "  << speed[2] << "], pos[" << pos[0] << ", "  << pos[1] << ", "  << pos[2] << "]"  << std::endl;
		}

		Sleep(100);
	}

	for (int i=0;i<CLIENT_COUNT;i++)
	{
		DestroyClient(client[i]);
	}
	return 0;
}