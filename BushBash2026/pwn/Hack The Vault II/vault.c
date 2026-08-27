#include <stdio.h>
#include <string.h>

void welcome(){
    printf("I've found another one, I need your help, quick, he's running!\n");
}

int auth(){
    char array[127 + 64];
    char *buffer = &array[0];
    char *password = &array[127];
    printf("Enter the password: ");

    size_t inputlen = 0;
    char c;
    while((c = getchar()) != '\n' && c != '\r' && c != EOF){
        if(inputlen == 127){
            printf("input exceeded buffer limit\n");
            return 0;
        }
        buffer[inputlen] = c;
        ++inputlen;
    }
    buffer[inputlen] = '\0';

    FILE *pf = fopen("password.txt", "r");
    
    if(pf == NULL){
        printf("password.txt not found");
        return 0;
    }
    size_t bytesRead = fread(password, 1, 48, pf);
    password[bytesRead] = '\0';
    size_t passwordlen = strlen(password);

    printf("password you entered: %s\n", buffer);

    if(passwordlen > 0 && password[passwordlen - 1] == '\n'){
        passwordlen--;
        password[passwordlen] = '\0';
    }
    if(passwordlen != inputlen) return 0;
    if(strncmp(buffer, password, passwordlen) == 0) return 1;
    return 0;
}

void displayFlag(){
    char buffer[128];
    FILE *f = fopen("flag.txt", "r");
    if(f == NULL){
        printf("flag.txt not found\n");
        return;
    }
    size_t readres = fread(buffer, 1, 100, f);
    printf("%s", buffer);
}


int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    welcome();
    if(auth()){
        printf("I knew I can count on you! Chasing 'em down, and see you on the flip side.\n");
        displayFlag();
    }else{
        printf("Better luck next time.\n");
    }
    return 0;
}
