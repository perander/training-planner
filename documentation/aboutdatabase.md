## About database

The database consists of three main tables: `account`, `task` and `category`. The relations between them are many-to-many:
- A user can mark done or in progress any number of tasks, and a task can be marked by any number of users.
    - association tables `tasksdone` and `tasksinprogress`
- A task can have any number of categories, and many tasks can belong to the same category.
    - association table `tags`
- A task can have any number of subtasks, and a subtask can be a part of any number of tasks.
    - association table `subtasks` (not implemented yet)

An updated but not necessarily final scheme of the database as a diagram:

![diagram](./img/database.png) 