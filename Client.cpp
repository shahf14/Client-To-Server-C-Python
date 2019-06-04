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
#include <thread>
#include<string>

#pragma comment(lib, "Ws2_32.lib")
#pragma warning(disable:4996)


#pragma pack(1)

typedef struct payload_t {
	uint32_t id;
	uint32_t counter;
	uint32_t opcode;
} payload;

#pragma pack()


int main()
{
	int PORT = 12345;
	int BUFFSIZE = 512;
	char buff[512];
	int ssock, csock;
	int nread;

	WSADATA WSAData;
	SOCKET server;
	SOCKADDR_IN addr;

	WSAStartup(MAKEWORD(2, 0), &WSAData);
	ssock = socket(AF_INET, SOCK_STREAM, 0);

	addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // local ip
	addr.sin_family = AF_INET; // IPV4
	addr.sin_port = htons(12345); // Port number 12345

	//connect(server, (SOCKADDR*)& addr, sizeof(addr));




	while (1) {
		csock = connect(ssock, (SOCKADDR*)& addr, sizeof(addr));;

		printf("connect to %s\n", inet_ntoa(addr.sin_addr));
		memset(buff, 0, BUFFSIZE);

		int i = 0;
		while (true){
			std::chrono::seconds interval(3);

			payload* p = (payload*)buff;

			p->counter = i;
			i++;
			p->id = 1;
			std::cout << "enter Opcode : ";
			std::cin >> p->opcode;

			nread=send(ssock, buff, sizeof(payload), 0);
			printf("send: id=%d, counter=%d, counter=%d\n",
				p->id, p->counter, p->opcode);
			printf("\nReceived %d bytes\n", nread);

			//sendMsg(csock, p, sizeof(payload));
			if((nread = recv(ssock, buff, BUFFSIZE, 0)) > 0)
				printf("Received: id=%d, counter=%d, opcode=%d\n",
				p->id, p->counter, p->opcode);
				printf("\nReceived %d bytes\n", nread);


		std::this_thread::sleep_for(interval); // wait 3 seconds

		}

		printf("Closing connection to client\n");
		printf("----------------------------\n");
		WSACleanup();
		//	close(csock);
		break;

	}
	exit(0);
	return 0;
}