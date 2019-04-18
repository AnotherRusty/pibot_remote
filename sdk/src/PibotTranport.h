#ifndef PIBOT_TRANSPORT_H_
#define PIBOT_TRANSPORT_H_

#include "ITransport.h"
#include "Messages.h"


#define MAX_LEN 256

enum ParseState{
    WAITING_FOR_BOF = 0,
    WAITING_FOR_ID = 2,
    WAITING_FOR_LEN = 3,
    WAITING_FOR_DATA = 4,
    WAITING_FOR_EOF = 5,
};


class PibotTransport : public ITransport
{
public:
    PibotTransport();
    ~PibotTransport();

    bool data_recv(char* data, int len);
    void assign_update_pose_address(Pose* pose);
    void assign_update_speed_address(Speed* speed);
    DataToSend* pack_message(Message* msg);

private:
    bool parse(char ch);
    bool unpack(int id, int len, char* data);
    ParseState _parse_state;
    int 
        _id,
        _len,
        _index;
    char _data[MAX_LEN];
    Pose* pPose;
    Speed* pSpeed;
};

#endif