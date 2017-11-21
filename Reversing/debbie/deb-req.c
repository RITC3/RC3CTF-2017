#include <sys/mman.h>
#include <stdio.h>

int liberty;

unsigned long *giveMeLiberty(){
    liberty = 1;
    return mmap(NULL, 0x1000, PROT_READ|PROT_WRITE, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
}

void giveMeDeath(unsigned long *ptr){
    munmap(ptr, 0x1000);
}
