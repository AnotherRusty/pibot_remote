#ifndef IPARSER_H_
#define IPARSER_H_


class IParser
{
public:
    virtual bool data_recv(char* data, int len) = 0;
    virtual void assign_update_pose_address(float* pose) = 0;
    virtual void assign_update_speed_address(float* speed) = 0;
};

#endif