## Description and goals

This part of the documentation describes the intended product, but the end result might differ from this first draft.

With this program, a user can browse, subscribe and mark as done different kinds of training tasks or challenges. In fact, the tasks could be about anything, but here I'm interested in organizing and planning sports related tasks. The tasks are organized hierarchically so that for a task X, there can be a set of subtasks, so-to-say prerequisites for the task X. Then, for each of the subtasks, there can be again a set of subtasks, etc. This is supposed to make planning easier, since in order to help the user attain higher level goals, the program can show how to split tasks into smaller, easier parts.

Anyone can create a regular user account. Also at this point anyone can create an admin account, but the regular and admin accounts per person are separated.

After signing up (to a regular user account), the user can see the tasks both done and in progress, browse and search for tasks, see the subtasks per tasks (and continue further on the ‘chain’), see information about the users personal progress and possibly statistics about all tasks.

When a user is able to perform a task, it can be marked as done. The subtasks for the task are either automatically marked as done, or possibly just shown to the user, who can then decide whether to mark them or not (i’m not sure about this yet).

Tasks can also be marked as in progress, as something the user is currently working on. In case there are some uncompleted subtasks for the task in progress, the user is shown the subtasks and asked about their status. The program is supposed to be helpful in this way, by offering milestones on the way towards being able to perform a task.

A task can have any number of categories (kind of like tags). The tasks can be searched and found by their names, possibly their descriptions, and their categories.

A user with an admin role can create, update and delete tasks and categories and combine tasks with subtasks. When a subtask Y is assigned to a task X, all subtasks per that subtask Y will follow: in other words, the whole tree of subtasks is assigned to a new root: task X.
- An admin account can only be used for managing the content - not marking the tasks or viewing personal progress.
- At this point, it is up to the admin to create the content: a non-admin user can only view it. The admin is responsible for creating sensible tasks and hierarchies, so that the possibility of automatically marking subtasks done would be any useful. The program doesn’t know anything about the proper combination of tasks by their content.

### Planned features (not in order)
This is the original plan of the future use cases. During the project, I'm keeping an updated and more detailed list of implemented and planned user stories [here](https://github.com/perander/training-planner/projects/1).

##### Implementing first:

- Create, update and delete an account (regular, admin)
- Log in
- Browse all tasks
- Search tasks by name, category, possibly words in the description
- Only regular user:
    - Mark a task as done (and possibly mark the subtasks as done automatically)
    - Mark a task as in progress
- Only admin:
    - Create, update and delete tasks
    - Create, update and delete categories
    - Combine tasks hierarchically

##### Second:

- A front page showing the tasks in progress, maybe latest added tasks and recommendations
- Recommend tasks based on the previously marked tasks
    - Meaning, if the user has completed a set of tasks, which happen to be subtasks for some next level task, that can be recommended. There could also be an almost completed set of subtasks, in which case the program would say something like ‘you are this and that subtask away from completing this task’
- View personal progress information
    - User specific data/statistics about the progress by category, recommendations. This would maybe work better with some kind of an initial check of the starting situation.
- Possibility to see statistics for the most popular tasks or categories, or the subtasks contributing to the largest amount of tasks


##### Implementing later / if there’s enough time:
- Maybe: in addition to categories, there could be entire training plans or sports, which could form their own hierarchy and thereby be an individually complete training plan. If categories were something like strength or flexibility, sport/plan tags could be sports like acrobatics or crossfit, or something more abstract like ‘basic health for xx-year olds’. These tags could probably just be categories as well, though.
    - Would enable even larger goals, such as whole sports
    - Could search for ‘strength tasks in crossfit’, narrow down the search.
- A place for the users to suggest tasks for the admins.
- A possibility to comment on tasks.
- A calendar or other way of setting tasks to be worked on at a specific time / order.
    - Time stamps
- If there’s a task marked done, but which hasn’t been worked on (= any of it’s supertasks haven’t been marked as done or in progress) in some time (some months?), the program could ask ‘can you still do this’ or something. Since it’s possible to lose the ability to perform a task, they might get old and the recommendations would therefore be inaccurate.
