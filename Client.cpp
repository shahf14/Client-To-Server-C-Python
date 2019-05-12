// Client.cpp : Defines the functions for the static library.

#include "pch.h"
#include "framework.h"
#include <iostream>
#include <winsock2.h>
#include <chrono>
#include <thread>

using namespace std;

class Message {

	int static counter;

public:

	int *serial_number;
	int opcode = 0;
	string text;


	Message() {
		text = "this is message number : " + counter;
		serial_number = &counter;
		opcode = rand() % 3 + 1;
		counter++;
	}
};


int main(){

	WSADATA WSAData;
	SOCKET server;
	SOCKADDR_IN addr;

	WSAStartup(MAKEWORD(2, 0), &WSAData);
	server = socket(AF_INET, SOCK_STREAM, 0);

	addr.sin_addr.s_addr = (ULONG)"127.0.0.1";  // local ip
	addr.sin_family = AF_INET; // IPV4
 	addr.sin_port = htons(12345); // Port number 12345

	connect(server, (SOCKADDR*)& addr, sizeof(addr)); 

	while (true) {
		std::chrono::seconds interval(3); 
		Message* msg = new Message();

		char* converted_message = reinterpret_cast<char*>(&msg); // Converts the message object to binary

		send(server, converted_message, sizeof(*msg), 0); // sending message

			std::this_thread::sleep_for(interval); // wait 3 seconds
		}

	
closesocket(server);
WSACleanup();
	
	
}



