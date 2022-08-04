-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema GreenTree
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema GreenTree
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `GreenTree` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `GreenTree` ;

-- -----------------------------------------------------
-- Table `GreenTree`.`attributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GreenTree`.`attributes` (
  `attribute_id` INT NOT NULL AUTO_INCREMENT,
  `attribute_name` VARCHAR(64) NOT NULL,
  `attribute_description` VARCHAR(256) NULL DEFAULT NULL,
  `attribute_active` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`attribute_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 78
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `GreenTree`.`product_attributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GreenTree`.`product_attributes` (
  `product_attribute_id` INT NOT NULL AUTO_INCREMENT,
  `product_id` INT NOT NULL,
  `attribute_id` INT NOT NULL,
  `attribute_value` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`product_attribute_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 153
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `GreenTree`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GreenTree`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(128) NOT NULL,
  `product_description` VARCHAR(512) NULL DEFAULT NULL,
  `product_active` TINYINT NOT NULL DEFAULT '0',
  `product_image_filepath` VARCHAR(128) NULL DEFAULT NULL,
  `product_type` VARCHAR(45) NULL DEFAULT NULL,
  `product_brand` VARCHAR(45) NULL DEFAULT NULL,
  `product_price` VARCHAR(45) NULL DEFAULT NULL,
  `product_discount_price` VARCHAR(45) NULL DEFAULT NULL,
  `product_strain` VARCHAR(45) NULL DEFAULT NULL,
  `product_strain_type` VARCHAR(45) NULL DEFAULT NULL,
  `product_thc_percentage` VARCHAR(45) NULL DEFAULT NULL,
  `product_size` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`product_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 963
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `GreenTree`.`strains`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GreenTree`.`strains` (
  `strain_id` INT NOT NULL AUTO_INCREMENT,
  `strain_name` VARCHAR(64) NOT NULL,
  `strain_type` VARCHAR(6) NOT NULL,
  `thc_percentage` FLOAT NOT NULL,
  `image_filepath_1` VARCHAR(64) NULL DEFAULT NULL,
  `image_filepath_2` VARCHAR(64) NULL DEFAULT NULL,
  `image_filepath_3` VARCHAR(64) NULL DEFAULT NULL,
  `image_filepath_4` VARCHAR(64) NULL DEFAULT NULL,
  `strain_description` VARCHAR(256) NULL DEFAULT NULL,
  PRIMARY KEY (`strain_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
