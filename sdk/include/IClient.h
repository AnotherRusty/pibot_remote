
#ifndef CLIENT_INTERFACE_H_
#define CLIENT_INTERFACE_H_

class IClient
{
public:
    virtual bool init(char* ip, unsigned short port) = 0;

    virtual bool getRobotPose(float pose[3]) = 0;
    virtual bool getRobotSpeed(float spped[3]) = 0;

    virtual bool setRobotPose(float pose[3]) = 0;
    virtual bool setRobotSpeed(float spped[3]) = 0;
};

IClient* CreateClient();

void DestroyClient(IClient* client);

#endif