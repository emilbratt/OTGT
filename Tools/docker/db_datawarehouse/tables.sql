-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: CIP
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `article_id` int(10) unsigned NOT NULL,
  `brand_id` int(10) unsigned DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  KEY `article_id` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `barcodes`
--

DROP TABLE IF EXISTS `barcodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `barcodes` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `barcode` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brands`
--

DROP TABLE IF EXISTS `brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brands` (
  `brand_id` int(10) unsigned NOT NULL,
  `brand_name` varchar(255) NOT NULL,
  KEY `brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cip_cache`
--

DROP TABLE IF EXISTS `cip_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cip_cache` (
  `mem_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `mem_key` varchar(255) NOT NULL,
  `mem_val` varchar(4096) NOT NULL
) ENGINE=MEMORY DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `imports`
--

DROP TABLE IF EXISTS `imports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imports` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `import_qty` int(11) NOT NULL,
  `stock_qty` int(11) DEFAULT NULL,
  `stock_location` char(10) DEFAULT NULL,
  `supply_id` varchar(255) DEFAULT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `placement`
--

DROP TABLE IF EXISTS `placement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `placement` (
  `article_id` int(10) unsigned NOT NULL,
  `stock_location` char(10) NOT NULL,
  `timestamp` char(30) NOT NULL,
  `yyyymmdd` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `placement_invalid`
--

DROP TABLE IF EXISTS `placement_invalid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `placement_invalid` (
  `barcode` varchar(255) NOT NULL,
  `stock_location` char(10) NOT NULL,
  `timestamp` char(30) NOT NULL,
  `yyyymmdd` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales` (
  `article_id` int(10) unsigned NOT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `sold_qty` int(11) NOT NULL,
  `date` char(10) NOT NULL,
  `time` char(5) NOT NULL,
  `price` decimal(18,2) DEFAULT NULL,
  `discount` decimal(18,2) DEFAULT NULL,
  `pay_method` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sales_count`
--

DROP TABLE IF EXISTS `sales_count`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_count` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sales_hourly`
--

DROP TABLE IF EXISTS `sales_hourly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_hourly` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `soldout`
--

DROP TABLE IF EXISTS `soldout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `soldout` (
  `article_id` int(10) unsigned DEFAULT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `art_name` varchar(255) NOT NULL,
  `stock_qty` int(11) DEFAULT NULL,
  `stock_location` varchar(255) DEFAULT NULL,
  `last_import` char(10) DEFAULT NULL,
  `supply_id` varchar(255) DEFAULT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `week` int(11) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turnover_daily`
--

DROP TABLE IF EXISTS `turnover_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnover_daily` (
  `sum` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turnover_hourly`
--

DROP TABLE IF EXISTS `turnover_hourly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnover_hourly` (
  `00` int(11) NOT NULL,
  `01` int(11) NOT NULL,
  `02` int(11) NOT NULL,
  `03` int(11) NOT NULL,
  `04` int(11) NOT NULL,
  `05` int(11) NOT NULL,
  `06` int(11) NOT NULL,
  `07` int(11) NOT NULL,
  `08` int(11) NOT NULL,
  `09` int(11) NOT NULL,
  `10` int(11) NOT NULL,
  `11` int(11) NOT NULL,
  `12` int(11) NOT NULL,
  `13` int(11) NOT NULL,
  `14` int(11) NOT NULL,
  `15` int(11) NOT NULL,
  `16` int(11) NOT NULL,
  `17` int(11) NOT NULL,
  `18` int(11) NOT NULL,
  `19` int(11) NOT NULL,
  `20` int(11) NOT NULL,
  `21` int(11) NOT NULL,
  `22` int(11) NOT NULL,
  `23` int(11) NOT NULL,
  `year` smallint(6) NOT NULL,
  `month` tinyint(4) NOT NULL,
  `date` tinyint(4) NOT NULL,
  `week` tinyint(4) NOT NULL,
  `weekday` char(10) NOT NULL,
  `yyyymmdd` int(11) NOT NULL,
  `humandate` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-13 19:45:23
