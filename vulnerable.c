//gcc

#include <stdio.h>

int main(void){
    call_me();

    char buffer[10];
    puts("Vpisi svoje ime: \n");
    gets(buffer);
    printf("Zivjo %s\n", buffer);
	return 0;
}

void call_me(void){
	puts("Koliko ste stari:\n");
	char buffer[10];
	fgets(buffer, 10, stdin);
	printf(buffer);
}

void gadget_pop_rdi() {
    __asm__(
        "pop %rdi\n\t"
        "ret\n\t"
    );
}
