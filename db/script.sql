CREATE TABLE pacientes(
    id serial primary key,
    cedula varchar(10) unique not null,
    nombre varchar(100) not null,
    apellido varchar(100) not null,
    telefono varchar(10) not null,
    email varchar(100) not null
);