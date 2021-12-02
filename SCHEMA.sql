-- DROP SCHEMA "Project_1";

CREATE SCHEMA "Project_1" AUTHORIZATION postgres;

COMMENT ON SCHEMA "Project_1" IS 'CS425 Project Database';

-- "Project_1"."Hospital" definition

-- Drop table

-- DROP TABLE "Project_1"."Hospital";

CREATE TABLE "Project_1"."Hospital" (
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
CREATE INDEX hospital_hospitalname_idx ON "Project_1"."Hospital" USING btree (hospitalname);
CREATE INDEX hospital_region_idx ON "Project_1"."Hospital" USING btree (region);

-- Permissions

ALTER TABLE "Project_1"."Hospital" OWNER TO postgres;
GRANT ALL ON TABLE "Project_1"."Hospital" TO postgres;
GRANT ALL ON TABLE "Project_1"."Hospital" TO admin;


-- "Project_1".doctor definition

-- Drop table

-- DROP TABLE "Project_1".doctor;

CREATE TABLE "Project_1".doctor (
	doctorid bpchar(7) NOT NULL,
	doctorname varchar(30) NULL,
	specialization varchar(25) NULL,
	fee numeric(12, 2) NULL,
	CONSTRAINT doctor_pk PRIMARY KEY (doctorid),
	CONSTRAINT fee_check CHECK ((fee >= (0)::numeric))
);
CREATE INDEX doctor_specialization_idx ON "Project_1".doctor USING btree (specialization);

-- Permissions

ALTER TABLE "Project_1".doctor OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".doctor TO postgres;
GRANT ALL ON TABLE "Project_1".doctor TO admin;


-- "Project_1".donor definition

-- Drop table

-- DROP TABLE "Project_1".donor;

CREATE TABLE "Project_1".donor (
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
CREATE INDEX donor_bloodtype_idx ON "Project_1".donor USING btree (bloodtype);
CREATE INDEX donor_donorname_idx ON "Project_1".donor USING btree (donorname);
CREATE INDEX donor_lastdonation_idx ON "Project_1".donor USING btree (lastdonation);
CREATE INDEX donor_organname_idx ON "Project_1".donor USING btree (organname);

-- Permissions

ALTER TABLE "Project_1".donor OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".donor TO postgres;
GRANT INSERT, SELECT, UPDATE ON TABLE "Project_1".donor TO doctor;
GRANT ALL ON TABLE "Project_1".donor TO admin;


-- "Project_1".patient definition

-- Drop table

-- DROP TABLE "Project_1".patient;

CREATE TABLE "Project_1".patient (
	patientid bpchar(7) NOT NULL,
	patientname varchar(30) NULL,
	bloodtype varchar(3) NOT NULL,
	age numeric NULL,
	drughistory varchar(30) NULL,
	allergies varchar(40) NULL,
	CONSTRAINT patient_pk PRIMARY KEY (patientid)
);
CREATE INDEX patient_bloodtype_idx ON "Project_1".patient USING btree (bloodtype);
CREATE INDEX patient_patientname_idx ON "Project_1".patient USING btree (patientname);

-- Permissions

ALTER TABLE "Project_1".patient OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".patient TO postgres;
GRANT INSERT, SELECT, UPDATE ON TABLE "Project_1".patient TO doctor;
GRANT ALL ON TABLE "Project_1".patient TO admin;


-- "Project_1".affiliated definition

-- Drop table

-- DROP TABLE "Project_1".affiliated;

CREATE TABLE "Project_1".affiliated (
	doctorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT affiliated_pk PRIMARY KEY (doctorid, hospitalid),
	CONSTRAINT affiliated_fk FOREIGN KEY (hospitalid) REFERENCES "Project_1"."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT affiliated_fk_1 FOREIGN KEY (doctorid) REFERENCES "Project_1".doctor(doctorid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE "Project_1".affiliated OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".affiliated TO postgres;
GRANT ALL ON TABLE "Project_1".affiliated TO admin;


-- "Project_1".donates definition

-- Drop table

-- DROP TABLE "Project_1".donates;

CREATE TABLE "Project_1".donates (
	donorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT donates_pk PRIMARY KEY (donorid, hospitalid),
	CONSTRAINT donates_fk FOREIGN KEY (donorid) REFERENCES "Project_1".donor(donorid) ON DELETE CASCADE,
	CONSTRAINT donates_fk_1 FOREIGN KEY (hospitalid) REFERENCES "Project_1"."Hospital"(hospitalid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE "Project_1".donates OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".donates TO postgres;
GRANT ALL ON TABLE "Project_1".donates TO admin;


-- "Project_1".operated definition

-- Drop table

-- DROP TABLE "Project_1".operated;

CREATE TABLE "Project_1".operated (
	doctorid varchar(7) NOT NULL,
	patientid varchar(7) NOT NULL,
	fee numeric NULL,
	CONSTRAINT check_fee CHECK ((fee >= (0)::numeric)),
	CONSTRAINT operated_pk PRIMARY KEY (doctorid, patientid),
	CONSTRAINT operated_fk FOREIGN KEY (doctorid) REFERENCES "Project_1".doctor(doctorid) ON DELETE CASCADE,
	CONSTRAINT operated_fk_1 FOREIGN KEY (patientid) REFERENCES "Project_1".patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE "Project_1".operated OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".operated TO postgres;
GRANT ALL ON TABLE "Project_1".operated TO admin;


-- "Project_1".organ definition

-- Drop table

-- DROP TABLE "Project_1".organ;

CREATE TABLE "Project_1".organ (
	doctorid bpchar(7) NOT NULL,
	organid bpchar(7) NOT NULL,
	organname varchar(25) NULL,
	life_hrs numeric NULL,
	availibilitydate date NULL,
	donorid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT organ_pk PRIMARY KEY (doctorid, organid, donorid, hospitalid),
	CONSTRAINT organ_doctorid_fkey FOREIGN KEY (doctorid) REFERENCES "Project_1".doctor(doctorid) ON DELETE CASCADE,
	CONSTRAINT organ_fk FOREIGN KEY (hospitalid) REFERENCES "Project_1"."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT organ_fk_1 FOREIGN KEY (donorid) REFERENCES "Project_1".donor(donorid)
);
CREATE INDEX organ_availibilitydate_idx ON "Project_1".organ USING btree (availibilitydate);
CREATE INDEX organ_donorid_idx ON "Project_1".organ USING btree (donorid);
CREATE INDEX organ_organname_idx ON "Project_1".organ USING btree (organname);

-- Permissions

ALTER TABLE "Project_1".organ OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".organ TO postgres;
GRANT INSERT, SELECT, UPDATE ON TABLE "Project_1".organ TO doctor;
GRANT ALL ON TABLE "Project_1".organ TO admin;


-- "Project_1".patient_needs definition

-- Drop table

-- DROP TABLE "Project_1".patient_needs;

CREATE TABLE "Project_1".patient_needs (
	patientid varchar(7) NOT NULL,
	need varchar(20) NULL,
	CONSTRAINT patient_needs_pk PRIMARY KEY (patientid),
	CONSTRAINT patient_needs_fk FOREIGN KEY (patientid) REFERENCES "Project_1".patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE "Project_1".patient_needs OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".patient_needs TO postgres;
GRANT ALL ON TABLE "Project_1".patient_needs TO admin;


-- "Project_1".treated definition

-- Drop table

-- DROP TABLE "Project_1".treated;

CREATE TABLE "Project_1".treated (
	patientid varchar(7) NOT NULL,
	hospitalid varchar(7) NOT NULL,
	CONSTRAINT treated_pk PRIMARY KEY (patientid, hospitalid),
	CONSTRAINT treated_fk FOREIGN KEY (hospitalid) REFERENCES "Project_1"."Hospital"(hospitalid) ON DELETE CASCADE,
	CONSTRAINT treated_fk_1 FOREIGN KEY (patientid) REFERENCES "Project_1".patient(patientid) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE "Project_1".treated OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".treated TO postgres;
GRANT ALL ON TABLE "Project_1".treated TO admin;


-- "Project_1".donorlist source

CREATE OR REPLACE VIEW "Project_1".donorlist
AS SELECT donor.bloodtype,
    donor.organname,
    donor.donorid
   FROM "Project_1".donor;

-- Permissions

ALTER TABLE "Project_1".donorlist OWNER TO postgres;
GRANT ALL ON TABLE "Project_1".donorlist TO postgres;
GRANT INSERT, SELECT, UPDATE ON TABLE "Project_1".donorlist TO doctor;
GRANT SELECT ON TABLE "Project_1".donorlist TO patient;
GRANT ALL ON TABLE "Project_1".donorlist TO admin;




-- Permissions

GRANT ALL ON SCHEMA "Project_1" TO postgres;
GRANT ALL ON SCHEMA "Project_1" TO public;
