#ifndef PIBOT_PARSER_H_
#define PIBOT_PARSER_H_

#include "IParser.h"

#define BOF 0x5a
#define EOF 0x0a
#define MAX_LEN 256

enum ParseState{
    WAITING_FOR_BOF = 0,
    WAITING_FOR_ID = 2,
    WAITING_FOR_LEN = 3,
    WAITING_FOR_DATA = 4,
    WAITING_FOR_EOF = 5,
};

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


class PibotParser : public IParser
{
public:
    PibotParser();
    ~PibotParser();

    bool data_recv(char* data, int len);
    bool parse(char ch);
    bool unpack(int id, int len, char* data);
    void assign_update_pose_address(float* pose);
    void assign_update_speed_address(float* speed);

private:
    ParseState _parse_state;
    int 
        _id,
        _len,
        _index;
    char _data[MAX_LEN];
    float* pPose;
    float* pSpeed;
};

#endif