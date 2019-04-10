-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 10, 2019 at 05:16 PM
-- Server version: 5.7.25-0ubuntu0.18.04.2
-- PHP Version: 7.2.15-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ALL POS`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(20) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `telephone_no` int(8) NOT NULL,
  `email` varchar(100) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `Sex` varchar(5) NOT NULL,
  `birth` varchar(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `collecting_points` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `first_name`, `last_name`, `telephone_no`, `email`, `Address`, `Sex`, `birth`, `username`, `password`, `collecting_points`) VALUES
(1, 'chan', ' tai man', 43215346, 'vincent99v1123li@gmail.com', '2 xyz street', 'M', '11/11/1111', 'ctm', '123456', 242),
(2, 'lee', 'tai man', 85334521, 'lee@cba.com', '21 xyz street', 'M', '11/11/1111', 'lee123', '654321', 27),
(3, 'li', 'tai man', 87654321, 'a@gmail.com', '5 xyz street', 'N/A', '11/11/1111', 'li321', '12341234', 122651),
(5, 'chan', 'tai man', 88888888, 'chan123@abc.com', '7 xyz street', 'M', '11/11/1111', 'chantaiman001', '12342234', 3),
(6, 'chan', 'xiao man', 66666666, 'cxm@abc.com', '1 xyz street', 'M', '11/11/1111', 'cxm', '42345234', 3),
(7, 'Panda', 'Eric', 51105554, 'vincent99v1123li2@gmail.com', '5 xyz street', 'M', '11/11/1111', 'PandaEric', 'a1234567', 233),
(8, 'm', 'mky', 69020826, 'mmky@richclub.com', '8 xyz street', 'F', '11/11/1111', 'm.mky', '1231232242m', 87913),
(9, 'wong', 'pak', 91486878, 'wongpak@gmail.com', '45 xyz street', 'M', '11/11/1111', 'wong', 'W23424fsf', 104),
(10, 'ada', 'chan', 94569082, 'ada66chan@yahoo.com.hk', '7 xyz street', 'F', '1966-10-28', 'ada66', '123456', 0),
(25, 'Vincent', 'Li', 97218289, 'vincent23li@yahoo.com.hk', '7 xyz street', 'M', '1999-11-23', 'vin', 'a1234567', 0),
(27, 'hey', 'Li', 90000011, '6n2017liyatlong@gmail.com', '7', 'N/A', '2001-02-01', 'hey_li', 'a1234567', 4);

-- --------------------------------------------------------

--
-- Table structure for table `Delivery`
--

CREATE TABLE `Delivery` (
  `delivery_schedule` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Delivery`
--

INSERT INTO `Delivery` (`delivery_schedule`) VALUES
(2);

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `product_id` int(20) UNSIGNED NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `product_brand` varchar(20) NOT NULL,
  `product_price` float UNSIGNED NOT NULL,
  `Stock` int(10) UNSIGNED NOT NULL,
  `product_type` set('Drink','Food') NOT NULL,
  `product_subtype` set('Tea','Milk','Carbonated_drink','Drink_other','Food_other','Beer','Coffee','Cup_noodle','Juice','Bread','Ice_cream','Frozen_food','Snacks','water') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Product`
--

INSERT INTO `Product` (`product_id`, `product_name`, `product_brand`, `product_price`, `Stock`, `product_type`, `product_subtype`) VALUES
(1, 'Lemon tea 375ml 6 packs', 'Vita', 8.8, 900, 'Drink', 'Tea'),
(2, 'Coca-cola Peach 500ml', 'Coca-cola', 8.8, 0, 'Drink', 'Carbonated_drink'),
(3, 'Coca-cola Japan Ver. 250ml', 'Coca-cola', 7.5, 3, 'Drink', 'Carbonated_drink'),
(4, 'Mineral Water 1.5L', 'Volvic', 30, 24, 'Drink', 'water'),
(5, 'Inst Coffee Drink 250ml 6packs', 'Nescafe', 31, 0, 'Drink', 'Coffee'),
(6, 'Mango Juice Drink 250m', 'Hi-c', 4.7, 3, 'Drink', 'Juice'),
(7, 'Apple Juice Drink 250ml', 'Hi-c', 4.7, 13, 'Drink', 'Juice'),
(8, 'Mineralized Water 500ml', 'Bonaqua', 4.4, 8, 'Drink', 'water'),
(9, 'Supreme Oolong Tea 500ml', 'Tao Ti', 7.9, 1, 'Drink', 'Tea'),
(10, 'Cream Soda 330ml', 'Schweppes', 8.8, 5, 'Drink', 'Carbonated_drink'),
(11, 'Guava Drink 250ml', 'Vita', 6.9, 5, 'Drink', 'Juice'),
(12, 'Orange Juice Drink 1.2L', 'Minute Maid', 13.9, 0, 'Drink', 'Juice'),
(13, 'Melon Soya Milk 250ml', 'Hi-c', 7.5, 20, 'Drink', 'Milk'),
(14, 'Water 750ml', 'Cool', 4.2, 3, 'Drink', 'water'),
(15, 'Apple Green Tea 250ml 6 packs', 'Vita', 8.8, 992, 'Drink', 'Tea'),
(17, 'Large Bottle Draftbeer 600ml', 'Yanjing', 8.9, 4, 'Drink', 'Beer'),
(18, 'Draught 500ml', 'Boddingtons', 19.9, 3, 'Drink', 'Beer'),
(19, 'Whole Wheat Toast Bread 8 Slices', 'Baker\'s Choice', 9.9, 0, 'Food', 'Bread'),
(20, 'Life Bread 14 Slices', 'Garden', 11.1, 13, 'Food', 'Bread'),
(21, 'Life Bread - Wheat 14 Slices', 'Garden', 12.6, 7, 'Food', 'Bread'),
(22, 'Seafood Cup Noodle 75gm', 'Nissin', 6.5, 5, 'Food', 'Cup_noodle'),
(23, 'Sesame Oil Cup Noodle 72gm', 'Nissin', 7.3, 9, 'Food', 'Cup_noodle'),
(24, 'Beef Bowl Noodle 188gm', 'Imperialb.meal', 16.9, 195, 'Food', 'Cup_noodle'),
(25, 'new Belgian Chocolate Ice Cream', 'Haagen-dazs', 30.7, 11, 'Food', 'Ice_cream'),
(26, 'Cookies & Cream Ice Cream', 'Haagen-dazs', 33.4, 16, 'Food', 'Ice_cream'),
(27, 'Drumstick Vanilla Mp', 'Nestle', 23.4, 0, 'Food', 'Ice_cream'),
(28, 'Cookies & Cream Ice Cream', 'Haagen-dazs', 30.4, 2, 'Food', 'Ice_cream'),
(29, 'Strawberry Ice Cream', 'Haagen-dazs', 33.4, 17, 'Food', 'Ice_cream'),
(30, 'Drumstick Chocolate Mp', 'Nestle', 23.4, 10, 'Food', 'Ice_cream'),
(31, 'Mini Passions', 'Haagen-dazs', 34.5, 12, 'Food', 'Ice_cream'),
(32, 'Deluxe Collection', 'Haagen-dazs', 35.6, 3, 'Food', 'Ice_cream'),
(33, 'Deluxe Shrimp Wonton', 'Wanchai Ferry', 21.9, 5, 'Food', 'Frozen_food'),
(34, 'Sesame Tongyuen', 'Wanchai Ferry', 7, 5, 'Food', 'Frozen_food'),
(35, 'Breaded Chicken Breast Chunks 300g', 'Waitrose', 55.9, 5, 'Food', 'Frozen_food'),
(36, '4 Finger Chocolate', 'Kit Kat', 11.5, 8, 'Food', 'Snacks'),
(37, 'Almond Chocolate', 'Meiji', 18.9, 3, 'Food', 'Snacks'),
(38, 'Demae Iccho - Spicy Beef Flavour Instant Noodle ', 'Nissin', 10, 494, 'Food', 'Cup_noodle'),
(39, 'new noodle', 'new', 13, 200, 'Food', 'Cup_noodle'),
(42, 'r43rt', '34t3t', 4, 4, 'Drink', 'Tea'),
(43, 'rewrew', 'werwr', 3, 3, 'Drink', 'Tea'),
(44, 'testtest', 'tes', 4, 4, 'Food', 'Bread');

-- --------------------------------------------------------

--
-- Table structure for table `Shopping_cart`
--

CREATE TABLE `Shopping_cart` (
  `customer_id` int(20) NOT NULL,
  `product_id` int(20) UNSIGNED NOT NULL,
  `shopping_cart_id` int(50) NOT NULL,
  `quantity` int(10) NOT NULL,
  `total_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Shopping_cart`
--

INSERT INTO `Shopping_cart` (`customer_id`, `product_id`, `shopping_cart_id`, `quantity`, `total_price`) VALUES
(10, 1, 4, 1, 8.8),
(10, 1, 5, 1, 8.8);

-- --------------------------------------------------------

--
-- Table structure for table `Shopping_record`
--

CREATE TABLE `Shopping_record` (
  `customer_id` int(20) NOT NULL,
  `product_id` int(20) UNSIGNED NOT NULL,
  `Shopping_record_id` int(50) NOT NULL,
  `quantity` int(10) NOT NULL,
  `total_price` float NOT NULL,
  `date_purchase` varchar(10) NOT NULL,
  `time_purchase` varchar(15) NOT NULL,
  `delivery_date` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Shopping_record`
--

INSERT INTO `Shopping_record` (`customer_id`, `product_id`, `Shopping_record_id`, `quantity`, `total_price`, `date_purchase`, `time_purchase`, `delivery_date`) VALUES
(7, 3, 22, 3, 36, '2019-04-01', '14:34:30.818310', '2019-04-02'),
(7, 1, 23, 10, 88, '2019-04-01', '14:34:30.818310', '2019-04-02'),
(7, 5, 24, 1, 7.5, '2019-04-01', '14:34:30.818310', '2019-04-02'),
(7, 8, 25, 2, 8.8, '2019-04-01', '14:34:30.818310', '2019-04-02'),
(7, 1, 26, 9, 79.2, '2019-04-01', '14:38:31.411687', '2019-04-02'),
(7, 2, 27, 8, 70.4, '2019-04-01', '14:38:31.411687', '2019-04-02'),
(7, 4, 28, 2, 60, '2019-04-01', '14:38:31.411687', '2019-04-02'),
(7, 18, 29, 2, 39.8, '2019-04-01', '19:22:32.589433', '2019-04-02'),
(7, 2, 30, 1, 8.8, '2019-04-01', '19:36:16.509324', '2019-04-02'),
(7, 4, 31, 1, 30, '2019-04-01', '19:38:12.894379', '2019-04-02'),
(7, 3, 32, 1, 12, '2019-04-01', '21:04:12.842713', '2019-04-02'),
(7, 1, 33, 1, 8.8, '2019-04-01', '21:04:58.922366', '2019-04-02'),
(7, 1, 34, 1, 8.8, '2019-04-01', '21:06:10.208337', '2019-04-02'),
(7, 1, 35, 1, 8.8, '2019-04-01', '21:06:54.942997', '2019-04-02'),
(7, 1, 36, 1, 8.8, '2019-04-01', '21:07:58.420975', '2019-04-02'),
(7, 1, 37, 1, 8.8, '2019-04-01', '21:09:52.361043', '2019-04-02'),
(7, 1, 38, 2, 17.6, '2019-04-01', '21:11:44.408697', '2019-04-02'),
(7, 1, 39, 2, 17.6, '2019-04-01', '21:14:44.469570', '2019-04-02'),
(7, 2, 40, 1, 8.8, '2019-04-01', '21:14:44.469570', '2019-04-02'),
(7, 1, 41, 2, 17.6, '2019-04-01', '21:16:51.795238', '2019-04-02'),
(7, 3, 42, 1, 12, '2019-04-01', '21:16:51.795238', '2019-04-02'),
(7, 6, 43, 1, 4.7, '2019-04-01', '21:16:51.795238', '2019-04-02'),
(7, 1, 44, 2, 17.6, '2019-04-01', '21:19:03.435006', '2019-04-02'),
(7, 1, 45, 1, 8.8, '2019-04-01', '21:20:37.223679', '2019-04-02'),
(7, 1, 46, 2, 17.6, '2019-04-01', '21:26:58.946201', '2019-04-02'),
(7, 15, 47, 4, 35.2, '2019-04-01', '21:26:58.946201', '2019-04-02'),
(10, 15, 48, 2, 17.6, '2019-04-01', '21:32:12.427673', '2019-04-02'),
(10, 15, 49, 2, 17.6, '2019-04-01', '21:33:24.111774', '2019-04-02'),
(10, 1, 50, 3, 26.4, '2019-04-01', '22:22:11.592617', '2019-04-02'),
(10, 20, 51, 2, 22.2, '2019-04-01', '22:22:11.592617', '2019-04-02'),
(7, 1, 52, 2, 17.6, '2019-04-01', '22:37:21.432378', '2019-04-02'),
(7, 3, 53, 1, 12, '2019-04-01', '22:37:21.432378', '2019-04-02'),
(7, 4, 54, 1, 30, '2019-04-01', '22:37:21.432378', '2019-04-02'),
(7, 6, 55, 2, 9.4, '2019-04-01', '22:37:21.432378', '2019-04-02'),
(7, 1, 56, 3, 26.4, '2019-04-01', '23:03:02.248444', '2019-04-02'),
(7, 1, 57, 1, 8.8, '2019-04-01', '23:03:32.809942', '2019-04-02'),
(7, 1, 58, 7, 61.6, '2019-04-01', '23:04:53.172597', '2019-04-02'),
(7, 2, 59, 1, 8.8, '2019-04-01', '23:04:53.172597', '2019-04-02'),
(7, 19, 60, 1, 9.9, '2019-04-01', '23:04:53.172597', '2019-04-02'),
(7, 25, 61, 2, 60.8, '2019-04-01', '23:04:53.172597', '2019-04-02'),
(1, 12, 62, 8, 111.2, '2019-04-01', '23:12:34.027903', '2019-04-02'),
(1, 6, 63, 3, 14.1, '2019-04-01', '23:12:34.027903', '2019-04-02'),
(1, 20, 64, 2, 22.2, '2019-04-01', '23:12:34.027903', '2019-04-02'),
(1, 23, 65, 1, 7.3, '2019-04-01', '23:12:34.027903', '2019-04-02'),
(1, 29, 66, 3, 100.2, '2019-04-01', '23:12:34.027903', '2019-04-02'),
(1, 4, 67, 8, 240, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 6, 68, 2, 9.4, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 7, 69, 1, 4.7, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 19, 70, 1, 9.9, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 24, 71, 2, 29.8, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 26, 72, 4, 133.6, '2019-04-01', '23:15:18.592472', '2019-04-02'),
(1, 13, 73, 2, 15, '2019-04-02', '00:00:53.728005', '2019-04-03'),
(1, 25, 74, 1, 30.4, '2019-04-02', '00:00:53.728005', '2019-04-03'),
(1, 38, 75, 3, 30, '2019-04-02', '01:49:09.580425', '2019-04-03'),
(7, 3, 76, 1, 12, '2019-04-02', '14:39:11.864383', '2019-04-03'),
(7, 1, 77, 1, 8.8, '2019-04-02', '14:40:08.602542', '2019-04-03'),
(7, 1, 78, 1, 8.8, '2019-04-02', '15:44:59.640004', '2019-04-03'),
(7, 1, 79, 1, 8.8, '2019-04-02', '15:46:26.845630', '2019-04-03'),
(7, 1, 80, 3, 26.4, '2019-04-02', '23:43:10.024214', '2019-04-03'),
(7, 1, 81, 1, 8.8, '2019-04-03', '00:42:02.935934', '2019-04-04'),
(7, 34, 82, 1, 7, '2019-04-03', '16:10:14.676351', '2019-04-04'),
(7, 37, 83, 1, 18.9, '2019-04-03', '16:10:14.676351', '2019-04-04'),
(7, 1, 84, 1, 8.8, '2019-04-03', '16:41:18.904745', '2019-04-04'),
(7, 3, 85, 1, 7.5, '2019-04-03', '18:13:30.313811', '2019-04-04'),
(7, 1, 86, 2, 17.6, '2019-04-03', '18:13:30.313811', '2019-04-04'),
(7, 19, 87, 1, 9.9, '2019-04-04', '01:46:24.527125', '2019-04-05'),
(7, 20, 88, 1, 11.1, '2019-04-04', '01:46:24.527125', '2019-04-05'),
(7, 1, 89, 1, 8.8, '2019-04-04', '14:10:08.867599', '2019-04-04'),
(27, 20, 91, 3, 33.3, '2019-04-04', '17:45:31.609159', '2019-04-05'),
(27, 1, 92, 1, 8.8, '2019-04-04', '20:36:40.005066', '2019-04-06'),
(7, 20, 93, 1, 11.1, '2019-04-07', '21:45:45.837747', '2019-04-09'),
(1, 1, 94, 1, 8.8, '2019-04-10', '00:38:39.709747', '2019-04-11'),
(1, 20, 95, 3, 33.3, '2019-04-10', '00:38:39.709747', '2019-04-11'),
(1, 1, 96, 1, 8.8, '2019-04-10', '00:38:39.709747', '2019-04-11'),
(1, 1, 97, 1, 8.8, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 3, 98, 1, 7.5, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 13, 99, 1, 7.5, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 2, 100, 1, 8.8, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 1, 101, 1, 8.8, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 22, 102, 1, 6.5, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 25, 103, 1, 30.7, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 25, 104, 1, 30.7, '2019-04-10', '12:52:23.795262', '2019-04-11'),
(1, 1, 105, 1, 8.8, '2019-04-10', '14:22:17.734356', '2019-04-11'),
(1, 1, 106, 1, 8.8, '2019-04-10', '17:12:04.306258', '2019-04-11'),
(1, 1, 107, 1, 8.8, '2019-04-10', '17:12:04.306258', '2019-04-11'),
(1, 19, 108, 1, 9.9, '2019-04-10', '17:12:04.306258', '2019-04-11'),
(1, 22, 109, 1, 6.5, '2019-04-10', '17:12:04.306258', '2019-04-11'),
(1, 38, 110, 3, 30, '2019-04-10', '17:12:04.306258', '2019-04-11');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staff_id` int(10) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `telephone_no` int(8) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_of_birth` varchar(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staff_id`, `first_name`, `last_name`, `telephone_no`, `email`, `date_of_birth`, `username`, `password`) VALUES
(1, 'chan', 'tai man', 12345678, 'ctm@xxxmail.com', '1999-01-01', 'ctm', '123456'),
(2, 'chan', 'xiao man', 12341234, 'cxm@xxxmail.com', '1999-01-01', 'cxm', '654321'),
(3, 'lee', 'tai man', 43214321, 'ltm@xxxmail.com', '2000-11-11', 'ltm', '42310'),
(4, 'lee', 'xiao man', 43211234, 'lxm@xxxmail.com', '2000-11-11', 'lxm', '42310');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_id` (`customer_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `telephone_no` (`telephone_no`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `product_id` (`product_id`);

--
-- Indexes for table `Shopping_cart`
--
ALTER TABLE `Shopping_cart`
  ADD PRIMARY KEY (`shopping_cart_id`),
  ADD UNIQUE KEY `shopping_cart id` (`shopping_cart_id`),
  ADD KEY `Shopping_cart_ibfk_1` (`customer_id`),
  ADD KEY `Shopping_cart_ibfk_2` (`product_id`);

--
-- Indexes for table `Shopping_record`
--
ALTER TABLE `Shopping_record`
  ADD PRIMARY KEY (`Shopping_record_id`),
  ADD UNIQUE KEY `customer_id` (`customer_id`,`product_id`,`Shopping_record_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staff_id`),
  ADD UNIQUE KEY `staff_id` (`staff_id`,`telephone_no`,`email`,`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT for table `Product`
--
ALTER TABLE `Product`
  MODIFY `product_id` int(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;
--
-- AUTO_INCREMENT for table `Shopping_cart`
--
ALTER TABLE `Shopping_cart`
  MODIFY `shopping_cart_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `Shopping_record`
--
ALTER TABLE `Shopping_record`
  MODIFY `Shopping_record_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=111;
--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `staff_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `Shopping_cart`
--
ALTER TABLE `Shopping_cart`
  ADD CONSTRAINT `Shopping_cart_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  ADD CONSTRAINT `Shopping_cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`);

--
-- Constraints for table `Shopping_record`
--
ALTER TABLE `Shopping_record`
  ADD CONSTRAINT `Shopping_record_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  ADD CONSTRAINT `Shopping_record_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `Product` (`product_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
