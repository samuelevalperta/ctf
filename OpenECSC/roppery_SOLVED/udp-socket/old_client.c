#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>

int main(void){
    int socket_desc;
    struct sockaddr_in server_addr;
    char client_message[2000];
    int server_struct_length = sizeof(server_addr);

    // Clean buffers:
    memset(client_message, '\0', sizeof(client_message));
    // FILE *fd = fopen("flag.txt", "r");
    int fd = open("flag.txt", O_RDONLY);
    

    read(fd, client_message, 50);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(2000);
    server_addr.sin_addr.s_addr = inet_addr("87.4.35.214");
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    // Set port and IP:
    

    // Send the message to server:
    sendto(socket_desc, client_message, strlen(client_message), 0, (struct sockaddr*)&server_addr, server_struct_length);
    // Close the socket:
    close(socket_desc);

    return 0;
}