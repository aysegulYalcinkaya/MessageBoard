DROP TABLE IF EXISTS `tb_mail`;
CREATE TABLE IF NOT EXISTS `tb_mail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `mail_content` varchar(2000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE IF NOT EXISTS `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `trigger_table`;
CREATE TABLE IF NOT EXISTS `trigger_table` (
  `new_mail` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

ALTER TABLE `tb_mail`
  ADD CONSTRAINT `tb_mail_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`id`);
COMMIT;

DROP TRIGGER IF EXISTS `new_mail_trigger`;
DELIMITER $$
CREATE TRIGGER `new_mail_trigger` AFTER INSERT ON `tb_mail` FOR EACH ROW begin
           INSERT INTO trigger_table
           (new_mail) VALUES(NEW.id);

END
$$
DELIMITER ;


