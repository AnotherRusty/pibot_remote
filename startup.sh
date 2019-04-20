#!/bin/bash
clear

echo 'killing rosmaster/roscore if already exists'
killall -9 roscore
killall -9 rosmaster

echo 'start roscore ..'
roscore &

until rostopic list | grep -q rosout; do
    sleep 1
done

echo 'start gateway ..'
cd Gateway
./Gateway.py

