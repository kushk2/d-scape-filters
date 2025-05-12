#include "queue_data_s.h"

void initialize(queue_s *q, int full)
{
    q->count = 0;
    q->front = NULL;
    q->rear = NULL;
    q->full = full;
}

int isempty(queue_s *q)
{
    return (q->rear == NULL);
}

void enqueue(queue_s *q, int value)
{
    if (q->count < q->full)
    {
        node_s *tmp;
        tmp = malloc(sizeof(node_s));
        tmp->data = value;
        tmp->next = NULL;
        if(!isempty(q))
        {
            q->rear->next = tmp;
            q->rear = tmp;
        }
        else
        {
            q->front = q->rear = tmp;
        }
        q->count++;
    }
    else
    {
        printf("List is full\n");
    }
}

int dequeue(queue_s *q)
{
    node_s *tmp;
    int n = q->front->data;
    tmp = q->front;
    q->front = q->front->next;
    q->count--;
    free(tmp);
    return(n);
}

void display(node_s *head)
{
    if(head == NULL)
    {
        printf("NULL\n");
    }
    else
    {
        printf("%d\n", head -> data);
        display(head->next);
    }
}

// Example
// int main()
// {
//     queue *q;
//     q = malloc(sizeof(queue));
//     initialize(q);
//     enqueue(q,10);
//     enqueue(q,20);
//     enqueue(q,30);
//     // printf("Queue before dequeue\n");
//     display(q->front);
//     dequeue(q);
//     // printf("Queue after dequeue\n");
//     display(q->front);
//     return 0;
// }