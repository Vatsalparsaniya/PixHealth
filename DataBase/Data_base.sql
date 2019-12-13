-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sys
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `basic_details`
--

DROP TABLE IF EXISTS `basic_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `basic_details` (
  `Name` varchar(45) NOT NULL,
  `DOB` varchar(45) NOT NULL,
  `Number` varchar(45) NOT NULL,
  `AGE` varchar(45) NOT NULL,
  `Height` varchar(45) NOT NULL,
  `Dagnosis` varchar(45) NOT NULL,
  `Allergies` varchar(45) NOT NULL,
  `CardNumber` varchar(45) NOT NULL,
  PRIMARY KEY (`CardNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `basic_details`
--

LOCK TABLES `basic_details` WRITE;
/*!40000 ALTER TABLE `basic_details` DISABLE KEYS */;
INSERT INTO `basic_details` VALUES ('vatsal','03/09/1999','8460422610','20','173','Headache','Food Allergy','188320981535'),('jinish','02/02/2001','6789054321','19','152','Depression','Allergic asthma','30870680586'),('darshit','03/06/1997','1234567890','22','167','Hearing Loss','Animal Allergy','328435987208'),('bhautik','04/11/1998','9876543210','21','168','Depression','-','760207156235');
/*!40000 ALTER TABLE `basic_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chemist`
--

DROP TABLE IF EXISTS `chemist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chemist` (
  `EMAIL` varchar(40) NOT NULL,
  `PASSWORD` varchar(45) NOT NULL,
  `UNAME` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`EMAIL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chemist`
--

LOCK TABLES `chemist` WRITE;
/*!40000 ALTER TABLE `chemist` DISABLE KEYS */;
INSERT INTO `chemist` VALUES ('bhautik@gmail.com','12345678',NULL),('jinish@gmail.com','12345678',NULL),('parth@gmail.com','12345678',NULL),('vatsal@gmail.com','12345678',NULL);
/*!40000 ALTER TABLE `chemist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `USER` varchar(30) NOT NULL,
  `EMAIL` varchar(35) NOT NULL,
  `PASSWORD` varchar(30) NOT NULL,
  PRIMARY KEY (`USER`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES ('bhautik','bhautik@gmail.com','12345678'),('darshit','darshit@gmail.com','12345678'),('tanmeet','tanmeet@gmail.com','12345678'),('vatsal','vatsal@gmail.com','12345678');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `p_medical_visits`
--

DROP TABLE IF EXISTS `p_medical_visits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `p_medical_visits` (
  `CARDNO` varchar(30) NOT NULL,
  `CASE_FLOW_NO` varchar(45) NOT NULL,
  `DOCTOR` varchar(45) NOT NULL,
  `HOSPITAL` varchar(45) NOT NULL,
  `DATE` varchar(45) NOT NULL,
  `DIAGNOSIS` varchar(125) NOT NULL,
  `PRESCRIOPTION` varchar(145) NOT NULL,
  `REPORTLINK` varchar(145) NOT NULL,
  PRIMARY KEY (`DOCTOR`,`DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `p_medical_visits`
--

LOCK TABLES `p_medical_visits` WRITE;
/*!40000 ALTER TABLE `p_medical_visits` DISABLE KEYS */;
INSERT INTO `p_medical_visits` VALUES ('328435987208','1','bhautik','wockhardt','2019-11-1 22:06:20.930374','abc','xyz','http://xyz...'),('328435987208','15','bhautik','wockhardt','2019-12-1 22:06:20.930374','abc','xyz','http://xyz...'),('30870680586','5','darshit','sterling','2019-11-1 22:06:20.930374','pqr','abc','http://xyz...'),('30870680586','6','darshit','sterling','2019-12-1 22:06:20.930374','asd','rtre','http://xyz...'),('188320981535','7','tanmeet','Apolo','2019-11-1 22:06:20.930374','pqr','abc','http://xyz...'),('188320981535','8','tanmeet','Apolo','2019-12-1 22:06:20.930374','abc','xyx','http://xyz...'),('760207156235','10','vatsal','zydus','2019-11-1 22:06:20.930374','abc','xyz','http://xyz...'),('760207156235','12','vatsal','zydus','2019-12-1 22:06:20.930374','abc','xyz','http://xyz...'),('328435987208','12','vatsal','temp','2019-12-12 14:55:03.170641','temp','temp','temp'),('188320981535','3','vatsal','temp','2019-12-12 14:55:30.605386','temp','temp','temp');
/*!40000 ALTER TABLE `p_medical_visits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `CARDNO` varchar(40) NOT NULL,
  `USER` varchar(45) NOT NULL,
  `EMAIL` varchar(45) NOT NULL,
  `PASSWORD` varchar(45) NOT NULL,
  PRIMARY KEY (`CARDNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES ('188320981535','vatsal','vatsal@gmail.com','12345678'),('30870680586','tanmeet','tanmeet@gmail.com','12345678'),('328435987208','darshit','darshit@gmail.com','12345678'),('760207156235','twinkle','twinkle@gmail.com','12345678');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-13 20:02:51
