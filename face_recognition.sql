-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- 主機: 127.0.0.1:3306
-- 產生時間： 2019 年 04 月 08 日 11:45
-- 伺服器版本: 5.7.19
-- PHP 版本： 7.0.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `face_recognition`
--

-- --------------------------------------------------------

--
-- 資料表結構 `app01_attendance_record`
--

DROP TABLE IF EXISTS `app01_attendance_record`;
CREATE TABLE IF NOT EXISTS `app01_attendance_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `today_date` date NOT NULL,
  `arrive_time` time(6) NOT NULL,
  `is_late` tinyint(1) NOT NULL,
  `is_abs` tinyint(1) NOT NULL,
  `c_to_m_id_id` int(11) NOT NULL,
  `s_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_attendance_record_c_to_m_id_id_82312bc0` (`c_to_m_id_id`),
  KEY `app01_attendance_record_s_id_id_2897333f` (`s_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `app01_attendance_record`
--

INSERT INTO `app01_attendance_record` (`id`, `today_date`, `arrive_time`, `is_late`, `is_abs`, `c_to_m_id_id`, `s_id_id`) VALUES
(1, '2019-03-15', '02:00:00.000000', 0, 1, 1, 1),
(2, '2019-03-15', '16:00:00.000000', 0, 0, 1, 2),
(3, '2019-03-15', '16:00:00.000000', 1, 0, 1, 3),
(4, '2019-03-15', '16:54:00.000000', 0, 0, 1, 4),
(5, '2019-03-15', '16:00:00.000000', 0, 0, 1, 5);

-- --------------------------------------------------------

--
-- 資料表結構 `app01_course`
--

DROP TABLE IF EXISTS `app01_course`;
CREATE TABLE IF NOT EXISTS `app01_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `app01_course`
--

INSERT INTO `app01_course` (`id`, `c_id`, `name`) VALUES
(1, '252436', 'BSc (Hons) Computing');

-- --------------------------------------------------------

--
-- 資料表結構 `app01_course_to_module`
--

DROP TABLE IF EXISTS `app01_course_to_module`;
CREATE TABLE IF NOT EXISTS `app01_course_to_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `weekday` int(10) UNSIGNED NOT NULL,
  `class_room` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `c_id_id` int(11) NOT NULL,
  `m_id_id` int(11) NOT NULL,
  `s_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_course_to_module_c_id_id_b9016d2d` (`c_id_id`),
  KEY `app01_course_to_module_m_id_id_e9a82e90` (`m_id_id`),
  KEY `app01_course_to_module_s_id_id_1c221a4c` (`s_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `app01_course_to_module`
--

INSERT INTO `app01_course_to_module` (`id`, `start_date`, `end_date`, `start_time`, `end_time`, `weekday`, `class_room`, `c_id_id`, `m_id_id`, `s_id_id`) VALUES
(1, '2019-01-15', '2019-04-08', '16:59:00.000000', '20:49:00.000000', 5, 'Rm404', 1, 6, 11),
(2, '2019-01-16', '2019-04-16', '16:00:00.000000', '23:00:00.000000', 3, 'LT118B', 1, 5, 11),
(3, '2019-02-01', '2019-04-06', '08:00:00.000000', '10:00:00.000000', 2, '427B', 1, 5, 11);

-- --------------------------------------------------------

--
-- 資料表結構 `app01_module`
--

DROP TABLE IF EXISTS `app01_module`;
CREATE TABLE IF NOT EXISTS `app01_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `m_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `app01_module`
--

INSERT INTO `app01_module` (`id`, `m_id`, `name`) VALUES
(1, '210CT', 'Programming, Algorithms and Data Structures'),
(2, '303COM', 'Individual Project'),
(3, '302CEM', 'Agile Development'),
(4, '304CEM', 'Web API Development'),
(5, '300CEM', 'Android Applications Development'),
(6, '310CT', 'Intelligent Agents'),
(7, 'A300CAW', 'Academic Writing 3: Writing Skills for Dissert');

-- --------------------------------------------------------

--
-- 資料表結構 `app01_user`
--

DROP TABLE IF EXISTS `app01_user`;
CREATE TABLE IF NOT EXISTS `app01_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `role` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `c_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app01_user_c_id_id_25ed8a0f` (`c_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `app01_user`
--

INSERT INTO `app01_user` (`id`, `s_id`, `name`, `password`, `role`, `c_id_id`) VALUES
(1, '187106298', 'wong wing hei', 'e10adc3949ba59abbe56e057f20f883e', 'student', 1),
(2, '187106299', 'john ', 'e10adc3949ba59abbe56e057f20f883e', 'student', 1),
(3, '187106297', 'jack', 'e10adc3949ba59abbe56e057f20f883e', 'student', 1),
(4, '187106296', 'peter', 'e10adc3949ba59abbe56e057f20f883e', 'student', 1),
(5, '187106295', 'alan', 'e10adc3949ba59abbe56e057f20f883e', 'student', 1),
(11, '187106294', 'mr.wong', 'e10adc3949ba59abbe56e057f20f883e', 'teacher', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add attendance_ record', 7, 'add_attendance_record'),
(20, 'Can change attendance_ record', 7, 'change_attendance_record'),
(21, 'Can delete attendance_ record', 7, 'delete_attendance_record'),
(22, 'Can add course', 8, 'add_course'),
(23, 'Can change course', 8, 'change_course'),
(24, 'Can delete course', 8, 'delete_course'),
(25, 'Can add course_to_ module', 9, 'add_course_to_module'),
(26, 'Can change course_to_ module', 9, 'change_course_to_module'),
(27, 'Can delete course_to_ module', 9, 'delete_course_to_module'),
(28, 'Can add module', 10, 'add_module'),
(29, 'Can change module', 10, 'change_module'),
(30, 'Can delete module', 10, 'delete_module'),
(31, 'Can add user', 11, 'add_user'),
(32, 'Can change user', 11, 'change_user'),
(33, 'Can delete user', 11, 'delete_user');

-- --------------------------------------------------------

--
-- 資料表結構 `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'app01', 'attendance_record'),
(8, 'app01', 'course'),
(9, 'app01', 'course_to_module'),
(10, 'app01', 'module'),
(11, 'app01', 'user');

-- --------------------------------------------------------

--
-- 資料表結構 `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2019-03-14 10:43:24.684912'),
(2, 'auth', '0001_initial', '2019-03-14 10:43:25.050789'),
(3, 'admin', '0001_initial', '2019-03-14 10:43:25.144673'),
(4, 'admin', '0002_logentry_remove_auto_add', '2019-03-14 10:43:25.153668'),
(5, 'app01', '0001_initial', '2019-03-14 10:43:25.518965'),
(6, 'contenttypes', '0002_remove_content_type_name', '2019-03-14 10:43:25.573345'),
(7, 'auth', '0002_alter_permission_name_max_length', '2019-03-14 10:43:25.599331'),
(8, 'auth', '0003_alter_user_email_max_length', '2019-03-14 10:43:25.627315'),
(9, 'auth', '0004_alter_user_username_opts', '2019-03-14 10:43:25.639324'),
(10, 'auth', '0005_alter_user_last_login_null', '2019-03-14 10:43:25.669290'),
(11, 'auth', '0006_require_contenttypes_0002', '2019-03-14 10:43:25.673303'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2019-03-14 10:43:25.683299'),
(13, 'auth', '0008_alter_user_username_max_length', '2019-03-14 10:43:25.711283'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2019-03-14 10:43:25.738264'),
(15, 'sessions', '0001_initial', '2019-03-14 10:43:25.771241');

-- --------------------------------------------------------

--
-- 資料表結構 `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 資料表的匯出資料 `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('jug3nahqu7v3v3exj9ljlj9056gq000g', 'MThmYWU0M2NjMzYwYWNiMWUyMTRjOGQyM2YzZDE0ZjVkYjljNTJiZTp7InNfaWQiOiIxODcxMDYyOTgiLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-16 15:28:34.380391'),
('d826s45hemqzekui0egrum465xna0ypt', 'MThmYWU0M2NjMzYwYWNiMWUyMTRjOGQyM2YzZDE0ZjVkYjljNTJiZTp7InNfaWQiOiIxODcxMDYyOTgiLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-16 15:30:30.558219'),
('ipr1ms7sgdlszlhggflxvwvs9892kp7j', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-20 17:56:07.812119'),
('3rnyi0h6mdve5ezsrtuy6eoikpx0uroq', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-17 16:39:15.196306'),
('9pxyw2mg7vrbjc44djlogoamxlspccy1', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-18 10:57:46.739887'),
('8cj0ygpoo91zctsyk0b2a8jbaw1n54vu', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-18 19:15:18.107518'),
('qpkc68z0zlei6fu7mm7yi3x7ctjaq7q4', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-19 04:37:34.497691'),
('iera4yk0sk7ayyy37bxrkbtpnvsqyosq', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-19 05:22:51.250634'),
('4k80a8ud19ih0laf3lb8cvi8wxhhunju', 'Y2FmOTRiMWQ3MDIyZTUxYjZjZTU1MzFlMjZiZDhiY2I4MDYxZDMxNDp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExfQ==', '2019-04-20 11:17:52.063018'),
('0d95bx1mg5b2vbyxll8kef532oazcw20', 'MWQyNTc3ZjE1MGE2NDc0Zjg5NTE2YjE2ZjMxMjNlNmM3ZTUwZWFkMTp7InNfaWQiOiIxODcxMDYyOTQiLCJuYW1lIjoibXIud29uZyIsInJvbGUiOiJ0ZWFjaGVyIiwiY19pZF9pZCI6MSwiaWQiOjExLCJfc2Vzc2lvbl9leHBpcnkiOjB9', '2019-04-20 17:53:11.261281');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
