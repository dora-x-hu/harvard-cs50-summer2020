Documentation

### Opening the server
Run the server with $ flask run in the project directory and click on the link the terminal provides to open the server.
It will direct you to the home page; users are initially not logged in, so opening the server will direct users to the login page.

### Registering and Logging in
There are links on the right side of the navigation bar at the top of the page. Clicking on the "Register" link will send the user to a page with three text boxes for input:
one for a username, one for a password, and one for a password confirmation. If any of the fields are left blank, the inputs will not be submitted for registration. If the
password and confirmation do not match, the registrant will be redirected to a page with a message telling them to input matching passwords without their input being submitted.
Similarly, if another user has the same username as the username input, the input will not be submitted and the registrant will be asked to register with another password.
After a successful registration, the registrant will be redirected to the login page.

The login page has a form with input for a username and a password. If users submit the form without either input, the form will not submit.
If the username and password are invalid, the user will be directed to an apology page telling them to input a valid username and password.
After inputting a correct username and password, the user will be logged in and sent to the main page: the list of incomplete tasks.

### Adding tasks
When logged in, the navigation bar shows only one link on its right side and two on its left side. The left side's links read "Add" and "Completed".

Upon clicking "Add", the user will be directed to a form with five fields: one for the date of the task, two for the start and end time respectively, the type of task, and a
description of the task. All fields are initially blank. If the user submits the form with any blank fields(aside from "Tag"), the form will not submit and the user will
be told to fill in all the required fields that are empty. If the start time is after the end time, the user will be redirected to an apology page telling them to submit
appropriate start and end times.

After a task is successfully added, it will appear in the main task list, color-coded by its tag.

### The main page
After a successful login, users are directed to the main page, the one with the task list. It displays a table of tasks: it has columns for the date of the task, the start
and end times, the type of task, and a description of the task. The tasks are sorted in chronological order, with the most imminent tasks appearing first.

Each row also has buttons for marking tasks as complete, deleting the task, or editing the task. They appear as a green check mark, a red x, and "Edit".
Clicking on the button for completing or deleting tasks will both lead the user to a confirmation page. If the user clicks "No", the user will be directed back to the
task list page with no changes from before. If the user clicks "Yes", then they will be sent to the task list page with one difference from before: said task will no longer
be there. If the task was "completed", the task will appear on a list of completed tasks. If the task was deleted, it will not appear anywhere on the website.

The button reading "Edit" will lead the user to a page with a form identical in appearance and behavior to the form for adding fields. The key difference is that the form
for editing will initially contain the date, start and end times, tag, and description that said task currently has. After an edit is successfully submitted, the changes
to the task will appear on the main task list.

### Completed tasks
After tasks are marked complete, they appear on the list of completed tasks. The list of completed tasks can be accessed by clicking on "Completed" on the navigation bar.
It will lead the user to a page with a table of completed tasks, appearing in reverse chronological order (the most recent tasks appear first). Like the main task list, the
tasks are color-coded. Instead of having three buttons like the main task list, there is one button that reads "Retrieve". It will take said task and move it back to the
main task list. Like the complete and delete buttons though, it directs the user to a confirmation page before taking action.

### Logout
When logged in, the navigation shows one link on its right side: the logout. Upon clicking on this, the user currently signed in will be logged out and sent to the login
page.