COMMENT ON SCHEMA {schema} IS 'CS425 Project Database';

-- {schema}."Hospital" definition

CREATE TABLE {schema}."Hospital" (
	hospitalid varchar(7) NOT NULL,
	hospitalname varchar(20) NULL,
	region varchar(30) NULL,
	hospitalizationcost numeric(12, 2) NULL,
	numberofopenbeds numeric NULL,
	numberofavailableorgans numeric NULL,
	CONSTRAINT "Hospital_hospitalizationcost_check" CHECK ((hospitalizationcost >= (0)::numeric)),
	CONSTRAINT "Hospital_numberofavailableorgans_check" CHECK ((numberofavailableorgans >= (0)::numeric)),
	CONSTRAINT "Hospital_numberofopenbeds_check" CHECK ((numberofopenbeds >= (0)::numeric)),
	CONSTRAINT hospital_pk PRIMARY KEY (hospitalid)
);
CREATE INDEX hospital_hospitalname_idx ON {schema}."Hospital" USING btree (hospitalname);
CREATE INDEX hospital_region_idx ON {schema}."Hospital" USING btree (region);

-- Permissions

ALTER TABLE {schema}."Hospital" OWNER TO postgres;
GRANT ALL ON TABLE {schema}."Hospital" TO postgres;


-- {schema}.doctor definition

CREATE TABLE {schema}.doctor (
	doctorid bpchar(7) NOT NULL,
	doctorname varchar(30) NULL,
	specialization varchar(25) NULL,
	fee numeric(12, 2) NULL,
	region varchar(25) NULL,
	CONSTRAINT doctor_pk PRIMARY KEY (doctorid),
	CONSTRAINT fee_check CHECK ((fee >= (0)::numeric))
);
CREATE INDEX doctor_specialization_idx ON {schema}.doctor USING btree (specialization);

-- Permissions

ALTER TABLE {schema}.doctor OWNER TO postgres;
GRANT ALL ON TABLE {schema}.doctor TO postgres;


-- {schema}.donor definition

CREATE TABLE {schema}.donor (
	donorid bpchar(7) NOT NULL,
	bloodtype varchar(3) NULL,
	age numeric NULL,
	chronicaldisease varchar(30) NULL,
	drugusage varchar(30) NULL,
	lasttattoo date NULL,
	medicalhistory varchar(50) NULL,
	lastdonation date NULL,
	phone bpchar(7) NULL,
	email varchar(40) NULL,
	region varchar(30) NULL,
	organname varchar(25) NULL,
	donorname varchar(35) NOT NULL,
	CONSTRAINT age_check CHECK ((age > (0)::numeric)),
	CONSTRAINT organ_donor_pk PRIMARY KEY (donorid)
);
CREATE INDEX donor_bloodtype_idx ON {schema}.donor USING btree (bloodtype);
CREATE INDEX donor_donorname_idx ON {schema}.donor USING btree (donorname);
CREATE INDEX donor_lastdonation_idx ON {schema}.donor USING btree (lastdonation);
CREATE INDEX donor_organname_idx ON {schema}.donor USING btree (organname);

-- Permissions

ALTER TABLE {schema}.donor OWNER TO postgres;
GRANT ALL ON TABLE {schema}.donor TO postgres;


-- {schema}.patient definition

CREATE TABLE {schema}.patient (
	patientid bpchar(7) NOT NULL,
	patientname varchar(30) NULL,
	bloodtype varchar(3) NOT NULL,
	age numeric NULL,
	drughistory varchar(30) NULL,
	allergies varchar(40) NULL,
	region varchar(25) NULL,
	CONSTRAINT patient_pk PRIMARY KEY (patientid)
);
CREATE INDEX patient_bloodtype_idx ON {schema}.patient USING btree (bloodtype);
CREATE INDEX patient_patientname_idx ON {schema}.patient USING btree (patientname);

-- Permissions

ALTER TABLE {schema}.patient OWNER TO postgres;
GRANT ALL ON TABLE {schema}.patient TO postgres;


-- {schema}.affiliated definition

CREATE TABLE {schema}.affiliated (
	doctorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT affiliated_pk PRIMARY KEY (doctorid, hospitalid),
	CONSTRAINT affiliated_fk FOREIGN KEY (hospitalid) REFERENCES {schema}."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT affiliated_fk_1 FOREIGN KEY (doctorid) REFERENCES {schema}.doctor(doctorid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE {schema}.affiliated OWNER TO postgres;
GRANT ALL ON TABLE {schema}.affiliated TO postgres;


-- {schema}.donates definition

CREATE TABLE {schema}.donates (
	donorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT donates_pk PRIMARY KEY (donorid, hospitalid),
	CONSTRAINT donates_fk FOREIGN KEY (donorid) REFERENCES {schema}.donor(donorid) ON DELETE CASCADE,
	CONSTRAINT donates_fk_1 FOREIGN KEY (hospitalid) REFERENCES {schema}."Hospital"(hospitalid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE {schema}.donates OWNER TO postgres;
GRANT ALL ON TABLE {schema}.donates TO postgres;


-- {schema}.operated definition

CREATE TABLE {schema}.operated (
	doctorid varchar(7) NOT NULL,
	patientid varchar(7) NOT NULL,
	fee numeric NULL,
	CONSTRAINT check_fee CHECK ((fee >= (0)::numeric)),
	CONSTRAINT operated_pk PRIMARY KEY (doctorid, patientid),
	CONSTRAINT operated_fk FOREIGN KEY (doctorid) REFERENCES {schema}.doctor(doctorid) ON DELETE CASCADE,
	CONSTRAINT operated_fk_1 FOREIGN KEY (patientid) REFERENCES {schema}.patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE {schema}.operated OWNER TO postgres;
GRANT ALL ON TABLE {schema}.operated TO postgres;


-- {schema}.organ definition

CREATE TABLE {schema}.organ (
	doctorid bpchar(7) NOT NULL,
	organid bpchar(7) NOT NULL,
	organname varchar(25) NULL,
	life_hrs numeric NULL,
	availibilitydate date NULL,
	donorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT organ_pk PRIMARY KEY (doctorid, organid, donorid, hospitalid),
	CONSTRAINT organ_doctorid_fkey FOREIGN KEY (doctorid) REFERENCES {schema}.doctor(doctorid) ON DELETE CASCADE,
	CONSTRAINT organ_fk FOREIGN KEY (hospitalid) REFERENCES {schema}."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT organ_fk_1 FOREIGN KEY (donorid) REFERENCES {schema}.donor(donorid)
);
CREATE INDEX organ_availibilitydate_idx ON {schema}.organ USING btree (availibilitydate);
CREATE INDEX organ_donorid_idx ON {schema}.organ USING btree (donorid);
CREATE INDEX organ_organname_idx ON {schema}.organ USING btree (organname);

-- Permissions

ALTER TABLE {schema}.organ OWNER TO postgres;
GRANT ALL ON TABLE {schema}.organ TO postgres;


-- {schema}.patient_needs definition

CREATE TABLE {schema}.patient_needs (
	patientid varchar(7) NOT NULL,
	need varchar(20) NULL,
	CONSTRAINT patient_needs_pk PRIMARY KEY (patientid),
	CONSTRAINT patient_needs_fk FOREIGN KEY (patientid) REFERENCES {schema}.patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE {schema}.patient_needs OWNER TO postgres;


-- {schema}.treated definition

CREATE TABLE {schema}.treated (
	patientid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT treated_pk PRIMARY KEY (patientid, hospitalid),
	CONSTRAINT treated_fk FOREIGN KEY (hospitalid) REFERENCES {schema}."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT treated_fk_1 FOREIGN KEY (patientid) REFERENCES {schema}.patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE {schema}.treated OWNER TO postgres;


-- {schema}.blooddonorlist source

CREATE OR REPLACE VIEW {schema}.organdonorlist
AS SELECT donor.bloodtype,
    donor.organname,
    donor.donorid
   FROM project_1.donor;

-- Permissions

ALTER TABLE {schema}.organdonorlist OWNER TO postgres;
GRANT ALL ON TABLE {schema}.organdonorlist TO postgres;


-- {schema}.blooddonorlist source

CREATE OR REPLACE VIEW {schema}.blooddonorlist
AS SELECT donor.bloodtype,
    donor.age,
    donor.donorid,
    donor.lastdonation
   FROM {schema}.donor where organname = 'blood';

-- Permissions

ALTER TABLE {schema}.blooddonorlist OWNER TO postgres;
GRANT ALL ON TABLE {schema}.donorlist TO postgres;




-- Permissions

GRANT ALL ON SCHEMA {schema} TO postgres;


-- Admin Permissions

GRANT USAGE, CREATE ON SCHEMA {schema} TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}."Hospital" TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.affiliated TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.doctor TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.donates TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.donor TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.blooddonorlist TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.organdonorlist TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.operated TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.organ TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.patient TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.patient_needs TO "admin";
GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE {schema}.treated TO "admin";


-- Doctor permissions

GRANT SELECT ON TABLE {schema}."Hospital" TO doctor;
GRANT SELECT ON TABLE {schema}.doctor TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.donor TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.blooddonorlist TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.organdonorlist TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.operated TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.organ TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.patient TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.patient_needs TO doctor;
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE {schema}.treated TO doctor;


-- Patient permissions

GRANT SELECT ON TABLE {schema}.donorlist TO patient;