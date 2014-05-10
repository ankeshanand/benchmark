CREATE DATABASE benchmark_db;

USE benchmark_db;

CREATE TABLE benchmark_logs (
	`id` INT auto_increment,
	`machine_desc` VARCHAR(255),
	`brlcad_version` VARCHAR(15),
	`running_time` INT(10),
   	`time_of_execution` TIMESTAMP,
   	`approx_vgr` FLOAT(10,5),
   	`log_vgr` FLOAT(10,5),
   	`params` VARCHAR(255),
   	`results` VARCHAR(255),
   	`compiler_flags` TEXT,
   	`complete_info` TEXT,
   	PRIMARY KEY(id)
);


CREATE TABLE md5_log(
	`benchmark_id` INT,
	`file_name` VARCHAR(255),
	`md5sum` VARCHAR(100),
	`archived` ENUM('YES', 'NO'),
	`db_entries` ENUM('YES', 'NO'),
	KEY(`md5sum`),
	KEY(`benchmark_id`),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE
);


CREATE TABLE machine_info(
	`benchmark_id` INT,
	`osrelease` VARCHAR(100),
	`cpu_mhz` FLOAT,
	`hostname` VARCHAR(100),
	`cores` INT(10),
	`processors` INT(10),
	`physical_addr_size` INT(5),
	`virtual_addr_size` INT(5),
	`vendor_id` VARCHAR(100),
	`ostype` VARCHAR(100),
	KEY(`hostname`),
	KEY(`cores`),
	KEY(`ostype`),
	KEY(`processors`),
	KEY(`vendor_id`),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE
);	

CREATE TABLE email_logs(
	`id` INT auto_increment,
	`imap_id` INT(10),
	`md5` VARCHAR(100),
	`time` TIMESTAMP,
	PRIMARY KEY(`id`),
	KEY(`id`),
	KEY(`md5`)
);

CREATE TABLE `email_verification_logs`(
	`id` INT auto_increment,
	`verified_till` INT(10),
	`time` TIMESTAMP,
	PRIMARY KEY(`id`),
	KEY(`verified_till`),
	KEY(`time`)
);

CREATE TABLE `rt_moss` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);

CREATE TABLE `rt_world` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);

CREATE TABLE `rt_star` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);

CREATE TABLE `rt_bldg391` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);

CREATE TABLE `rt_m35` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);

CREATE TABLE `rt_sphflake` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);


CREATE TABLE `rt_average` (
	`benchmark_id` INT,
	`abs_rps` FLOAT,
	`vgr_rps` FLOAT,
	`result` ENUM('RIGHT', 'WRONG', 'COMPARISION_FAILURE'),
	FOREIGN KEY(benchmark_id) REFERENCES benchmark_logs(id) ON UPDATE CASCADE,
	KEY(`result`)
);


