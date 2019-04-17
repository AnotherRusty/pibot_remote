#include "PibotParser.h"
#include <iostream>


PibotParser::PibotParser()
{
    _parse_state = WAITING_FOR_BOF;
}

PibotParser::~PibotParser()
{

}

void PibotParser::assign_update_pose_address(float* pose){
    pPose = pose;
}

void PibotParser::assign_update_speed_address(float* speed){
    pSpeed = speed;
}

bool PibotParser::data_recv(char* data, int len){
    for (int i=0; i<len; i++){
        if (parse(data[i])) return true;
    }
    return false;
}

bool PibotParser::parse(char ch){
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

bool PibotParser::unpack(int id, int len, char* data){
    if (id == robot_pose_res){
        if (len != 3) return false;
        pPose[0] = data[0];
        pPose[1] = data[1];
        pPose[2] = data[2];
        return true;
    }
    if (id == robot_speed_res){
        if (len != 3) return false;
        pSpeed[0] = data[0];
        pPose[1] = data[1];
        pPose[2] = data[2];
        return true;
    }
    return false;
}
