-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: reservations
-- ------------------------------------------------------
-- Server version	10.6.25-MariaDB

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
-- Table structure for table `artists`
--

DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artists` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(60) NOT NULL,
  `lastname` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists`
--

LOCK TABLES `artists` WRITE;
/*!40000 ALTER TABLE `artists` DISABLE KEYS */;
INSERT INTO `artists` (`id`, `firstname`, `lastname`) VALUES (1,'Daniel','Marcelin'),(2,'Philippe','Laurent'),(3,'Marius','Von Mayenburg'),(4,'Hicham','Ghassoul'),(5,'Sophie','Deprez'),(6,'Marc','Delcourt'),(7,'Isabelle','Warnier'),(8,'Jean-Luc','Piraux'),(9,'Nathalie','Uffner'),(10,'Pierre','Bodson'),(11,'Catherine','Claeys'),(12,'Antoine','Herbulot');
/*!40000 ALTER TABLE `artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `types` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
INSERT INTO `types` (`id`, `type`) VALUES (1,'rire'),(2,'Comédie'),(3,'Théâtre'),(4,'Drame'),(5,'One-man-show'),(6,'Danse'),(7,'Musique'),(8,'Improvisation');
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `localities`
--

DROP TABLE IF EXISTS `localities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `localities` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `postal_code` varchar(6) NOT NULL,
  `locality` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localities`
--

LOCK TABLES `localities` WRITE;
/*!40000 ALTER TABLE `localities` DISABLE KEYS */;
INSERT INTO `localities` (`id`, `postal_code`, `locality`) VALUES (1,'1000','Bruxelles'),(2,'1170','Watermael-Boitsfort'),(3,'1050','Ixelles'),(4,'1060','Saint-Gilles'),(5,'1080','Molenbeek-Saint-Jean'),(6,'1030','Schaerbeek'),(7,'1180','Uccle'),(8,'1190','Forest'),(9,'1140','Evere');
/*!40000 ALTER TABLE `localities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`id`, `role`) VALUES (1,'pdg'),(2,'Acteur'),(3,'Actrice'),(4,'Metteur en scène'),(5,'Metteuse en scène'),(6,'Comédien'),(7,'Comédienne'),(8,'Musicien');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) NOT NULL,
  `designation` varchar(60) NOT NULL,
  `address` varchar(255) NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `locality_id` bigint(20) DEFAULT NULL,
  `capacity` int(10) unsigned NOT NULL CHECK (`capacity` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `fk_locations_locality` (`locality_id`),
  CONSTRAINT `fk_locations_locality` FOREIGN KEY (`locality_id`) REFERENCES `localities` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` (`id`, `slug`, `designation`, `address`, `website`, `phone`, `locality_id`, `capacity`) VALUES (1,'espace-magh','Espace Magh','17 rue du Poincon','https://www.espacemagh.be','02/274.05.10',1,106),(2,'la-venerie','La Venerie','3 place Gilson','https://www.lavenerie.be','02/672.14.39',2,150),(3,'tto','Théâtre de la Toison d\'Or','Galeries de la Toison d\'Or 396',NULL,NULL,1,1000),(4,'theatre-national-bruxelles','Théâtre National de Bruxelles','Boulevard Emile Jacqmain 111-115','https://www.theatrenational.be','+32 2 203 41 55',1,800),(5,'theatre-les-riches-claires','Théâtre Les Riches Claires','Rue des Riches Claires 24','https://www.lesrichesclaires.be','+32 2 548 25 80',1,200),(6,'theatre-royal-du-parc','Théâtre Royal du Parc','Rue de la Loi 3','https://www.theatreduparc.be','+32 2 505 30 30',1,450),(7,'kaaitheater','Kaaitheater','Square Sainctelette 20','https://www.kaaitheater.be','+32 2 201 59 59',1,300);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shows`
--

DROP TABLE IF EXISTS `shows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shows` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `poster_url` varchar(255) DEFAULT NULL,
  `bookable` tinyint(1) NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `location_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `fk_shows_location` (`location_id`),
  CONSTRAINT `fk_shows_location` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shows`
--

LOCK TABLES `shows` WRITE;
/*!40000 ALTER TABLE `shows` DISABLE KEYS */;
INSERT INTO `shows` (`id`, `slug`, `title`, `description`, `poster_url`, `bookable`, `price`, `location_id`) VALUES (4,'le-prenom','Le Prénom','Venez découvrir Le Prénom, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=800',1,30.00,3),(5,'silence-on-tourne','Silence on tourne','Venez découvrir Silence on tourne, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800',1,22.50,3),(6,'edmond','Edmond','Venez découvrir Edmond, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',1,28.00,3),(8,'le-diner-de-cons','Le Dîner de Cons','Venez découvrir Le Dîner de Cons, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',1,24.00,3),(9,'boeing-boeing','Boeing Boeing','Venez découvrir Boeing Boeing, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800',1,20.00,3),(10,'toc-toc','Toc Toc','Venez découvrir Toc Toc, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800',1,23.00,3),(12,'intramuros','Intramuros','Venez découvrir Intramuros, une pièce unique dans le pur style du Théâtre de la Toison d\'Or.','https://images.unsplash.com/photo-1507915135761-41a0a222c709?w=800',1,29.00,3);
/*!40000 ALTER TABLE `shows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `representations`
--

DROP TABLE IF EXISTS `representations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `representations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `when` datetime(6) NOT NULL,
  `location_id` bigint(20) DEFAULT NULL,
  `show_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_representations_show` (`show_id`),
  KEY `fk_representations_location` (`location_id`),
  CONSTRAINT `fk_representations_location` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_representations_show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `representations`
--

LOCK TABLES `representations` WRITE;
/*!40000 ALTER TABLE `representations` DISABLE KEYS */;
INSERT INTO `representations` (`id`, `when`, `location_id`, `show_id`) VALUES (7,'2026-04-03 18:00:00.000000',3,4),(8,'2026-04-10 18:00:00.000000',3,4),(9,'2026-04-17 18:00:00.000000',3,4),(10,'2026-04-24 18:00:00.000000',3,4),(11,'2026-04-05 18:00:00.000000',3,5),(12,'2026-04-12 18:00:00.000000',3,5),(13,'2026-04-19 18:00:00.000000',3,5),(14,'2026-04-26 18:00:00.000000',3,5),(15,'2026-04-07 18:00:00.000000',3,6),(16,'2026-04-14 18:00:00.000000',3,6),(17,'2026-04-21 18:00:00.000000',3,6),(18,'2026-04-28 18:00:00.000000',3,6),(23,'2026-04-11 18:00:00.000000',3,8),(24,'2026-04-18 18:00:00.000000',3,8),(25,'2026-04-25 18:00:00.000000',3,8),(26,'2026-05-02 18:00:00.000000',3,8),(27,'2026-04-13 18:00:00.000000',3,9),(28,'2026-04-20 18:00:00.000000',3,9),(29,'2026-04-27 18:00:00.000000',3,9),(30,'2026-05-04 18:00:00.000000',3,9),(31,'2026-04-15 18:00:00.000000',3,10),(32,'2026-04-22 18:00:00.000000',3,10),(33,'2026-04-29 18:00:00.000000',3,10),(34,'2026-05-06 18:00:00.000000',3,10),(39,'2026-04-19 18:00:00.000000',3,12),(40,'2026-04-26 18:00:00.000000',3,12),(41,'2026-05-03 18:00:00.000000',3,12),(42,'2026-05-10 18:00:00.000000',3,12);
/*!40000 ALTER TABLE `representations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `places` int(10) unsigned NOT NULL CHECK (`places` >= 0),
  `representation_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reservations_representation` (`representation_id`),
  KEY `fk_reservations_user` (`user_id`),
  CONSTRAINT `fk_reservations_representation` FOREIGN KEY (`representation_id`) REFERENCES `representations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_reservations_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_reservations_places` CHECK (`places` >= 1)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` (`id`, `places`, `representation_id`, `user_id`) VALUES (32,5,40,8),(33,2,7,2),(34,1,12,2),(35,3,17,2),(36,4,9,8),(37,2,14,8),(38,1,26,1);
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artist_type`
--

DROP TABLE IF EXISTS `artist_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artist_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `artist_id` bigint(20) NOT NULL,
  `type_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_artist_type` (`artist_id`,`type_id`),
  KEY `fk_artist_type_type` (`type_id`),
  CONSTRAINT `fk_artist_type_artist` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_artist_type_type` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist_type`
--

LOCK TABLES `artist_type` WRITE;
/*!40000 ALTER TABLE `artist_type` DISABLE KEYS */;
INSERT INTO `artist_type` (`id`, `artist_id`, `type_id`) VALUES (1,1,1),(18,1,2),(19,2,3),(2,4,1),(3,5,2),(4,5,3),(5,6,2),(6,6,5),(7,7,3),(8,7,4),(9,8,2),(10,8,8),(11,9,3),(12,10,2),(13,10,3),(14,11,6),(15,11,7),(16,12,3),(17,12,4);
/*!40000 ALTER TABLE `artist_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artist_type_show`
--

DROP TABLE IF EXISTS `artist_type_show`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `artist_type_show` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `artist_type_id` bigint(20) NOT NULL,
  `show_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_artist_type_show` (`artist_type_id`,`show_id`),
  KEY `fk_ats_show` (`show_id`),
  CONSTRAINT `fk_ats_artist_type` FOREIGN KEY (`artist_type_id`) REFERENCES `artist_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ats_show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist_type_show`
--

LOCK TABLES `artist_type_show` WRITE;
/*!40000 ALTER TABLE `artist_type_show` DISABLE KEYS */;
INSERT INTO `artist_type_show` (`id`, `artist_type_id`, `show_id`) VALUES (3,2,9),(4,2,12),(17,3,4),(8,3,9),(18,5,4),(20,5,8),(9,5,9),(13,7,5),(5,7,6),(21,9,8),(19,10,4),(10,10,10),(12,11,10),(15,11,12),(7,12,6),(22,12,8),(16,13,12),(11,14,10),(6,16,6),(14,17,5);
/*!40000 ALTER TABLE `artist_type_show` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profiles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_profiles_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles`
--

LOCK TABLES `profiles` WRITE;
/*!40000 ALTER TABLE `profiles` DISABLE KEYS */;
INSERT INTO `profiles` (`id`, `image`, `user_id`) VALUES (3,'profile_pics/unnamed_LRFvY9W.jpg',8),(4,'default.jpg',1),(5,'default.jpg',2);
/*!40000 ALTER TABLE `profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_meta`
--

DROP TABLE IF EXISTS `user_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_meta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `langue` varchar(2) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `fk_user_meta_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_meta`
--

LOCK TABLES `user_meta` WRITE;
/*!40000 ALTER TABLE `user_meta` DISABLE KEYS */;
INSERT INTO `user_meta` (`id`, `langue`, `user_id`) VALUES (1,'fr',1),(2,'fr',2),(3,'nl',8);
/*!40000 ALTER TABLE `user_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `review` longtext NOT NULL,
  `stars` smallint(5) unsigned NOT NULL CHECK (`stars` >= 0),
  `validated` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `show_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_show` (`show_id`),
  KEY `fk_reviews_user` (`user_id`),
  CONSTRAINT `fk_reviews_show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `fk_reviews_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `chk_reviews_stars` CHECK (`stars` between 1 and 5)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` (`id`, `review`, `stars`, `validated`, `created_at`, `updated_at`, `show_id`, `user_id`) VALUES (1,'Excellent spectacle !',5,1,'2026-04-26 10:37:41.884894',NULL,4,1),(2,'j\'adore',5,0,'2026-04-26 11:26:32.142936',NULL,9,8),(3,'Belle mise en scène, très fidèle à l\'esprit de Rostand. Quelques longueurs dans le deuxième acte.',4,1,'2026-05-07 14:51:51.354553',NULL,6,8),(4,'J\'ai adoré ! Les six personnages sont tous attachants et les situations sont hilarantes.',5,1,'2026-05-07 14:51:51.357427',NULL,10,8),(5,'Bonne comédie de boulevard, sans grande surprise mais agréable à regarder.',3,1,'2026-05-07 14:51:51.360967',NULL,9,1),(6,'Un spectacle touchant et bien interprété. La salle était comble, c\'est mérité.',4,1,'2026-05-07 14:51:51.364369',NULL,12,1),(7,'Superbe ! La direction d\'acteurs est impeccable, on est transporté.',5,0,'2026-05-07 14:51:51.367467',NULL,5,2),(8,'Excellent spectacle, le texte est tres bien ecrit. Les acteurs sont convaincants.',4,1,'2026-05-07 14:53:54.617337',NULL,4,2),(9,'Un classique incontournable ! On rit du debut a la fin, le timing comique est parfait.',5,1,'2026-05-07 14:53:54.620474',NULL,8,2);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (1,'pbkdf2_sha256$1000000$UyEmTMR4CBJhbgIHgmdkeG$0CbNoh4Aw7UdL9xukSOu0XBwVTL/RenF30poohwgSOg=','2026-02-11 01:36:57.048389',1,'admin','','','',1,1,'2026-02-11 01:35:39.670467'),(2,'pbkdf2_sha256$1200000$J03eYTR1Jgi3Ja7ixaezUG$BGRtlJQRHRSzss+bTJZbsfBRuhgsofzk/k0NutLDeNY=','2026-04-14 20:36:31.160895',1,'hicham','','','',1,1,'2026-02-11 21:48:34.599310'),(8,'pbkdf2_sha256$1200000$aQ7Hn36NfTcWAmwEzE39OL$M2nVaqGaqbQle6R0GY2sz5IQDys1Ijei9Y0cYL4ewpo=','2026-04-24 21:28:06.333338',0,'hicham2026','Hicham','Ghassoul','hicham@gmail.com',0,1,'2026-04-24 21:27:46.847925');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` (`id`, `name`) VALUES (3,'ADMIN'),(2,'MEMBER');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES (2,8,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-08  0:15:24