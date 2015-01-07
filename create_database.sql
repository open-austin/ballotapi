-- Ballot API Create Table Statements / Schema
CREATE DATABASE ballotdb;

CREATE EXTENSION postgis;

--Create elections table
CREATE TABLE elections
(
election_id SERIAL PRIMARY KEY,
election_date DATE NOT NULL,
info TEXT
);

--Create precincts table
CREATE TABLE precincts
(
precinct_id SERIAL PRIMARY KEY,
election_id INTEGER, --Reference elections election_id
info TEXT,
confirmed DATE,
CONSTRAINT fk_election_id FOREIGN KEY (election_id) REFERENCES elections(election_id)
);

SELECT AddGeometryColumn('precincts', 'geom', 4326, 'multipolygon', 2);

--Create measures table
CREATE TABLE measures
(
measure_id SERIAL PRIMARY KEY,
election_id INTEGER, --Reference elections election_id
title TEXT,
info TEXT,
confirmed DATE,
question TEXT,
measure_type TEXT, --Constrain to valid choices
voting_system TEXT, -- Constrain to valid choices
choices JSON,
CONSTRAINT fk_election_id
	   FOREIGN KEY (election_id)
	   REFERENCES elections(election_id),
CONSTRAINT chk_measure_type CHECK (measure_type IN 
	  ('election', 'measure')),
CONSTRAINT chk_voting_system CHECK (voting_system IN 
	  ('plurality', 'approval', 'instant-runoff', 'ranked'))
);

--Create mappings table
CREATE TABLE mappings
(
precinct_id INTEGER, --Reference precincts precinct_id
measure_id INTEGER, --Reference measures measure_id
PRIMARY KEY (precinct_id, measure_id),
CONSTRAINT fk_precinct_id
	   FOREIGN KEY (precinct_id)
	   REFERENCES precincts(precinct_id),
CONSTRAINT fk_measure_id
	   FOREIGN KEY (measure_id)
	   REFERENCES measures(measure_id)
);
