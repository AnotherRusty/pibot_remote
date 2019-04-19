#ifndef MESSAGES_H_
#define MESSAGES_H_

#include "RobotData.h"
#include <string.h>

#define BOF 0x5a
#define EOF 0x0a
#define MAX_LEN 255

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
    const unsigned char bof = BOF;
    const unsigned char eof = EOF;
    virtual bool pack(char* buf, unsigned int& len) = 0;

};


class MsgSetPose : public Message
{
private:
    Pose _pose;
    const unsigned char id = (unsigned char)robot_pose_set;

public:
    MsgSetPose(float x, float y, float yaw){
        _pose.x = x;
        _pose.y = y;
        _pose.yaw = yaw;
    }

    bool pack(char* buf, unsigned int& len){
        buf[0] = bof;
        buf[1] = id;
        unsigned char data_len = sizeof(_pose);
        buf[2] = data_len;
        memcpy(buf+3, (unsigned char*)&_pose, data_len);
        buf[3+data_len] = eof;
        len = data_len+4;
    }
};


class MsgSetSpeed : public Message
{
private:
    Speed _speed;
    const unsigned char id = (unsigned char)robot_speed_set;

public:
    MsgSetSpeed(float x, float y, float w){
        _speed.vx = x;
        _speed.vy = y;
        _speed.vw = w;
    }

    bool pack(char* buf, unsigned int& len){
        buf[0] = bof;
        buf[1] = id;
        unsigned char data_len = sizeof(_speed);
        buf[2] = data_len;
        memcpy(buf+3, (unsigned char*)&_speed, data_len);
        buf[3+data_len] = eof;
        len = data_len+4;
    }
};


#endif