CREATE DATABASE  IF NOT EXISTS `esports` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `esports`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: esports
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `tournament_id` int NOT NULL,
  `team_1_id` int DEFAULT NULL,
  `team_2_id` int DEFAULT NULL,
  `team_1_roster_id` int NOT NULL,
  `team_2_roster_id` int NOT NULL,
  `start_time` int NOT NULL,
  `start_day` int NOT NULL,
  `start_month` int NOT NULL,
  `start_year` int NOT NULL,
  `duration` int NOT NULL COMMENT 'in minutes',
  `winner_team_id` int DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `game_id_UNIQUE` (`game_id`),
  KEY `tournament_id_idx` (`tournament_id`),
  KEY `team_1_id_idx` (`team_1_id`),
  KEY `team_2_id_idx` (`team_2_id`),
  KEY `team_1_roster_id_idx` (`team_1_roster_id`),
  KEY `team_2_roster_id_idx` (`team_2_roster_id`),
  CONSTRAINT `game_tournament_id` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`tournament_id`) ON DELETE CASCADE,
  CONSTRAINT `team_1_id` FOREIGN KEY (`team_1_id`) REFERENCES `team` (`team_id`) ON DELETE SET NULL,
  CONSTRAINT `team_1_roster_id` FOREIGN KEY (`team_1_roster_id`) REFERENCES `roster` (`roster_id`),
  CONSTRAINT `team_2_id` FOREIGN KEY (`team_2_id`) REFERENCES `team` (`team_id`) ON DELETE SET NULL,
  CONSTRAINT `team_2_roster_id` FOREIGN KEY (`team_2_roster_id`) REFERENCES `roster` (`roster_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,1,4,2,7,2,1600,12,4,2015,16,2),(2,1,1,3,1,5,1630,12,4,2015,32,3),(3,1,4,1,7,1,1900,12,4,2015,17,1),(4,1,2,3,2,5,1600,13,4,2015,46,2),(5,1,3,1,5,1,1700,13,4,2015,3,3),(6,1,2,3,2,5,1730,13,4,2015,53,2),(7,2,2,1,2,1,1400,25,12,2015,19,2),(8,2,4,3,7,5,1500,25,12,2015,56,3),(9,2,1,4,1,7,1700,25,12,2015,14,4),(10,2,2,3,2,5,1400,26,12,2015,62,2),(11,2,3,4,5,7,1545,26,12,2015,34,3),(12,2,2,3,3,5,1700,26,12,2015,46,3),(13,2,3,2,5,3,1400,27,12,2015,51,2),(14,3,3,2,5,3,1600,5,5,2016,49,3),(15,3,4,1,7,1,1700,5,5,2016,29,1),(16,3,2,4,3,7,1800,5,5,2016,11,2),(17,3,3,1,5,1,1600,6,5,2016,24,1),(18,3,3,2,5,3,1700,6,5,2016,46,2),(19,3,1,2,1,3,1800,6,5,2016,49,2),(20,3,2,1,3,1,1930,6,5,2016,52,2);
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_participant`
--

DROP TABLE IF EXISTS `game_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_participant` (
  `game_id` int NOT NULL,
  `player_id` int NOT NULL,
  `kills` int NOT NULL,
  `deaths` int NOT NULL,
  PRIMARY KEY (`game_id`,`player_id`),
  KEY `participant_plater_id_idx` (`player_id`),
  CONSTRAINT `participant_game_id` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`) ON DELETE CASCADE,
  CONSTRAINT `participant_player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_participant`
--

LOCK TABLES `game_participant` WRITE;
/*!40000 ALTER TABLE `game_participant` DISABLE KEYS */;
INSERT INTO `game_participant` VALUES (1,4,15,3),(1,5,11,6),(1,10,2,14),(1,11,6,11),(1,12,1,22),(1,13,20,0),(2,1,6,8),(2,2,9,5),(2,3,2,11),(2,7,6,7),(2,8,7,6),(2,9,11,4),(3,1,16,4),(3,2,26,1),(3,3,10,7),(3,10,3,13),(3,11,9,7),(3,12,0,32),(4,4,8,5),(4,5,5,7),(4,7,1,14),(4,8,4,11),(4,9,7,6),(4,13,18,0),(5,1,2,11),(5,2,3,7),(5,3,6,5),(5,7,6,5),(5,8,8,4),(5,9,9,2),(6,4,9,6),(6,5,7,9),(6,7,2,10),(6,8,5,13),(6,9,8,9),(6,13,16,0);
/*!40000 ALTER TABLE `game_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `in_game_name` varchar(45) NOT NULL,
  `team_id` int DEFAULT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `start_day` int DEFAULT NULL,
  `start_month` int DEFAULT NULL,
  `start_year` int DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `player_id_UNIQUE` (`player_id`),
  KEY `player_team_id_idx` (`team_id`),
  CONSTRAINT `player_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES (1,'Testdummy4',1,'Test','Dummy',5,12,1890),(2,'TestingCarapace',1,'Adam','Adam',5,12,1890),(3,'Rad_Gall',1,'Rag','Doll',5,12,1890),(4,'gigaChad',2,'Chad','Richard',4,3,2001),(5,'xXxFaZe_MaStEr_SwAgxXx',2,'Gabriel','Zachamaria',7,8,2005),(6,'JeremyGuy4',2,'Jeremy','Guy',4,4,2004),(7,'Elliot_Games',3,'Elliot','Smith',6,1,2007),(8,'JohnGamer',3,'John','Smith',4,3,2002),(9,'adamzzz',3,'Adam','Smith',29,12,2006),(10,'POOPOO2',4,'David','Davinci',2,7,2012),(11,'drPP',4,'Peter','Griffon',12,5,2010),(12,'EdatP',4,'Bryan','Lessland',15,12,2009),(13,'TheLegend27',NULL,'N','A',1,1,1997);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `player_kill_death_ratio`
--

DROP TABLE IF EXISTS `player_kill_death_ratio`;
/*!50001 DROP VIEW IF EXISTS `player_kill_death_ratio`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `player_kill_death_ratio` AS SELECT 
 1 AS `player_id`,
 1 AS `kill_death_ratio`,
 1 AS `games_played`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `roster`
--

DROP TABLE IF EXISTS `roster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roster` (
  `roster_id` int NOT NULL AUTO_INCREMENT,
  `team_id` int NOT NULL,
  PRIMARY KEY (`roster_id`),
  UNIQUE KEY `roster_id_UNIQUE` (`roster_id`),
  KEY `roster_team_id_idx` (`team_id`),
  CONSTRAINT `roster_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roster`
--

LOCK TABLES `roster` WRITE;
/*!40000 ALTER TABLE `roster` DISABLE KEYS */;
INSERT INTO `roster` VALUES (1,1),(2,2),(3,2),(5,3),(7,4);
/*!40000 ALTER TABLE `roster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roster_member`
--

DROP TABLE IF EXISTS `roster_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roster_member` (
  `roster_id` int NOT NULL,
  `player_id` int NOT NULL,
  PRIMARY KEY (`roster_id`,`player_id`),
  KEY `player_id_idx` (`player_id`),
  CONSTRAINT `player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`player_id`) ON DELETE CASCADE,
  CONSTRAINT `roster_id` FOREIGN KEY (`roster_id`) REFERENCES `roster` (`roster_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roster_member`
--

LOCK TABLES `roster_member` WRITE;
/*!40000 ALTER TABLE `roster_member` DISABLE KEYS */;
INSERT INTO `roster_member` VALUES (1,1),(1,2),(1,3),(2,4),(3,4),(2,5),(3,5),(3,6),(5,7),(5,8),(5,9),(7,10),(7,11),(7,12),(2,13);
/*!40000 ALTER TABLE `roster_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsor`
--

DROP TABLE IF EXISTS `sponsor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsor` (
  `sponsor_name` varchar(45) NOT NULL,
  `sponsored_team_id` int NOT NULL,
  PRIMARY KEY (`sponsor_name`),
  UNIQUE KEY `sponsor_name_UNIQUE` (`sponsor_name`),
  KEY `sponsor_team_id_idx` (`sponsored_team_id`),
  CONSTRAINT `sponsor_team_id` FOREIGN KEY (`sponsored_team_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsor`
--

LOCK TABLES `sponsor` WRITE;
/*!40000 ALTER TABLE `sponsor` DISABLE KEYS */;
INSERT INTO `sponsor` VALUES ('Monster',1),('G-Fuel',2),('Pepsi',2),('Domino\'s',3),('Republic of Gamers',3),('AT&T',4),('FTX',4);
/*!40000 ALTER TABLE `sponsor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `team_name` varchar(45) NOT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `team_id_UNIQUE` (`team_id`),
  UNIQUE KEY `team_name_UNIQUE` (`team_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (3,'Average team'),(4,'Loser team'),(1,'Test team'),(2,'Winner team');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `team_win_rates`
--

DROP TABLE IF EXISTS `team_win_rates`;
/*!50001 DROP VIEW IF EXISTS `team_win_rates`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `team_win_rates` AS SELECT 
 1 AS `team_id`,
 1 AS `win_rate`,
 1 AS `games_played`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `tournament`
--

DROP TABLE IF EXISTS `tournament`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tournament` (
  `tournament_id` int NOT NULL AUTO_INCREMENT,
  `tournament_name` varchar(45) NOT NULL,
  `start_day` int NOT NULL,
  `start_month` int NOT NULL,
  `start_year` int NOT NULL,
  `street_address` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`),
  UNIQUE KEY `tournament_id_UNIQUE` (`tournament_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament`
--

LOCK TABLES `tournament` WRITE;
/*!40000 ALTER TABLE `tournament` DISABLE KEYS */;
INSERT INTO `tournament` VALUES (1,'Test',12,4,2015,'420 Little Ceaser\'s Dr.','Rolla','WI'),(2,'Games Done Well',25,12,2015,'701 Convention Plaza','St. Louis','MO'),(3,'We The Best Videogame',5,5,2016,'1 Apple Park Way','Cupertino','CA');
/*!40000 ALTER TABLE `tournament` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tournament_participant`
--

DROP TABLE IF EXISTS `tournament_participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tournament_participant` (
  `tournament_id` int NOT NULL,
  `team_id` int NOT NULL,
  `result` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`,`team_id`),
  KEY `team_id_idx` (`team_id`),
  CONSTRAINT `participant_tournament_id` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`tournament_id`) ON DELETE CASCADE,
  CONSTRAINT `team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament_participant`
--

LOCK TABLES `tournament_participant` WRITE;
/*!40000 ALTER TABLE `tournament_participant` DISABLE KEYS */;
INSERT INTO `tournament_participant` VALUES (1,1,'3rd'),(1,2,'1st'),(1,3,'2nd'),(1,4,'4th'),(2,1,'4th'),(2,2,'1st'),(2,3,'2nd'),(2,4,'3rd'),(3,1,'2nd'),(3,2,'1st'),(3,3,'3rd'),(3,4,'4th');
/*!40000 ALTER TABLE `tournament_participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `player_kill_death_ratio`
--

/*!50001 DROP VIEW IF EXISTS `player_kill_death_ratio`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `player_kill_death_ratio` AS select `r`.`player_id` AS `player_id`,(`r`.`kills` / `r`.`deaths`) AS `kill_death_ratio`,count(`g`.`game_id`) AS `games_played` from ((select `p`.`player_id` AS `player_id`,`p`.`in_game_name` AS `in_game_name`,sum(`g`.`kills`) AS `kills`,sum(`g`.`deaths`) AS `deaths` from (`player` `p` left join `game_participant` `g` on((`g`.`player_id` = `p`.`player_id`))) group by `p`.`player_id`) `r` join `game_participant` `g` on((`r`.`player_id` = `g`.`player_id`))) group by `r`.`player_id` order by (`r`.`kills` / `r`.`deaths`) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `team_win_rates`
--

/*!50001 DROP VIEW IF EXISTS `team_win_rates`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `team_win_rates` AS select `w`.`team_id` AS `team_id`,(`w`.`wins` / count(`g`.`game_id`)) AS `win_rate`,count(`g`.`game_id`) AS `games_played` from ((select `t`.`team_id` AS `team_id`,`t`.`team_name` AS `team_name`,count(`g`.`game_id`) AS `wins` from (`team` `t` left join `game` `g` on((`g`.`winner_team_id` = `t`.`team_id`))) group by `t`.`team_id`) `w` join `game` `g` on(((`w`.`team_id` = `g`.`team_1_id`) or (`w`.`team_id` = `g`.`team_2_id`)))) group by `w`.`team_id` order by (`w`.`wins` / count(`g`.`game_id`)) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-08 21:50:18
