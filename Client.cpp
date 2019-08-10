//#include <sys/socket.h>
//#include <arpa/inet.h> //inet_addr
//#include <unistd.h>    //write
#include<io.h>
#include <fstream>
#include <thread>
#include <chrono>


#pragma comment(lib, "Ws2_32.lib")
#pragma warning(disable:4996)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <iostream>
#include <winsock2.h>
#include <chrono>
#include<string>

#pragma comment(lib, "Ws2_32.lib")
#pragma warning(disable:4996)


#pragma pack(1)

typedef struct message {
	uint32_t id;
	uint32_t counter;
	uint32_t opcode;
} payload;

#pragma pack()


int main()
{

	WSADATA WSAData;
	SOCKET UDP_socket;
	SOCKADDR_IN addr;



	// initialize socket 
	int PORT = 12345; 
	char buff[1024];
	int nread;

	// local variable
	int i = 0 ; // this will use by counter to increase by one. 
	const int TIME_TO_SLEEP = 1;

	

	if(WSAStartup(MAKEWORD(2, 0), &WSAData) != 0) {
		return -1;
	}
	

	UDP_socket = socket(AF_INET, SOCK_DGRAM, 0);

	if (UDP_socket == INVALID_SOCKET){
		printf("Create a new socket failed!");
		return -1;
	}
	printf("New socket has been created!");


	addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // local ip
	addr.sin_family = AF_INET; // IPV4
	addr.sin_port = htons(PORT); // Port number 12345

	//connect(server, (SOCKADDR*)& addr, sizeof(addr));
	std::chrono::seconds interval(TIME_TO_SLEEP); // define the number of 

	while (true) {
		
		connect(UDP_socket, (SOCKADDR*)& addr, sizeof(addr));
		printf("connect to %s\n", inet_ntoa(addr.sin_addr));
		memset(buff, 0, 1024); //initial buffer with zeros

		while (true) {

			payload* p = (payload*)buff;

			p->counter = i;
			i++;
			p->id = 1;
			//std::cout << "enter Opcode : ";
			//std::cin >> p->opcode;
			p->opcode = i * 5;

			nread = send(UDP_socket, buff, sizeof(message), 0);
			printf("send: id=%d, counter=%d, counter=%d\n",p->id, p->counter, p->opcode);
			printf("\nReceived %d bytes\n", nread);

			if ((nread = recv(UDP_socket, buff, 1024, 0)) > 0)
				printf("Received: id=%d, counter=%d, opcode=%d\n",
					p->id, p->counter, p->opcode);
			printf("\nReceived %d bytes\n", nread);


			std::this_thread::sleep_for(interval); // wait 3 seconds

		}

		printf("Closing connection to client\n");

		WSACleanup();
		//	close(csock);

	}
	exit(0);
	return 0;
}
