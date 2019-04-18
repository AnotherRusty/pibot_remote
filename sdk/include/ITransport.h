#ifndef ITRANSPORT_H_
#define ITRANSPORT_H_

#include "Messages.h"


class ITransport
{
public:
    virtual bool data_recv(char* data, int len) = 0;
    virtual void assign_update_pose_address(Pose* pose) = 0;
    virtual void assign_update_speed_address(Speed* speed) = 0;
    virtual DataToSend* pack_message(Message* msg) = 0;
};

#endif