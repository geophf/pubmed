DROP TABLE IF EXISTS "data_load";
DROP INDEX IF EXISTS "data_load_downloaded_ind_idx";

CREATE TABLE "data_load" (
	"id" serial NOT NULL,
	"packet_name" TEXT NOT NULL,
	"downloaded_ind" integer NOT NULL,
	"downloaded_dttm" TIMESTAMP,
	"processed_ind" integer,
	"processing_error" TEXT,
	CONSTRAINT "data_load_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE INDEX data_load_downloaded_ind_idx ON data_load (downloaded_ind);

DROP TABLE IF EXISTS "abstract_stg";

CREATE TABLE "abstract_stg" (
	"id" serial NOT NULL,
	"packet_id" integer NOT NULL,
	"raw_xml" TEXT NOT NULL,
	"parsed_ind" integer NOT NULL,
	"parsed_dttm" TIMESTAMP,
	CONSTRAINT "abstract_stg_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

-- LOOKUP TABLES -------------------------------------------------------------

CREATE TABLE "duality_lk" (
	"id" serial NOT NULL,
	"truth_serum" TEXT NOT NULL,
	CONSTRAINT "duality_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

INSERT INTO duality_lk (id,truth_serum)
VALUES (1,'Y'), (2,'N');
