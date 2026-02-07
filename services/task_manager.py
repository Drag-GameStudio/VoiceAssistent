from .base import classproperty, BaseService
import inspect
from todoist_api_python.api import TodoistAPI
import os

class TaskManager(BaseService):
    def __init__(self):
        super().__init__()
        TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
        self.api_manager = TodoistAPI(TODOIST_API_KEY)

    def get_tasks(self) -> dict:
        """
        Docstring for get_tasks
        this action returns list of tasks

        :return: Description
        :rtype: list
        """
        tasks = self.api_manager.get_tasks()
        if not tasks:
            return None

        all_tasks = []

        for task in tasks:
            for el in task:
                all_tasks.append({
                    "task_id": el.id,
                    "content": el.content,
                    "created_at": el.created_at
                })
        return all_tasks        

    def add_task(self, content: str):
        """
        Docstring for "add_task"
        :param content: content of task
        :type content: str

        this action is used to add some task
        """
        task_id = self.api_manager.add_task(content).id
        return f"Task has been added. Task id is {task_id}"
    
    def complite_task(self, task_id: int):
        """
        Docstring for complite_task
        this action is used to complite some task

        :param task_id: task id that have to be compited. You can take an id from data if you have already get data of tasks than you can take task id from there
        :type task_id: int
        """
        self.api_manager.complete_task(task_id)
        return "task has been complited"

    def del_task(self, task_id: int):
        """
        Docstring for del_task
        this action is used to del some task

        
        :param task_id: task id that have to be deleted. You can take an id from data if you have already get data of tasks than you can take task id from there
        :type task_id: int
        """
        self.api_manager.delete_task(task_id)
        return "task has been deleted"

    def handle(self, **kwargs):
        ...
        type_of_action = kwargs.get("type_of_action")
        kwargs.pop("type_of_action")
        result = getattr(self, type_of_action)(**kwargs)
        return result


    @classproperty
    def info(cls):
        return f"""
        This module can manage any task like add_task to calendar remove complite e.g.
        require arguments:
        type_of_action - it is the most important argument show what do you waht to do with calendar. The following arguments will depedent on type of action.
        {inspect.getdoc(cls.get_tasks)};
        {inspect.getdoc(cls.add_task)};
        {inspect.getdoc(cls.complite_task)};
        {inspect.getdoc(cls.del_task)};
        """        
        

