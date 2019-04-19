#ifndef ITRANSPORT_H_
#define ITRANSPORT_H_

#include "Messages.h"

class ITransport
{
public:
    virtual bool data_recv(char* data, int len) = 0;
    virtual bool pack_message(Message* msg, char* buf, unsigned int* len) = 0;
};

#endif