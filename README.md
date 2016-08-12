#SinaSeleniumSpider

## 主类为weiboClass，userClass，数据库也由二者组成。
```sql
/*
Navicat MySQL Data Transfer
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

```

- 该爬虫直接爬取weibo.com大站，大部分数据无需登陆，无需cookie。
 
- 若对数据量有要求建议爬取weibo.cn。这里仅作测试实验使用。

- Selenium作为测试自动化工具，爬虫适应性极强。对于大量js加载后的数据爬取有一定的优势。

- 在两主类基础上开发:
 1) 对用户主页的监控，关注人新发微博邮件提示
（HomePageMonitor.py + MonitorHandler.py + emailClass.py）

  2) 对于特定用户的粉丝或关注人进行提取
  
  3）对于特定用户的粉丝进行机器筛选清理
  
  4）对于粉丝机的生产
  
  5）再或者介于各种用户属性间，对于用户进行特定的识别分析，判定用户种类，喜好，加标签之类
  
  6）属于智能学习范畴的，前提是有这些数据
