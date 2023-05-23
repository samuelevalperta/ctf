#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main() {

  FILE *fp = fopen("flag.txt", "rb");

  asm("mov");
  
  
  har* flag = 0;

  fseek(fp, 0, SEEK_END);
  flag = malloc(ftell(fp));

  fread(flag, 1, ftell(fp), fp);
  printf("%s", flag);


  int sockfd = socket(AF_INET, SOCK_STREAM, 0);

  struct sockaddr_in server_addr;

  server_addr.sin_family = AF_INET;
  server_addr.sin_port = 80;
  server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
  
  int e = connect(sockfd, &server_addr, sizeof(server_addr));

  sendto(sockfd, flag, 1000, 0, &server_addr, 1000);
  
  return 0;
}