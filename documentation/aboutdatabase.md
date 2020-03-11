## About database

The database consists of three main tables: user, task and category. The relations between them are many-to-many:
- A user can 'have' (= mark done or in progress) many tasks, and a task can be marked by many users.
- A task can have many categories, and many tasks can belong to the same category.

First draft of the database as a diagram:

![diagram](../img/dbdiagram.png) 