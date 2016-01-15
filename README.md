### Apeksha IIT-JEE online mock test

#### Setup
	##### Database setup
	```sh
		CREATE DATABASE apeksha;
		CREATE TABLE `apeksha`.`user` (
		  `user_id` BIGINT NULL AUTO_INCREMENT,
		  `user_password` VARCHAR(45) NULL,
		  `email` VARCHAR(45) NULL,
		  `name` VARCHAR(45) NULL,
		  PRIMARY KEY (`user_id`));
	```
	##### Run app
		```py
			python runserver.py
		```