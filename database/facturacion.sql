-- Crear la tabla roles
CREATE TABLE IF NOT EXISTS `roles` (
  `id` TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
);

-- Insertar los roles en la tabla roles, ignorando si ya existen
INSERT IGNORE INTO `roles` (`id`, `role_name`) VALUES
  (1, 'master'),
  (2, 'administrador'),
  (3, 'operador');

-- Crear la tabla users
CREATE TABLE IF NOT EXISTS `users` (
  `id` SMALLINT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,
  `password` CHAR(128) COLLATE utf8_unicode_ci NOT NULL,
  `fullname` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `email` VARCHAR(100) COLLATE utf8_unicode_ci NOT NULL,
  `document_type` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `identity_number` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `role_id` TINYINT(1) UNSIGNED NOT NULL DEFAULT 1,
  `status` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE SET DEFAULT
);

-- Insertar un nuevo usuario en la tabla users
-- INSERT INTO `users` (`username`, `password`, `fullname`, `email`, `document_type`, `identity_number`, `role_id`, `status`)
-- VALUES 
--   ('cris86', 'pbkdf2:sha256:260000$m89Bjh07a9PLgbyZ$4d5c4dc07051fd3c94d726d351c0f850d50800f9df5f6fabf7dd8026b4627271', 'Cris Rios', 'cris86@example.com', 'CC', '1234567890', 1, 1);