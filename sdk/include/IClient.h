
#ifndef ICLIENT_H_
#define ICLIENT_H_

class IClient
{
public:
    virtual bool init(char* ip, unsigned short port) = 0;

    virtual bool getRobotPose(float pose[3]) = 0;
    virtual bool getRobotSpeed(float speed[3]) = 0;

    virtual bool setRobotPose(float pose[3]) = 0;
    virtual bool setRobotSpeed(float speed[3]) = 0;
};

IClient* CreateClient();

void DestroyClient(IClient* client);

#endif