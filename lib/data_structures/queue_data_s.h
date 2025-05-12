#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0

struct node_s
{
    int data;
    struct node_s *next;
};
typedef struct node_s node_s;

struct queue_s
{
    int count;
    int full;
    node_s *front;
    node_s *rear;
};
typedef struct queue_s queue_s;

void initialize(queue_s *q, int full);
int isempty(queue_s *q);
void enqueue(queue_s *q, int value);
int dequeue(queue_s *q);
void display(node_s *head);