CREATE DATABASE IF NOT EXISTS `workers`;
USE `workers`;
CREATE TABLE `workers`.`workers` (
  `workerid` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NULL,
  `lastname` VARCHAR(45) NULL,
  `age` INT NULL,
  `id` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`workerid`));

ALTER TABLE `workers`.`workers`
ADD UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE;
;
INSERT into workers(firstname,lastname,age,id,email) VALUES ('omri','gigi',22,'000','mail');
