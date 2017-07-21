# SchemaComparer

Python scripts that provides differences between given schemas based on metadata from the supported DBMS.

In the initial version, it prints in form of tables the information of differences like:

- Created / Dropped tables;

- Altered tables;

- Created / Dropped foreign keys;

- Created / Dropped primary keys;

- Created / Dropped uniques;

- Created / Dropped indexes;

- Created / Dropped functions;

- Altered functions fields;

- Altered functions definitions.

How to execute it:

- Alter line 12 and 13 of PostgreSQL.py, providing the data about your databases connections;

- Call the script PostgreSQL.py passing the name of the schema to be compared between the configured connections. Example: python PostgreSQL.py myschema;

- If there are differences in some of the categories described above, it will print a corresponding category table. Column 'status' takes 3 possible values:

> - **I**: inserted;
> - **D**: deleted;
> - **U**: updated. In this case, the "names" in column 'diff' will indicate where the differences are, and in the columns that correspond to such "names", the difference will be showed.

Uses the following libraries:

- [Spartacus](https://github.com/wind39/spartacus);

- [OmniDatabase](https://github.com/OmniDB/OmniDatabase).

This is a Work in Progress.
