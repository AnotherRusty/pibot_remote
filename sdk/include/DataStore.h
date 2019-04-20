#ifndef DATA_STORE_H_
#define DATA_STORE_H_

#include <string.h>
#include "RobotData.h"

class DataStore{
    public:
        static DataStore* get(){
            static DataStore ds;
            return &ds;
        }
    
    private:
        DataStore(){
            memset(&pose, 0, sizeof(Pose));
            memset(&speed, 0, sizeof(Speed));
            }
    public:
        Pose    pose;
        Speed   speed;
};

#endif