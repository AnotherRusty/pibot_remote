
#ifndef _CLIENT_H_
#define _CLIENT_H_
#include "clientInterface.h"


class Client : public ClientInterface
{
public:
    Client();
    ~Client();
    
    bool init(char* ip, unsigned short port);

    bool getRobotPose(float pose[3]);
    bool getRobotSpeed(float spped[3]);

    bool setRobotPose(float pose[3]);
    bool setRobotSpeed(float spped[3]);

private:
    float pose[3];
    float speed[3];
};

#endif