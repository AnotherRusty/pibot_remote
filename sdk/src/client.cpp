
#include "client.h"

Client::Client()
{

}

~Client::Client()
{

}

Client::Client()
{

}

bool Client::recvThread()
{
    while((true)){
        /* TODO */
    }
    
    return true;
}

bool Client::init(char* ip, unsigned short port)
{
    //connect

    //create_thread

    return true;
}


bool Client::getRobotPose(float pose[3])
{
    return true;
}

bool Client::getRobotSpeed(float spped[3])
{
    return true;
}

bool Client::setRobotPose(float pose[3])
{
    return true;
}

bool Client::setRobotSpeed(float spped[3])
{
    return true;
}

ClientInterface* createClient()
{
    return new Client();
}

void destroyClient(ClientInterface* client)
{
    delete client;
    client = NULL;
}

