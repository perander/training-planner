## The end result

This describes the program on 30.4. I will list the use cases which have been realised and those which have not, and the SQL-clauses for the realised ones. Most of the general topic description in [the first draft](./description.md) is still the same.

With this program, a user can browse, subscribe and mark as done different kinds of training tasks or challenges. In fact, the tasks could be about anything, but here I'm interested in organizing and planning sports related tasks. The tasks are organized hierarchically so that for a task X, there can be a set of subtasks, so-to-say prerequisites for the task X. Then, for each of the subtasks, there can be again a set of subtasks, etc. This is supposed to make planning easier, since in order to help the user attain higher level goals, the program can show how to split tasks into smaller, easier parts.

There are two roles: **admin** and **regular user**. Anyone can create a regular user account as well as an admin account, but the regular and admin accounts per person are separated. After registering and signing in, here's what both roles can do:

### Admin

- Register/create an account
    - `INSERT INTO account (date_created, date_modified, username, _password, admin) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)`
- Log in
- Create tasks
    - `INSERT INTO task (date_created, date_modified, name, description) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)`
    - `INSERT INTO tags (category_id, task_id) VALUES (?, ?)`
    - ` INSERT INTO subtask (supertask_id, subtask_id) VALUES (?, ?)`
- View all tasks
    - ` SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task ORDER BY task.date_created DESC`
- Update task
    - `UPDATE task SET date_modified=CURRENT_TIMESTAMP, name=? WHERE task.id = ?`
- Delete task
    - `DELETE FROM tags WHERE tags.category_id = ? AND tags.task_id = ?`
    - `DELETE FROM subtask WHERE subtask.supertask_id = ? AND subtask.subtask_id = ?`
    - `DELETE FROM task WHERE task.id = ?`
- Create categories
    - `INSERT INTO category (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)`
- View all categories
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name`
- Update category
    - `UPDATE category SET date_modified=CURRENT_TIMESTAMP, name=? WHERE category.id = ?`
- Delete category
    - `DELETE FROM category WHERE category.id = ?`
- Search for tasks and categories
    - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task 
WHERE (lower(task.name) LIKE '%' || lower(?) || '%')`
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name 
FROM category 
WHERE (lower(category.name) LIKE '%' || lower(?) || '%')`

### Regular user

- Register/create an account
    - `INSERT INTO account (date_created, date_modified, username, _password, admin) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)`
- Log in
- View all tasks
    - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task`
    - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description FROM task, tasksdone 
WHERE ? = tasksdone.account_id AND task.id = tasksdone.task_id`
    - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description FROM task, tasksinprogress 
WHERE ? = tasksinprogress.account_id AND task.id = tasksinprogress.task_id`
- View task
    - ` SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task 
WHERE task.id = ?`
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name 
FROM category JOIN tags ON category.id = tags.category_id JOIN task ON task.id = tags.task_id 
WHERE tags.category_id = category.id AND tags.task_id = ?`
    - `SELECT subtask.supertask_id AS subtask_supertask_id, subtask.subtask_id AS subtask_subtask_id, task_1.id AS task_1_id, task_1.date_created AS task_1_date_created, task_1.date_modified AS task_1_date_modified, task_1.name AS task_1_name, task_1.description AS task_1_description 
FROM subtask LEFT OUTER JOIN task AS task_1 ON task_1.id = subtask.subtask_id 
WHERE ? = subtask.supertask_id`
- `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task, tasksdone 
WHERE ? = tasksdone.account_id AND task.id = tasksdone.task_id`
- mark task in progress
    - `INSERT INTO tasksinprogress (account_id, task_id) VALUES (?, ?)`
- mark task done
    - `INSERT INTO tasksdone (account_id, task_id) VALUES (?, ?)`
- View all categories
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name 
FROM category ORDER BY category.date_created DESC`
- View category
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name 
FROM category 
WHERE category.id = ?`
- View recommendations
- View new tasks
    - fetch all:
        - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task`
    - see which have been marked as done by the user:
        - ` SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task, tasksdone 
WHERE ? = tasksdone.account_id AND task.id = tasksdone.task_id`
    - see which have been marked as in progress by the user:
        - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task, tasksinprogress 
WHERE ? = tasksinprogress.account_id AND task.id = tasksinprogress.task_id`
    - show the rest
- View top 5 tasks done
    - ` SELECT task_id, task.name, COUNT(*) FROM tasksdone, task WHERE tasksdone.task_id = task.id GROUP BY task_id, task.name ORDER BY COUNT(*) DESC LIMIT 5`
- View top 5 tasks in progress
    - `SELECT task_id, task.name, COUNT(*) FROM tasksinprogress, task WHERE tasksinprogress.task_id = task.id GROUP BY task_id, task.name ORDER BY COUNT(*) DESC LIMIT 5`
- Search for tasks and categories
    - `SELECT task.id AS task_id, task.date_created AS task_date_created, task.date_modified AS task_date_modified, task.name AS task_name, task.description AS task_description 
FROM task 
WHERE (lower(task.name) LIKE '%' || lower(?) || '%')`
    - `SELECT category.id AS category_id, category.date_created AS category_date_created, category.date_modified AS category_date_modified, category.name AS category_name 
FROM category 
WHERE (lower(category.name) LIKE '%' || lower(?) || '%')`
    
    
## Use cases left undone

The most relevant use cases I planned to implement but didn't (yet) are:

- Admin can update their account information
- Admin can delete their account
- Regular user can update their account information
- Regular user can delete their account
- It would have been nice to visualise the task chains / hierarchies somehow
- Some kind of an alert if user has marked a task done or in progress a long time ago: a reminder

## Known errors / what's not working

- When a new category is created, the server adds a # in front of the name. Then, when updating the category, it shows the old name with the # as default value. You can update the name without erasing the #. I thought initially though to be able to compare the names on the server so that you couldn't update a category to be the same as an already existing one. This fails now, because it compares the name with a name with a #, and doesn't detect the doubles. It only succeeds if the updated name is written without the #. This is not a huge issue, rather a question of time.
- It is still possible to create empty tasks. I implemented the TaskForm with a custom MultiCheckBoxField, which doesn't support the form.validate. I didn't yet find out how to make a custom validator for it.
- The recommendations only take into account direct subtasks. It is however possible to update some of the *subtasks* by adding it a subtask, which the user hasn't done. It would maybe be better to show it directly like 'there is a new subtask for this task'.
    - I think that if the added subtask is rather deep in the hierarchy, it is probably something the user can do. If the user won't see it though, it might mess up with the other tasks having the updated task as subtask.