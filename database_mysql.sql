CREATE TABLE `Telewizor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `przekatna_(cal)` INT NOT NULL,
    `typ_wyswietlacza` VARCHAR(255) NOT NULL,
    `rozdzielczosc_(xK)` BIGINT NOT NULL,
    `smart_TV` BOOLEAN NOT NULL
);
CREATE TABLE `Komputer`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `procesor` BIGINT UNSIGNED NOT NULL,
    `pamiec_RAM` BIGINT UNSIGNED UNSIGNED NOT NULL,
    `pojemnosc_dysku` INT NOT NULL
);
CREATE TABLE `Monitor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `przekatna_(czal)` INT NOT NULL,
    `odswiezanie_(Hz)` INT NOT NULL,
    `rozdzielczość` BIGINT NOT NULL,
    `typ_wyswietlacza` BIGINT NOT NULL,
    `glosniki_` BOOLEAN NOT NULL,
    `proporcje_ekranu` VARCHAR(255) NOT NULL
);
CREATE TABLE `Historia_cen`(
    `id` BIGINT UNSIGNED NOT NULL,
    `id_sklepu_z_danym_produktem` BIGINT UNSIGNED NOT NULL,
    `cena` DECIMAL(8, 2) NOT NULL,
    `data` DATE NOT NULL,
    PRIMARY KEY(`id`)
);
CREATE TABLE `Procesor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `liczba_rdzeni` BIGINT NOT NULL,
    `taktowanie` BIGINT NOT NULL,
    `rodzaj_gniazda` VARCHAR(255) NOT NULL
);
CREATE TABLE `RAM`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `typ_pamieci` VARCHAR(255) NOT NULL,
    `pojemnosc_(GB)` INT NOT NULL,
    `taktowanie_(MHz)` BIGINT NOT NULL
);
CREATE TABLE `Lista_produktow`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `kategoria` BIGINT NOT NULL,
    `marka` VARCHAR(255) NOT NULL,
    `model` BIGINT NOT NULL
);
CREATE TABLE `Lista_sklepow`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_produktu` BIGINT UNSIGNED NOT NULL,
    `nazwa` BIGINT NOT NULL
);
CREATE TABLE `Lista_opinii`(
    `id` BIGINT UNSIGNED NOT NULL,
    `id_produktu` BIGINT UNSIGNED UNSIGNED NOT NULL,
    `opinia` VARCHAR(255) NOT NULL,
    `data` DATETIME NOT NULL,
    PRIMARY KEY(`id`)
);
ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_id_foreign` FOREIGN KEY(`id`) REFERENCES `Lista_produktow`(`id`);
ALTER TABLE
    `Monitor` ADD CONSTRAINT `monitor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Lista_produktow`(`id`);
ALTER TABLE
    `Telewizor` ADD CONSTRAINT `telewizor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Lista_produktow`(`id`);
ALTER TABLE
    `Procesor` ADD CONSTRAINT `procesor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Lista_produktow`(`id`);
ALTER TABLE
    `RAM` ADD CONSTRAINT `ram_id_foreign` FOREIGN KEY(`id`) REFERENCES `Lista_produktow`(`id`);


ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_pamiec_ram_foreign` FOREIGN KEY(`pamiec_RAM`) REFERENCES `RAM`(`id`);
ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_procesor_foreign` FOREIGN KEY(`procesor`) REFERENCES `Procesor`(`id`);

ALTER TABLE
    `Historia_cen` ADD CONSTRAINT `historia_cen_id_sklepu_z_danym_produktem_foreign` FOREIGN KEY(`id_sklepu_z_danym_produktem`) REFERENCES `Lista_sklepow`(`id`);
ALTER TABLE
    `Lista_opinii` ADD CONSTRAINT `lista_opinii_id_produktu_foreign` FOREIGN KEY(`id_produktu`) REFERENCES `Lista_produktow`(`id`);
ALTER TABLE
    `Lista_sklepow` ADD CONSTRAINT `lista_sklepow_id_produktu_foreign` FOREIGN KEY(`id_produktu`) REFERENCES `Lista_produktow`(`id`);
