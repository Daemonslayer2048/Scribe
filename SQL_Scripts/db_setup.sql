PRAGMA foreign_keys = 1;

create table users (
  'pk' INTEGER PRIMARY KEY,
  'username' text NOT NULL UNIQUE
);

create table device_models (
  'pk' INTEGER PRIMARY KEY,
  'manufacturer' text NOT NULL,
  'model' text NOT NULL,
  'OS' text
);

create table devices (
  'pk' INTEGER PRIMARY KEY,
  'ip' text NOT NULL,
  'port' INT DEFAULT 22,
  'alias' text,
  'model' text NOT NULL,
  'user' text,
  'username' text NOT NULL,
  'password' text NOT NULL,
  'enable' text,
  'last_updated' text DEFAULT "Never",
  'enabled' text DEFAULT "True",
  CONSTRAINT fk_models
    FOREIGN KEY ('model')
    REFERENCES device_models ('pk')
);

create table config (

);

create table proxies (

);

INSERT INTO device_models ("manufacturer", "Model", "OS") VALUES ("Ubiquiti", "Edge Switch", "EdgeOS");
INSERT INTO devices (ip, alias, model, username, password, enable) VALUES ("10.0.10.2", "Rack Switch", 1, "ubnt", "ubnt", "Fpd2485um1489w*");