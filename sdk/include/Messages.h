#ifndef MESSAGES_H_
#define MESSAGES_H_

#include "RobotData.h"

#define BOF 0x5a
#define EOF 0x0a
#define MAX_LEN 256

enum MsgId{
    //client ----> host
    robot_speed_get = 1,
    robot_speed_set = 2,
    robot_pose_get = 3,
    robot_pose_set = 4,

    //host ----> client
    robot_speed_res = 101,
    robot_pose_res = 102,
};


class Message
{
public: 
    virtual bool pack(char* buf, const unsigned int len){
        return true;
    };

private:
    const unsigned char bof = BOF;
    const unsigned char eof = EOF;
    const unsigned char id = 0;
};


class MsgSetSpeed : public Message
{
public:

};


#endif