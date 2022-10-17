-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema utagDb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema utagDb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `utagDb` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema utagdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema utagdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `utagdb` DEFAULT CHARACTER SET utf8 ;
USE `utagDb` ;

-- -----------------------------------------------------
-- Table `utagDb`.`lecturer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`lecturer` (
  `surname` VARCHAR(45) NOT NULL,
  `othername` VARCHAR(50) NULL,
  `email` VARCHAR(255) NOT NULL,
  `hashedPassword` VARCHAR(128) NOT NULL,
  `phoneNumber` VARCHAR(10) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `staffId` VARCHAR(7) NULL,
  `priority` INT NOT NULL DEFAULT 0,
  `verifiedMail` ENUM("YES", "NO") NULL DEFAULT 'NO',
  `verifiedLecturer` ENUM("YES", "NO") NULL DEFAULT 'NO',
  `idLecturer` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idLecturer`),
  UNIQUE INDEX `phoneNumber_UNIQUE` (`phoneNumber` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `lecturerId_UNIQUE` (`staffId` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `utagDb`.`bookingList`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`bookingList` (
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `bookingId` INT NOT NULL AUTO_INCREMENT,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`bookingId`, `idLecturer`),
  INDEX `fk_bookingList_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_bookingList_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagDb`.`lecturer` (`idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `utagDb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`admin` (
  `username` VARCHAR(20) NULL,
  `hashedPassword` VARCHAR(128) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `adminId` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`adminId`));


-- -----------------------------------------------------
-- Table `utagDb`.`selectedApplicants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`selectedApplicants` (
  `accepted` ENUM("YES", "NO", "NULL") NULL DEFAULT NULL,
  `applicationId` INT NOT NULL AUTO_INCREMENT,
  `idLecturer` INT NOT NULL,
  `sold` ENUM("YES", "NO") NULL DEFAULT 'NO',
  PRIMARY KEY (`applicationId`, `idLecturer`),
  INDEX `fk_selectedApplicants_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_selectedApplicants_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagDb`.`lecturer` (`idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `utagDb`.`applicationWindow`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`applicationWindow` (
  `startTime` TIMESTAMP NOT NULL,
  `endTime` TIMESTAMP NOT NULL,
  `slots` INT NOT NULL,
  `acceptanceDeadline` TIMESTAMP NULL);


-- -----------------------------------------------------
-- Table `utagDb`.`Verification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`Verification` (
  `idVerification` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(5) NULL,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`idVerification`, `idLecturer`),
  INDEX `fk_Verification_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_Verification_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagDb`.`lecturer` (`idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `utagDb`.`wardInfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`wardInfo` (
  `surname` VARCHAR(45) NULL,
  `othername` VARCHAR(45) NULL,
  `referenceNumber` VARCHAR(8) NULL,
  `gender` ENUM("M", "F") NULL,
  `wardInfoId` INT NOT NULL AUTO_INCREMENT,
  `applicationId` INT NOT NULL,
  `idLecturer` INT NOT NULL,
  `hostel` VARCHAR(45) NULL,
  `roomNumber` VARCHAR(45) NULL,
  PRIMARY KEY (`wardInfoId`, `applicationId`, `idLecturer`),
  INDEX `fk_wardInfo_selectedApplicants1_idx` (`applicationId` ASC, `idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `applicationId_UNIQUE` (`applicationId` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_wardInfo_selectedApplicants1`
    FOREIGN KEY (`applicationId` , `idLecturer`)
    REFERENCES `utagDb`.`selectedApplicants` (`applicationId` , `idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `utagDb`.`sellingbed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`sellingbed` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `applicationId` INT NOT NULL,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`Id`, `idLecturer`, `applicationId`),
  INDEX `fk_sellingbed_selectedApplicants1_idx` (`applicationId` ASC, `idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `applicationId_UNIQUE` (`applicationId` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_sellingbed_selectedApplicants1`
    FOREIGN KEY (`applicationId` , `idLecturer`)
    REFERENCES `utagDb`.`selectedApplicants` (`applicationId` , `idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `utagDb`.`Bid`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagDb`.`Bid` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `lecturer_idLecturer` INT NOT NULL,
  `sellingbed_Id` INT NOT NULL,
  `sellingbed_selectedApplicants_idLecturer` INT NOT NULL,
  `sellingbed_selectedApplicants_applicationId` INT NOT NULL,
  PRIMARY KEY (`Id`, `lecturer_idLecturer`, `sellingbed_Id`, `sellingbed_selectedApplicants_idLecturer`, `sellingbed_selectedApplicants_applicationId`),
  INDEX `fk_Bid_lecturer1_idx` (`lecturer_idLecturer` ASC) VISIBLE,
  INDEX `fk_Bid_sellingbed1_idx` (`sellingbed_Id` ASC, `sellingbed_selectedApplicants_idLecturer` ASC, `sellingbed_selectedApplicants_applicationId` ASC) VISIBLE,
  CONSTRAINT `fk_Bid_lecturer1`
    FOREIGN KEY (`lecturer_idLecturer`)
    REFERENCES `utagDb`.`lecturer` (`idLecturer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Bid_sellingbed1`
    FOREIGN KEY (`sellingbed_Id` , `sellingbed_selectedApplicants_idLecturer` , `sellingbed_selectedApplicants_applicationId`)
    REFERENCES `utagDb`.`sellingbed` (`Id` , `idLecturer` , `applicationId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `utagdb` ;

-- -----------------------------------------------------
-- Table `utagdb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`admin` (
  `username` VARCHAR(20) NULL DEFAULT NULL,
  `hashedPassword` VARCHAR(128) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `adminId` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`adminId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`applicationwindow`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`applicationwindow` (
  `startTime` TIMESTAMP NOT NULL,
  `endTime` TIMESTAMP NOT NULL,
  `slots` INT NOT NULL,
  `acceptanceDeadline` TIMESTAMP NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`lecturer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`lecturer` (
  `surname` VARCHAR(45) NOT NULL,
  `othername` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(255) NOT NULL,
  `hashedPassword` VARCHAR(128) NOT NULL,
  `phoneNumber` VARCHAR(10) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `staffId` VARCHAR(7) NULL DEFAULT NULL,
  `priority` INT NOT NULL DEFAULT '0',
  `verifiedMail` ENUM('YES', 'NO') NULL DEFAULT 'NO',
  `verifiedLecturer` ENUM('YES', 'NO') NULL DEFAULT 'NO',
  `idLecturer` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idLecturer`),
  UNIQUE INDEX `phoneNumber_UNIQUE` (`phoneNumber` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `lecturerId_UNIQUE` (`staffId` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`selectedapplicants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`selectedapplicants` (
  `accepted` ENUM('YES', 'NO', 'NULL') NULL DEFAULT NULL,
  `applicationId` INT NOT NULL AUTO_INCREMENT,
  `idLecturer` INT NOT NULL,
  `sold` ENUM('YES', 'NO') NULL DEFAULT 'NO',
  PRIMARY KEY (`applicationId`, `idLecturer`),
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  INDEX `fk_selectedApplicants_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_selectedApplicants_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagdb`.`lecturer` (`idLecturer`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`sellingbed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`sellingbed` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `applicationId` INT NOT NULL,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`Id`, `idLecturer`, `applicationId`),
  UNIQUE INDEX `applicationId_UNIQUE` (`applicationId` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  INDEX `fk_sellingbed_selectedApplicants1_idx` (`applicationId` ASC, `idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_sellingbed_selectedApplicants1`
    FOREIGN KEY (`applicationId` , `idLecturer`)
    REFERENCES `utagdb`.`selectedapplicants` (`applicationId` , `idLecturer`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`bid`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`bid` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `lecturer_idLecturer` INT NOT NULL,
  `sellingbed_Id` INT NOT NULL,
  `sellingbed_selectedApplicants_idLecturer` INT NOT NULL,
  `sellingbed_selectedApplicants_applicationId` INT NOT NULL,
  PRIMARY KEY (`Id`, `lecturer_idLecturer`, `sellingbed_Id`, `sellingbed_selectedApplicants_idLecturer`, `sellingbed_selectedApplicants_applicationId`),
  UNIQUE INDEX `lecturer_idLecturer_UNIQUE` (`lecturer_idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `sellingbed_Id_UNIQUE` (`sellingbed_Id` ASC) VISIBLE,
  UNIQUE INDEX `sellingbed_selectedApplicants_idLecturer_UNIQUE` (`sellingbed_selectedApplicants_idLecturer` ASC) VISIBLE,
  UNIQUE INDEX `sellingbed_selectedApplicants_applicationId_UNIQUE` (`sellingbed_selectedApplicants_applicationId` ASC) VISIBLE,
  INDEX `fk_Bid_lecturer1_idx` (`lecturer_idLecturer` ASC) VISIBLE,
  INDEX `fk_Bid_sellingbed1_idx` (`sellingbed_Id` ASC, `sellingbed_selectedApplicants_idLecturer` ASC, `sellingbed_selectedApplicants_applicationId` ASC) VISIBLE,
  CONSTRAINT `fk_Bid_lecturer1`
    FOREIGN KEY (`lecturer_idLecturer`)
    REFERENCES `utagdb`.`lecturer` (`idLecturer`),
  CONSTRAINT `fk_Bid_sellingbed1`
    FOREIGN KEY (`sellingbed_Id` , `sellingbed_selectedApplicants_idLecturer` , `sellingbed_selectedApplicants_applicationId`)
    REFERENCES `utagdb`.`sellingbed` (`Id` , `idLecturer` , `applicationId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`bookinglist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`bookinglist` (
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `bookingId` INT NOT NULL AUTO_INCREMENT,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`bookingId`, `idLecturer`),
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  INDEX `fk_bookingList_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_bookingList_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagdb`.`lecturer` (`idLecturer`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`verification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`verification` (
  `idVerification` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `code` VARCHAR(5) NULL DEFAULT NULL,
  `idLecturer` INT NOT NULL,
  PRIMARY KEY (`idVerification`, `idLecturer`),
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  INDEX `fk_Verification_lecturer1_idx` (`idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_Verification_lecturer1`
    FOREIGN KEY (`idLecturer`)
    REFERENCES `utagdb`.`lecturer` (`idLecturer`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `utagdb`.`wardinfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `utagdb`.`wardinfo` (
  `surname` VARCHAR(45) NULL DEFAULT NULL,
  `othername` VARCHAR(45) NULL DEFAULT NULL,
  `referenceNumber` VARCHAR(8) NULL DEFAULT NULL,
  `gender` ENUM('M', 'F') NULL DEFAULT NULL,
  `wardInfoId` INT NOT NULL AUTO_INCREMENT,
  `applicationId` INT NOT NULL,
  `idLecturer` INT NOT NULL,
  `hostel` VARCHAR(45) NULL DEFAULT NULL,
  `roomNumber` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`wardInfoId`, `applicationId`, `idLecturer`),
  UNIQUE INDEX `applicationId_UNIQUE` (`applicationId` ASC) VISIBLE,
  UNIQUE INDEX `idLecturer_UNIQUE` (`idLecturer` ASC) VISIBLE,
  INDEX `fk_wardInfo_selectedApplicants1_idx` (`applicationId` ASC, `idLecturer` ASC) VISIBLE,
  CONSTRAINT `fk_wardInfo_selectedApplicants1`
    FOREIGN KEY (`applicationId` , `idLecturer`)
    REFERENCES `utagdb`.`selectedapplicants` (`applicationId` , `idLecturer`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
