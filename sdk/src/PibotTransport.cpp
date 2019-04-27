#include "PibotTransport.h"
#include <string.h>
#include <iostream>


PibotTransport::PibotTransport(DataStore& ds) : m_ds(ds)
{
    _parse_state = WAITING_FOR_BOF;
}

PibotTransport::~PibotTransport()
{

}

bool PibotTransport::data_recv(char* data, int len){
    for (int i=0; i<len; i++){
        parse(data[i]);
    }
    return false;
}

bool PibotTransport::pack_message(Message* msg, char* buf, unsigned int& len){
    return msg->pack(buf, len);
}


/*---------------------------------------*/
bool PibotTransport::parse(char ch){
    if (_parse_state == WAITING_FOR_BOF){
        _id = 0;
        _len = 0;
        _index = 0;
        memset(_data, 0, sizeof(_data));
        
        if (ch == _BOF) _parse_state = WAITING_FOR_ID;
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
            _data[_index++] = ch;

		if (_index >= _len)
		{
			_index = 0;
			_parse_state = WAITING_FOR_EOF;
		}
		return false;
    }
	if (_parse_state == WAITING_FOR_EOF){
		_parse_state = WAITING_FOR_BOF;
		if (ch == _EOF){
            return unpack(_id, _len, _data);
        }
        return false;
    }

	return true;
}

bool PibotTransport::unpack(int id, int len, char* data){
    if (id == ROBOT_POSE_RES){
        if (len != sizeof(Pose)) return false;
		memcpy(&m_ds.pose, data, len);
        return true;
    }
    if (id == ROBOT_SPEED_RES){
        if (len != sizeof(Speed)) return false;
		memcpy(&m_ds.speed, data, len);
        return true;
    }
    return false;
}
