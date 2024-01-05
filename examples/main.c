#include <stdio.h>

struct test {
  int a;
};

struct container {
  int some_other_data;
  int this_data;
  struct test t;
};

struct vm {
  int some_other_data;
  int this_data;
};

struct vm_data {
  int some_other_data;
  int this_data;
  struct test t;
};

int main()
{
  printf("In-struct-me test\n");
}
