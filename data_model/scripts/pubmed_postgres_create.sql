DROP TABLE IF EXISTS "data_load";

CREATE TABLE "data_load" (
	"id" serial NOT NULL,
	"packet_name" TEXT NOT NULL,
	"downloaded_ind" integer NOT NULL,
	"downloaded_dttm" TIMESTAMP,
	CONSTRAINT "data_load_pk" PRIMARY KEY ("id")
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


