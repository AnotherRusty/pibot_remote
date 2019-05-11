# Pibot远程控制系统使用手册

## 1. 系统介绍
在机器人ROS导航系统的框架基础上增加了一套系统，该系统提供了可跨平台的无需基于ROS的开发接口，可对机器人状态进行实时获取以及远程控制机器人的行动。
该系统采用tcp通讯，通过PHLCP（Pibot High Level Control Protocol）协议对机器人的进行控制以及监控状态。

## 2. 硬件
该系统针对的硬件为Pibot的全系列机器人。

## 3. 软件程序
### 3.1. Pibot ROS
Pibot机器人基于ROS系统，ROS相关程序位于机器人树莓派系统 /home/pibot/pibot_ros/
其中包含所有关于ROS程序源码（建图、导航等）。

### 3.2. Pibot Remote
Pibot远程控制系统的软件程序包含以下部分：
* `gateway`	- 机器人server程序
* `client`	- client 实现案例（python）
* `pypibot`	- 用于管理rosluanch
* `sdk`		- client开发包（C++）

## 4. 使用方法
机器人作为host，需要运行gateway程序。

ssh到树莓派，运行脚本～/pibot_remote/startup.sh
```
$: cd ~/pibot_remote/
$: sh startup.sh
```

PC作为client进行远程控制。

### 4.1 Demo (python)
client文件夹提供了Python实现的demo程序，可对单个机器人进行控制。

步骤1: 修改`Config.py`中HOST为机器人树莓派ip

步骤2: 运行`demo.py` 或 `demo_with_gui.py`

前者会接受机器人速度和位置的更新消息并打印出来。
后者可通过简单的UI界面对机器人速度和位置进行控制。

### 4.2 sdk (C++)

`sdk`提供一个另一个windows的动态库接口应用于创建`client`用于连接`Server`,可以参考`PibotClientTest.cpp`中的调用

#### 4.2.1 创建实例
```C
IClient* CreateClient();
void DestroyClient	(IClient* client);
```
- 通过`CreateClient`函数可以创建一个`IClient`实例
- `DestroyClient`释放资源

#### 4.2.2 IClient接口
```C++
class IClient
{
public:
    virtual bool init(const char* ip, unsigned short port, INotify* notify=0) = 0;
	virtual bool reconect() = 0;
    virtual bool getRobotPose(float pose[3]) = 0;
    virtual bool getRobotSpeed(float speed[3]) = 0;

    virtual bool setRobotPose(float pose[3]) = 0;
    virtual bool setRobotSpeed(float speed[3]) = 0;
};
```
- `init`：连接至一台机器人`Server`
> 传入ip，port以及通知接口（如果需要接受通知）
- `reconect`:重新建立连接
- `getRobotPose`:获取当前位置信息，x，y，yaw
- `getRobotSpeed`:获取当前速度信息，vx，vy，vz
- `setRobotPose`:设置当前位置信息，x，y，yaw
- `setRobotSpeed`:设置当前速度信息，vx，vy，vz

> vs文件夹提供visual stido 2008的工程