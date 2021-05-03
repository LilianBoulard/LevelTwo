# Database

We use an SQL (relational) database, which will be used to store information relative to the project.

## Structure

It contains five tables:


### ``objects``

- Goal: hold information about the objects of the game
- 6 columns:
  1. ``id`` - primary identifier
  2. ``name`` - the name of the object
  3. ``effect`` - an integer linked to the `Effects` enumerator, indicating which effect it has on the player / level
  4. ``traversable`` - a boolean indicating whether a character can pass through
  5. ``min_instances`` - how many instances can there be at least in a single level
  6. ``max_instances`` - how many instances can there be at most in a single level


### ``levels``

- Goal: hold information about each level
- 6 columns:
  1. ``id`` - primary identifier
  2. ``name`` - the name of the level (can be entered by the user)
  3. ``author`` - the author name, as a string
  4. ``shape`` - the shape of the level, formatted like `x,y`
  5. ``creation_date`` - the date the level was submitted
  6. ``last_modification_date`` - the date the level was last modified


### ``levels_content``

- Goal: hold a data structure capable of storing the content of each level
- 5 columns:
  1. ``id`` - primary identifier
  2. ``level_id`` - the ID of the level it is linked to, from the `levels` table
  3. ``pos_x`` - the `x` coordinate of the cell
  4. ``pos_y`` - the `y` coordinate of the cell
  5. ``value`` - the value of the cell: an integer linked to the id of the object, from the ``objects`` database


### `tests`

- Goal: hold information about each test performed
- 3 columns:
  1. ``id`` - primary identifier
  2. ``algorithm`` - the name of the algorithm used for this test
  3. ``run_date`` - the date the test was ran


### `tests_content`

- Goal: hold information about the content of the test, usually pathfinding steps
- 5 columns:
  1. ``id`` - primary identifier
  2. ``test_id`` - the ID of the test it is linked to, from the `tests` table
  3. ``step`` - the step index
  4. ``pos_x`` - the `x` coordinate of the character at the end of this step
  5. ``pos_y`` - the `y` coordinate of the character at the end of this step
