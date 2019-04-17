
#include <iostream>
#include "IClient.h"

int main()
{
	IClient* client1 = CreateClient();
	client1->init("127.0.0.1", 9002);

	DestroyClient(client1);
	return 0;
}