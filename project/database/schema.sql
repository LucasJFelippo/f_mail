CREATE DATABASE "project";

CREATE TABLE "user" (
	"cod" SERIAL, 
	"name" VARCHAR(100) NOT NULL,
	"nickname" VARCHAR(50) UNIQUE NOT NULL,
	"password" VARCHAR(92) NOT NULL,
	"verify" BOOLEAN DEFAULT False,
	"admin" BOOLEAN DEFAULT False,
	CONSTRAINT "UserPk" PRIMARY KEY ("cod"));

INSERT INTO "user" ("name", "nickname", "login") VALUES ('Tiago', 't', MD5('t'));