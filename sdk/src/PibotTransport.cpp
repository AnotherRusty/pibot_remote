#include "PibotTransport.h"
#include <string.h>
#include <iostream>
#include "DataStore.h"


PibotTransport::PibotTransport()
{
    _parse_state = WAITING_FOR_BOF;
}

PibotTransport::~PibotTransport()
{

}

bool PibotTransport::data_recv(char* data, int len){
    for (int i=0; i<len; i++){
        if (parse(data[i])) return true;
    }
    return false;
}

bool PibotTransport::pack_message(Message* msg, char* buf, unsigned int& len){
    return msg->pack(buf, len);
}


/*---------------------------------------*/
bool PibotTransport::parse(char ch){
    std::cout << ch;
    if (_parse_state == WAITING_FOR_BOF){
        _id = 0;
        _len = 0;
        _index = 0;
        memset(_data, 0, sizeof(_data));
        
        if (ch == BOF) _parse_state = WAITING_FOR_ID;
        return false;
    }
    if (_parse_state == WAITING_FOR_ID){
        _id = int(ch);
        _parse_state = WAITING_FOR_LEN;
        return false;
    }
    if (_parse_state == WAITING_FOR_LEN){
        _len = int(ch);
        _parse_state = WAITING_FOR_DATA;
        return false;
    }
    if (_parse_state == WAITING_FOR_DATA){
        if (_index < _len){
            _data[_index++] = ch;
            return false;
        }
        else
            _parse_state = WAITING_FOR_EOF;
    }
    if (_parse_state == WAITING_FOR_EOF){
        if (ch == EOF){
            return unpack(_id, _len, _data);
        }
        _parse_state = WAITING_FOR_BOF;
        return false;
    }
}

bool PibotTransport::unpack(int id, int len, char* data){
    if (id == robot_pose_res){
        if (len != sizeof(Pose)) return false;
        DataStore* ds = DataStore::get();
        ds->pose.x = data[0];
        ds->pose.y = data[1];
        ds->pose.yaw = data[2];
        return true;
    }
    if (id == robot_speed_res){
        if (len != 3) return false;
        DataStore* ds = DataStore::get();
        ds->speed.vx = data[0];
        ds->speed.vy = data[1];
        ds->speed.vw = data[2];
        return true;
    }
    return false;
}
