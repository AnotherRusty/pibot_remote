
#include <iostream>
#include "IClient.h"
#include <windows.h>
int main()
{
	float a[3]={1,2,3};

	IClient* client1 = CreateClient();
	if (!client1->init("192.168.2.231", 8998))
	{
		return 0;
	}

	float speed[3]={1,2,3};
	float pos[3]={4,4,1};
	client1->setRobotPose(pos);
	memset(pos, 0, sizeof(pos));
	while(1)
	{
		client1->setRobotSpeed(speed);
		client1->getRobotPose(pos);
		
		memset(speed, 0, sizeof(speed));
		client1->getRobotSpeed(speed);

		std::cout << "speed:" << speed[0] << ", " << speed[1] << ", "  << speed[2] << ", pos: " << pos[0] << ", "  << pos[1] << ", "  << pos[2] << ", "  << std::endl;
		Sleep(100);
	}

	DestroyClient(client1);
	return 0;
}