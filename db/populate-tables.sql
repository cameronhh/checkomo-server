BEGIN TRANSACTION;

DROP TABLE IF EXISTS VENUE CASCADE;

DROP TABLE IF EXISTS VENUE_CODE_TEMPLATE CASCADE;

DROP TABLE IF EXISTS VENUE_CODE CASCADE;

DROP TABLE IF EXISTS VISIT CASCADE;

DROP TABLE IF EXISTS "user" CASCADE;

DROP TABLE IF EXISTS VENUE_USER CASCADE;

DROP TABLE IF EXISTS SETTINGS CASCADE;

CREATE TABLE venue (
        id SERIAL NOT NULL, 
        name VARCHAR(256) NOT NULL, 
        address VARCHAR(800), 
        timezone VARCHAR(64) NOT NULL, 
        PRIMARY KEY (id)
);

CREATE TABLE venue_code_template (
        id SERIAL NOT NULL, 
        PRIMARY KEY (id)
);

CREATE TABLE "user" (
        id SERIAL NOT NULL, 
        contact_number VARCHAR(30), 
        email VARCHAR(80) NOT NULL, 
        password VARCHAR(200) NOT NULL, 
        token_register VARCHAR(128), 
        token_password_reset VARCHAR(128), 
        PRIMARY KEY (id), 
        UNIQUE (email)
);

CREATE TABLE settings (
        setting_key VARCHAR(30) NOT NULL, 
        setting_value VARCHAR(2048), 
        PRIMARY KEY (setting_key)
);

CREATE TABLE venue_code (
        id VARCHAR(64) NOT NULL, 
        venue_id INTEGER NOT NULL, 
        venue_code_template_id INTEGER, 
        code VARCHAR(64) NOT NULL, 
        name VARCHAR(64), 
        sys_name VARCHAR(64), 
        start_dttm TIMESTAMP WITHOUT TIME ZONE, 
        end_dttm TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (id), 
        FOREIGN KEY(venue_id) REFERENCES venue (id), 
        FOREIGN KEY(venue_code_template_id) REFERENCES venue_code_template (id)
);

CREATE TABLE venue_user (
        venue_id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        is_admin BOOLEAN, 
        PRIMARY KEY (venue_id, user_id), 
        FOREIGN KEY(venue_id) REFERENCES venue (id), 
        FOREIGN KEY(user_id) REFERENCES "user" (id)
);

CREATE TABLE visit (
        clustered_id SERIAL NOT NULL, 
        id VARCHAR(64) NOT NULL, 
        in_dttm TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        out_dttm TIMESTAMP WITHOUT TIME ZONE, 
        approved_in BOOLEAN, 
        approved_out BOOLEAN, 
        venue_code_id VARCHAR(64), 
        venue_id INTEGER, 
        given_name VARCHAR(60) NOT NULL, 
        surname VARCHAR(60) NOT NULL, 
        phone VARCHAR(30) NOT NULL, 
        email VARCHAR(80) NOT NULL, 
        address VARCHAR(200) NOT NULL, 
        meta_info VARCHAR(1024), 
        PRIMARY KEY (clustered_id), 
        FOREIGN KEY(venue_code_id) REFERENCES venue_code (id), 
        FOREIGN KEY(venue_id) REFERENCES venue (id)
);

-- Inserts default user into the DB with username 'demo' and password 'password'
INSERT INTO "user" (email, PASSWORD)
  VALUES ('demo', '$2y$10$.qT8isdX5ljv7HKCPh2r2.b6Bcs4s5COSYGuvqf2xKFEYaOh4Qd7q');

-- Create default venue
INSERT INTO venue (name, address, timezone) VALUES ('Los Pollos Hermanos', 'Brisbane, Australia', 'Australia/Brisbane');

-- Auth default user to venue
INSERT INTO venue_user (venue_id, user_id, is_admin) VALUES (1, 1, TRUE);

-- Add Check-Ins
INSERT INTO visit (id, in_dttm, venue_id, given_name, surname, phone, email, address, meta_info)
VALUES ('', '2020-06-01 20:00:00', 1, 'Walter', 'White', '', 'w.white@gmail.com', '', ''),
('', '2020-06-01 20:00:00', 1, 'Skylar', 'White', '', 's.white@gmail.com', '', ''),
('', '2020-06-01 20:00:00', 1, 'Walt Jr', 'White', '', 'flynn.white@gmail.com', '', ''),
('', '2020-06-01 20:05:00', 1, 'Marie', 'Schrader', '', 'h.schrader@gmail.com', '', ''),
('', '2020-06-01 20:05:00', 1, 'Hank', 'Schrader', '', 'm.schrader@gmail.com', '', '');

-- Add a check-in code
INSERT INTO venue_code (id, venue_id, code, name, start_dttm)
VALUES ('0', 1, 'tG74Hy', 'Customer Entrance', '2020-06-01 12:00:00'),
('1', 1, '8KrP4G', 'Delivery Entrance', '2020-06-01 12:00:00');

END TRANSACTION;
