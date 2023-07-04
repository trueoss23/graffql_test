import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
tasks = []


@strawberry.type
class Task:
    name: str
    assignee_id: int


def find_index_task(task_id) -> Task:
    for i, elem in enumerate(tasks):
        if elem.id_ == task_id:
            return i
    raise KeyError("Task not found")


@strawberry.type
class TaskDb:
    id_: int
    name: str
    assignee_id: int


@strawberry.type
class Query:
    @strawberry.field
    def get_tasks(self) -> list[TaskDb]:
        return tasks

    @strawberry.field
    def get_task(self, task_id: int) -> TaskDb:
        index = find_index_task(task_id)
        task = tasks[index]
        return task


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, name: str,
                    assignee_id: int) -> TaskDb:
        new_id_ = len(tasks) + 1
        result = TaskDb(name=name, assignee_id=assignee_id, id_=new_id_)
        tasks.append(result)
        return result

    @strawberry.mutation
    def update_task_name(self, task_id: int,
                         new_name: str) -> TaskDb:
        try:
            index = find_index_task(task_id)
            task = tasks[index]
            task.name = new_name
            return task
        except KeyError:
            raise ValueError("Task not found")

    @strawberry.mutation
    def update_task_assignee_id(self, task_id: int,
                                new_assignee_id: int) -> TaskDb:
        try:
            index = find_index_task(task_id)
            task = tasks[index]
            task.assignee_id = new_assignee_id
            return task
        except KeyError:
            raise ValueError("Task not found")

    @strawberry.mutation
    def update_task(
                    self, task_id: int,
                    new_assignee_id: int,
                    new_name: str) -> TaskDb:
        try:
            index = find_index_task(task_id)
            task = tasks[index]
            task.assignee_id = new_assignee_id
            task.name = new_name
            return task
        except KeyError:
            raise ValueError("Task not found")

    @strawberry.mutation
    def delete_task(self, task_id: int) -> bool:
        try:
            index = find_index_task(task_id)
            del tasks[index]
        except KeyError:
            raise ValueError("Task not found")


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
