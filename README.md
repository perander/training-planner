## training-planner

A study project for the university course on databases.

With this program, a user can browse, subscribe and mark as done different kinds of training tasks or challenges. The tasks are organized hierarchically so that for a task X, there can be a set of subtasks, so-to-say prerequisites for the task X. Then, for each of the subtasks, there can be again a set of subtasks, etc. This is supposed to make planning easier, since in order to attain larger goals a user can see how to split them into smaller, easier tasks.

See [the final state of the program](./documentation/current_state.md) in the frame of the course with the implemented use cases as well as corresponding SQL-clauses.

You can find a more detailed [description about the topic](./documentation/description.md) and more [about the database](./documentation/aboutdatabase.md). Here is(was) the updating list of [user stories](https://github.com/perander/training-planner/projects/1) according to the time or their implementation.

See the [user guide](./documentation/userguide.md) and instructions on [how to install](./documentation/install.md) the application locally and in heroku.

The application is in [heroku](https://tsoha-training-planner.herokuapp.com). Example credentials are:

username | password | admin |
--- |--- |--- |
theadmin | theadmin | True
hello | hello | False
new | new | False

It is however also possible to register a new user.