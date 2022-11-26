create table if not exists departments(
id integer primary key,
department_name VARCHAR not null
);
create table if not exists employees(
id integer primary key,
employee_name VARCHAR not null,
department_id integer references departments(id),
chief boolean
);
