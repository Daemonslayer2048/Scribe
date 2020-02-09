PRAGMA foreign_keys = ON;

CREATE TABLE users (
  'pk' INTEGER PRIMARY KEY,
  'username' TEXT NOT NULL UNIQUE,
  'group' INTEGER,
  FOREIGN KEY ('group')
    REFERENCES groups ('pk')
);

CREATE TABLE groups (
  'pk' INTEGER PRIMARY KEY,
  'groupname' TEXT NOT NULL UNIQUE
);

CREATE TABLE device_models (
  'pk' INTEGER PRIMARY KEY,
  'manufacturer' TEXT NOT NULL,
  'model' TEXT NOT NULL,
  'OS' TEXT
);

CREATE TABLE repos (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'repo_name' TEXT NOT NULL UNIQUE,
	'remote_repo' TEXT DEFAULT NULL,
	FOREIGN KEY ('remote_repo') REFERENCES remote_repos ('repo_name')
);

CREATE TABLE remote_repos (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'repo_name' TEXT NOT NULL UNIQUE,
	'URL' TEXT NOT NULL UNIQUE
);

CREATE TABLE proxies (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'ip' TEXT NOT NULL,
  	'port' INT DEFAULT 22,
  	'username' TEXT NOT NULL,
    'password' TEXT NOT NULL
);

CREATE TABLE devices (
  'pk' INTEGER PRIMARY KEY,
  'ip' TEXT NOT NULL,
  'port' INT DEFAULT 22,
  'alias' TEXT,
  'model' TEXT NOT NULL,
  'user' TEXT,
  'username' TEXT NOT NULL,
  'password' TEXT NOT NULL,
  'enable' TEXT,
  'last_updated' TEXT NOT NULL DEFAULT "Never",
  'enabled' TEXT NOT NULL DEFAULT "True",
  'repo' TEXT NOT NULL DEFAULT "Default",
  'proxy' INTEGER DEFAULT NULL,
  CONSTRAINT fk_models
    FOREIGN KEY ('model')
    REFERENCES device_models ('pk'),
  CONSTRAINT fk_repo
  	FOREIGN KEY ('repo')
  	REFERENCES repos ('repo_name'),
  FOREIGN KEY ('proxy')
    REFERENCES proxies ('pk')
);

INSERT INTO repos (repo_name) VALUES ("Default");
