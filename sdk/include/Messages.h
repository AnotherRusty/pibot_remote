#ifndef MESSAGES_H_
#define MESSAGES_H_

#include "RobotData.h"
#include <string.h>

#define _BOF 0x5a
#define _EOF 0x0a
#define MAX_LEN 255

enum MsgId{
    //client ----> host
    ROBOT_SPEED_GET = 1,
    ROBOT_SPEED_SET = 2,
    ROBOT_POSE_GET = 3,
    ROBOT_POSE_SET = 4,

    //host ----> client
    ROBOT_SPEED_RES = 101,
    ROBOT_POSE_RES = 102,
};


class Message
{
public: 
    virtual bool pack(char* buf, unsigned int& len) = 0;

};


class MsgSetPose : public Message
{
private:
    Pose _pose;
    unsigned char id;

public:
    MsgSetPose(float x, float y, float yaw){
        _pose.x = x;
        _pose.y = y;
        _pose.yaw = yaw;
		id = (unsigned char)ROBOT_POSE_SET;
    }

    bool pack(char* buf, unsigned int& len){
        buf[0] = _BOF;
        buf[1] = id;
        unsigned char data_len = sizeof(_pose);
        buf[2] = data_len;
        memcpy(buf+3, (unsigned char*)&_pose, data_len);
        buf[3+data_len] = _EOF;
        len = data_len+4;

		return true;
    }
};


class MsgSetSpeed : public Message
{
private:
    Speed _speed;
    unsigned char id;

public:
    MsgSetSpeed(float x, float y, float w){
        _speed.vx = x;
        _speed.vy = y;
        _speed.vw = w;
		id = (unsigned char)ROBOT_SPEED_SET;
    }

    bool pack(char* buf, unsigned int& len){
        buf[0] = _BOF;
        buf[1] = id;
        unsigned char data_len = sizeof(_speed);
        buf[2] = data_len;
        memcpy(buf+3, (unsigned char*)&_speed, data_len);
        buf[3+data_len] = _EOF;
        len = data_len+4;

		return true;
    }
};


#endif