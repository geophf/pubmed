
-- XML MAPPING ---------------------------------------------------------------

DROP TABLE IF EXISTS "xml_element";

CREATE TABLE "xml_element" (
	"id" serial NOT NULL,
	"xpath" TEXT NOT NULL,
	"xml_element" TEXT NOT NULL,
	CONSTRAINT "xml_element_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


DROP TABLE IF EXISTS "xml_element_map";

CREATE TABLE "xml_element_map" (
	"id" serial NOT NULL,
        "xml_element_id" integer NOT NULL,
	"table_nm" TEXT NOT NULL,
	"column_nm" TEXT NOT NULL,
        "processor" TEXT NOT NULL,
	CONSTRAINT "xml_element_map_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "not_mapped";

CREATE TABLE "not_mapped" (
	"id" serial NOT NULL,
	"article_stg_id" integer NOT NULL,
	"xml_element_id" integer NOT NULL,
	CONSTRAINT "not_mapped_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


-- ETL and STAGING TABLES ----------------------------------------------------

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
	"parsing_error" TEXT NULL,
	CONSTRAINT "abstract_stg_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

-- NEW TABLES FOR PUBMED ARTICLE ABSTRACTS -----------------------------------

DROP TABLE IF EXISTS "pubmed_article";

CREATE TABLE "pubmed_article" (
	"id" serial NOT NULL,
	"abstract_stg_id" integer NOT NULL,
	"publication_status_id" integer NULL,
	"pmid" integer NOT NULL,
	"e_location_id" integer NULL,
	"journal_id" integer NULL,
	"article_title" TEXT NOT NULL,
	"abstract_text" TEXT NOT NULL,
	"language_id" integer NULL,
	"medline_journal_info_id" integer NULL,
	"keyword_list_owner_id" integer NULL,
	CONSTRAINT "pubmed_article_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "article_id";

CREATE TABLE "article_id" (
	"id" serial NOT NULL,
	"id_type" integer NOT NULL,
	"id_value" TEXT NOT NULL,
	CONSTRAINT "article_id_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "pubmed_article_article_id";

CREATE TABLE "pubmed_article_article_id" (
	"id" serial NOT NULL,
	"pubmed_article_id" integer NOT NULL,
	"article_id_id" integer NOT NULL,
	CONSTRAINT "pubmed_article_article_id_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "pubmed_article_date";

CREATE TABLE "pubmed_article_date" (
	"id" serial NOT NULL,
	"pubmed_article_id" integer NOT NULL,
	"date_type_ind" integer NOT NULL,
	"date_value" DATE NOT NULL,
	CONSTRAINT "pubmed_article_date_id_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "journal_issue";

CREATE TABLE "journal_issue" (
	"id" serial NOT NULL,
	"volume" integer NOT NULL,
	"issue" integer NOT NULL,
	"pub_date" DATE NOT NULL,
	CONSTRAINT "journal_issue_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "journal";

CREATE TABLE "journal" (
	"id" serial NOT NULL,
	"publication_ind" integer NOT NULL,
	"issue_ind" integer NOT NULL,
	CONSTRAINT "journal_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "author";

CREATE TABLE "author" (
	"id" serial NOT NULL,
	"valid_ind" integer NOT NULL,
	"last_name" TEXT NOT NULL,
	"fore_name" TEXT NOT NULL,
	"initials" TEXT NOT NULL,
	CONSTRAINT "author_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE INDEX author_last_name_idx ON author (last_name);

DROP TABLE IF EXISTS "author_affiliation";

CREATE TABLE "author_affiliation" (
	"id" serial NOT NULL,
	"author_id" integer NOT NULL,
	"affiliation_ind" integer NOT NULL,
	CONSTRAINT "author_affiliation_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "pubmed_article_author";

CREATE TABLE "pubmed_article_author" (
	"id" serial NOT NULL,
	"pubmed_article_id" integer NOT NULL,
	"author_id" integer NOT NULL,
	CONSTRAINT "pubmed_article_author_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE INDEX pubmed_article_author_author_id_idx ON pubmed_article_author (author_id);

DROP TABLE IF EXISTS "pubmed_article_keyword";

CREATE TABLE "pubmed_article_keyword" (
	"id" serial NOT NULL,
	"pubmed_article_id" integer NOT NULL,
	"keyword_ind" integer NOT NULL,
	"major_topic_ind" integer NOT NULL,
	CONSTRAINT "pubmed_article_keyword_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE INDEX pubmed_article_keyword_keyword_ind_idx ON pubmed_article_keyword (keyword_ind);

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

CREATE TABLE "date_type_lk" (
	"id" serial NOT NULL,
	"date_type" TEXT NOT NULL,
	CONSTRAINT "date_type_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

INSERT INTO date_type_lk (date_type) 
VALUES ('COMPLETED'),('REVISED'),('PUBLISHED');

CREATE TABLE "article_id_lk" (
	"id" serial NOT NULL,
	"id_kind" TEXT NOT NULL,
	CONSTRAINT "article_id_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "publication_status_lk" (
	"id" serial NOT NULL,
	"status" TEXT NOT NULL,
	CONSTRAINT "publication_status_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "journal_lk" (
	"id" serial NOT NULL,
	"issn" TEXT NOT NULL,
	"title" TEXT NOT NULL,
	"iso_abbrev" TEXT NOT NULL,
	CONSTRAINT "journal_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "affiliation_lk" (
	"id" serial NOT NULL,
	"affiliation" TEXT NOT NULL,
	CONSTRAINT "affiliation_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "language_lk" (
	"id" serial NOT NULL,
	"language" TEXT NOT NULL,
	CONSTRAINT "language_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "keyword_list_owner_lk" (
	"id" serial NOT NULL,
	"owner" TEXT NOT NULL,
	CONSTRAINT "keyword_list_owner_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

DROP TABLE IF EXISTS "medline_journal_info_lk";

CREATE TABLE "medline_journal_info_lk" (
	"id" serial NOT NULL,
	"nlm_unique_id" integer NULL,
	"country_id" integer NULL,
	"issn_linking" TEXT NULL,
	CONSTRAINT "medline_journal_info_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "country_lk" (
	"id" serial NOT NULL,
	"country" TEXT NOT NULL,
	CONSTRAINT "country_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "keyword_lk" (
	"id" serial NOT NULL,
	"keyword" TEXT NOT NULL,
	CONSTRAINT "keyword_lk_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE INDEX keyword_lk_keyword_idx ON keyword_lk (keyword);

