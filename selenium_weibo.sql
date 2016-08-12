/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : selenium_weibo

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2016-08-13 00:38:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `fans_cot` int(11) NOT NULL,
  `follow_cot` int(11) NOT NULL,
  `weibo_cot` int(11) NOT NULL,
  `area` varchar(255) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `sex` tinyint(4) DEFAULT NULL,
  `abstract_info` varchar(255) DEFAULT NULL,
  `is_auth` tinyint(4) DEFAULT NULL,
  `is_vip` tinyint(4) DEFAULT '0',
  `company` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for weibo
-- ----------------------------
DROP TABLE IF EXISTS `weibo`;
CREATE TABLE `weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weibo_id` varchar(255) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `user` int(11) NOT NULL,
  `submit_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  `like_cot` int(11) NOT NULL DEFAULT '0',
  `via_cot` int(11) NOT NULL,
  `comment_cot` int(11) NOT NULL DEFAULT '0',
  `source` varchar(255) DEFAULT NULL,
  `is_top` tinyint(4) DEFAULT '0',
  `via_weibo_id` varchar(255) DEFAULT NULL,
  `is_via` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `weibo_id` (`weibo_id`),
  KEY `user` (`user`),
  CONSTRAINT `user` FOREIGN KEY (`user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=211 DEFAULT CHARSET=utf8;
