-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ProjPy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ProjPy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ProjPy` DEFAULT CHARACTER SET utf8 ;
USE `ProjPy` ;

-- -----------------------------------------------------
-- Table `ProjPy`.`game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjPy`.`game` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `gameCode` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ProjPy`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjPy`.`players` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pseudo` VARCHAR(20) NOT NULL,
  `password` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `pseudo_UNIQUE` (`pseudo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ProjPy`.`gameplay`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjPy`.`gameplay` (
  `game_id` INT NOT NULL,
  `players_id` INT NOT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  `timePlayed` VARCHAR(45) NOT NULL,
  `hitNumber` INT NOT NULL,
  `totalNumber` INT NOT NULL,
  `date` DATETIME NOT NULL,
  INDEX `fk_game_has_players_players1_idx` (`players_id` ASC) VISIBLE,
  INDEX `fk_game_has_players_game_idx` (`game_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_game_has_players_game`
    FOREIGN KEY (`game_id`)
    REFERENCES `ProjPy`.`game` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_has_players_players1`
    FOREIGN KEY (`players_id`)
    REFERENCES `ProjPy`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = INNODB;

-- Listage des données de la table projpy.game : ~3 rows (environ)
INSERT INTO `game` (`id`, `gameCode`) VALUES
	(10, 'GEO01'),
	(11, 'INFO02'),
	(12, 'INFO05');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
