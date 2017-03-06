-----------------------------------------------------------
--  Ennigaldi: a lightweight set of museum applications  --
--             Django SQLite database schema             --
--  (c) 2017 Ábaco Arquitetura & Design Ambiental Ltda.  --
--          Distributed under the M.I.T. License         --
--       This document for reference purposes only.      --
--       Authoritative and current schema only at:       --
--        https://github.com/arq-abaco/ennigaldi         --
-----------------------------------------------------------
BEGIN TRANSACTION;
CREATE TABLE "place_place" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "location_name" varchar(63) NOT NULL, "location_name_type" varchar(11) NOT NULL, "location_extent" varchar(63) NOT NULL, "email" varchar(254) NOT NULL, "phone_primary" varchar(31) NOT NULL, "phone_secondary" varchar(31) NOT NULL, "website" varchar(255) NOT NULL, "address_1" varchar(35) NOT NULL, "address_2" varchar(35) NOT NULL, "city" varchar(35) NOT NULL, "state_province" varchar(35) NOT NULL, "zip_code" varchar(35) NOT NULL, "country" varchar(35) NOT NULL);
CREATE TABLE "objectinfo_workinstance" ("artifact_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "objectinfo_artifact" ("work_id"), "copy_number" varchar(63) NOT NULL, "edition_number" varchar(63) NOT NULL, "form" varchar(255) NOT NULL, "issue_source" varchar(255) NOT NULL);
CREATE TABLE "objectinfo_textref" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "textref_name" varchar(255) NOT NULL, "textref_name_type" varchar(15) NOT NULL, "textref_refid" varchar(63) NOT NULL, "textref_refid_type" smallint unsigned NOT NULL, "textref_datadate" date NOT NULL, "textref_location_id" integer NOT NULL REFERENCES "place_place" ("id"), "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_techniquetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "technique" varchar(64) NOT NULL, "tecnique_type" varchar(255) NOT NULL UNIQUE);
CREATE TABLE "objectinfo_technicalattribute" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "attribute_type" smallint unsigned NOT NULL, "attribute_value" integer unsigned NOT NULL, "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_specimendatetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_type" varchar(31) NOT NULL, "date_source" varchar(255) NULL, "date_value_id" integer NOT NULL REFERENCES "historicdate_historicdate" ("id"), "date_of_id" integer NOT NULL REFERENCES "objectinfo_specimen" ("work_id"));
CREATE TABLE "objectinfo_specimen_colour" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "specimen_id" integer NOT NULL REFERENCES "objectinfo_specimen" ("work_id"), "colour_id" integer NOT NULL REFERENCES "objectinfo_colour" ("id"));
CREATE TABLE "objectinfo_specimen" ("work_id" integer NOT NULL PRIMARY KEY REFERENCES "objectinfo_objectidentification" ("work_id"), "physical_description" text NOT NULL, "description_display" text NOT NULL, "specimen_age" decimal NOT NULL, "specimen_age_qualification" smallint unsigned NOT NULL, "specimen_age_unit" smallint unsigned NOT NULL, "phase" varchar(255) NOT NULL, "sex" smallint unsigned NOT NULL);
CREATE TABLE "objectinfo_relatedobject" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relation_type" smallint unsigned NOT NULL, "related_note" text NOT NULL, "work1_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"), "work2_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_ownership" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "owner_category" smallint unsigned NOT NULL, "owner_begin_date" date NOT NULL, "owner_end_date" date NOT NULL, "owner_method" smallint unsigned NOT NULL, "owner_note" text NOT NULL, "sale_price" decimal NOT NULL, "owner_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "owner_place_id" integer NOT NULL REFERENCES "place_place" ("id"));
CREATE TABLE "objectinfo_otherobjectnumber" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_number" varchar(72) NOT NULL, "object_number_type" varchar(255) NOT NULL, "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_objectrights_rights_holder" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "objectrights_id" integer NOT NULL REFERENCES "objectinfo_objectrights" ("rights_refid"), "agent_id" integer NOT NULL REFERENCES "agent_agent" ("id"));
CREATE TABLE "objectinfo_objectrights" ("right_begin_date" date NOT NULL, "right_end_date" date NOT NULL, "rights_display" varchar(255) NOT NULL, "rights_notes" text NOT NULL, "rights_refid" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rights_type" smallint unsigned NOT NULL, "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_objectproduction_technique_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "objectproduction_id" integer NOT NULL REFERENCES "objectinfo_objectproduction" ("id"), "techniquetype_id" integer NOT NULL REFERENCES "objectinfo_techniquetype" ("id"));
CREATE TABLE "objectinfo_objectproduction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "production_note" text NOT NULL, "technical_justification" text NOT NULL, "production_date_id" integer NOT NULL UNIQUE REFERENCES "historicdate_historicdate" ("id"), "work_id" integer NOT NULL UNIQUE REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_objectplacetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "location_type" varchar(31) NOT NULL, "location_id" integer NOT NULL REFERENCES "place_place" ("id"), "work_id" integer NOT NULL REFERENCES "objectinfo_objectproduction" ("id"));
CREATE TABLE "objectinfo_objectname" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_name" varchar(255) NOT NULL, "name_currency" date NOT NULL, "name_level" varchar(63) NOT NULL, "name_note" text NOT NULL, "name_source" varchar(255) NOT NULL, "name_type" smallint unsigned NOT NULL, "name_preferred" bool NOT NULL, "title_translation" varchar(255) NOT NULL, "identification_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"), "name_lang_id" varchar(7) NOT NULL REFERENCES "objectinfo_isolanguage" ("language_iso"));
CREATE TABLE "objectinfo_objectmaterial" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "material_component" varchar(63) NOT NULL, "material_note" varchar(255) NOT NULL, "material_name" varchar(255) NOT NULL, "material_source_id" integer NOT NULL REFERENCES "place_place" ("id"));
CREATE TABLE "objectinfo_objectlocation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "location_fitness" text NOT NULL, "location_note" text NOT NULL, "location_date" datetime NOT NULL, "location_id" integer NOT NULL REFERENCES "objectinfo_location" ("id"), "normal_location_id" integer NOT NULL REFERENCES "objectinfo_location" ("id"), "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_objectinscription" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "inscription_display" text NOT NULL, "inscription_type" varchar(15) NOT NULL, "inscription_notes" text NOT NULL, "inscription_position" varchar(255) NOT NULL, "inscription_script" varchar(63) NOT NULL, "inscription_text" text NOT NULL, "inscription_transliteration" text NOT NULL, "inscription_translation" text NOT NULL, "inscription_author_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "inscription_date_id" integer NOT NULL UNIQUE REFERENCES "historicdate_historicdate" ("id"), "inscription_language_id" varchar(7) NOT NULL REFERENCES "objectinfo_isolanguage" ("language_iso"), "inscription_method_id" integer NOT NULL REFERENCES "objectinfo_techniquetype" ("id"), "work_id" integer NOT NULL UNIQUE REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_objectidentification" ("work_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "work_snapshot" varchar(100) NOT NULL, "source" varchar(255) NOT NULL, "description" text NOT NULL, "description_source" varchar(255) NOT NULL, "comments" text NOT NULL, "distinguishing_features" text NOT NULL, "work_type" varchar(255) NOT NULL);
CREATE TABLE "objectinfo_objectdimension" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "dimension_part" varchar(32) NOT NULL, "dimension_type" smallint unsigned NOT NULL, "dimension_value" integer unsigned NOT NULL, "dimension_value_date" date NOT NULL, "dimension_value_qualifier" bool NOT NULL, "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_materialtype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "material_type" smallint unsigned NOT NULL, "material_extent" varchar(255) NOT NULL, "material_id" integer NOT NULL REFERENCES "objectinfo_objectmaterial" ("id"), "work_id" integer NOT NULL REFERENCES "objectinfo_artifact" ("work_id"));
CREATE TABLE "objectinfo_location" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "location_id" varchar(7) NOT NULL, "location_name" varchar(32) NOT NULL, "location_note" text NOT NULL, "address_id" integer NOT NULL REFERENCES "place_place" ("id"), "agent_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "location_parent_id" integer NOT NULL REFERENCES "objectinfo_location" ("id"));
CREATE TABLE "objectinfo_isolanguage" ("language_iso" varchar(7) NOT NULL PRIMARY KEY, "language" varchar(63) NOT NULL UNIQUE);
CREATE TABLE "objectinfo_descriptioncontent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_name" varchar(255) NOT NULL, "content_type" smallint unsigned NOT NULL);
CREATE TABLE "objectinfo_contentmeta" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_type" varchar(63) NOT NULL, "event_type" varchar(63) NOT NULL, "other_type" varchar(63) NOT NULL, "content_script" varchar(255) NOT NULL, "content_position" varchar(63) NOT NULL, "content_source" varchar(255) NOT NULL, "content_id" integer NOT NULL REFERENCES "objectinfo_descriptioncontent" ("id"), "content_lang_id" varchar(7) NOT NULL REFERENCES "objectinfo_isolanguage" ("language_iso"), "work_id" integer NOT NULL REFERENCES "objectinfo_artifact" ("work_id"));
CREATE TABLE "objectinfo_colour" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "colour" varchar(255) NOT NULL UNIQUE);
CREATE TABLE "objectinfo_associatedobject" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "associated_object_name" varchar(255) NOT NULL, "associated_object_type" varchar(64) NOT NULL, "associated_object_datadate" date NOT NULL, "work_id" integer NOT NULL REFERENCES "objectinfo_objectidentification" ("work_id"));
CREATE TABLE "objectinfo_artifactdatetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_type" varchar(31) NOT NULL, "date_source" varchar(255) NULL, "date_value_id" integer NOT NULL REFERENCES "historicdate_historicdate" ("id"), "date_of_id" integer NOT NULL REFERENCES "objectinfo_artifact" ("work_id"));
CREATE TABLE "objectinfo_artifact_colour" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "artifact_id" integer NOT NULL REFERENCES "objectinfo_artifact" ("work_id"), "colour_id" integer NOT NULL REFERENCES "objectinfo_colour" ("id"));
CREATE TABLE "objectinfo_artifact" ("work_id" integer NOT NULL PRIMARY KEY REFERENCES "objectinfo_objectidentification" ("work_id"), "physical_description" text NOT NULL, "description_display" text NOT NULL, "status" varchar(255) NOT NULL, "style" varchar(255) NOT NULL, "cultural_context" varchar(255) NOT NULL);
CREATE TABLE "objectinfo_agentrole" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "agent_role" varchar(31) NOT NULL, "attributed" bool NOT NULL, "attribution_type" varchar(31) NOT NULL, "agent_role_display" varchar(255) NOT NULL, "agent_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "work_id" integer NOT NULL REFERENCES "objectinfo_objectproduction" ("id"));
CREATE TABLE "historicdate_historicdate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_earliest" varchar(15) NOT NULL, "date_earliest_accuracy" bool NOT NULL, "date_latest" varchar(15) NOT NULL, "date_latest_accuracy" bool NOT NULL, "date_source" varchar(255) NOT NULL, "date_display" varchar(255) NOT NULL);
CREATE TABLE "agent_agentdatetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_type" varchar(31) NOT NULL, "date_source" varchar(255) NULL, "date_of_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "date_value_id" integer NOT NULL REFERENCES "historicdate_historicdate" ("id"));
CREATE TABLE "agent_agentaffiliation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "agent_role" varchar(255) NOT NULL, "agent_affiliation_id" integer NOT NULL REFERENCES "agent_agent" ("id"), "agent_person_id" integer NOT NULL REFERENCES "agent_agent" ("id"));
CREATE TABLE "agent_agent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "agent_name" varchar(255) NOT NULL, "name_type" varchar(15) NOT NULL, "agent_culture" varchar(63) NOT NULL, "agent_display" varchar(255) NOT NULL, "orcid" varchar(31) NOT NULL, "email" varchar(254) NOT NULL, "phone_primary" varchar(31) NOT NULL, "phone_mobile" varchar(31) NOT NULL, "phone_business" varchar(31) NOT NULL, "phone_home" varchar(31) NOT NULL, "address_1" varchar(35) NOT NULL, "address_2" varchar(35) NOT NULL, "city" varchar(35) NOT NULL, "state_province" varchar(31) NOT NULL, "zip_code" varchar(31) NOT NULL, "country" varchar(31) NOT NULL, "website" varchar(255) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id"));
CREATE INDEX "objectinfo_textref_84c7ac35" ON "objectinfo_textref" ("work_id");
CREATE INDEX "objectinfo_textref_2a36e7a9" ON "objectinfo_textref" ("textref_location_id");
CREATE INDEX "objectinfo_technicalattribute_84c7ac35" ON "objectinfo_technicalattribute" ("work_id");
CREATE INDEX "objectinfo_specimendatetype_e400e55a" ON "objectinfo_specimendatetype" ("date_value_id");
CREATE INDEX "objectinfo_specimendatetype_d90a8332" ON "objectinfo_specimendatetype" ("date_of_id");
CREATE UNIQUE INDEX "objectinfo_specimen_colour_specimen_id_22861730_uniq" ON "objectinfo_specimen_colour" ("specimen_id", "colour_id");
CREATE INDEX "objectinfo_specimen_colour_ea0c5523" ON "objectinfo_specimen_colour" ("specimen_id");
CREATE INDEX "objectinfo_specimen_colour_97e96fa3" ON "objectinfo_specimen_colour" ("colour_id");
CREATE INDEX "objectinfo_relatedobject_ae295abb" ON "objectinfo_relatedobject" ("work1_id");
CREATE INDEX "objectinfo_relatedobject_35108048" ON "objectinfo_relatedobject" ("work2_id");
CREATE INDEX "objectinfo_ownership_b3615c03" ON "objectinfo_ownership" ("owner_place_id");
CREATE INDEX "objectinfo_ownership_5e7b1936" ON "objectinfo_ownership" ("owner_id");
CREATE INDEX "objectinfo_otherobjectnumber_84c7ac35" ON "objectinfo_otherobjectnumber" ("work_id");
CREATE UNIQUE INDEX "objectinfo_objectrights_rights_holder_objectrights_id_8edb407c_uniq" ON "objectinfo_objectrights_rights_holder" ("objectrights_id", "agent_id");
CREATE INDEX "objectinfo_objectrights_rights_holder_9b18f05f" ON "objectinfo_objectrights_rights_holder" ("agent_id");
CREATE INDEX "objectinfo_objectrights_rights_holder_20280bbd" ON "objectinfo_objectrights_rights_holder" ("objectrights_id");
CREATE INDEX "objectinfo_objectrights_84c7ac35" ON "objectinfo_objectrights" ("work_id");
CREATE INDEX "objectinfo_objectplacetype_e274a5da" ON "objectinfo_objectplacetype" ("location_id");
CREATE INDEX "objectinfo_objectplacetype_84c7ac35" ON "objectinfo_objectplacetype" ("work_id");
CREATE INDEX "objectinfo_objectname_a7eb5a82" ON "objectinfo_objectname" ("name_lang_id");
CREATE INDEX "objectinfo_objectname_88bcc9f7" ON "objectinfo_objectname" ("identification_id");
CREATE INDEX "objectinfo_objectmaterial_ba71f27b" ON "objectinfo_objectmaterial" ("material_source_id");
CREATE INDEX "objectinfo_objectlocation_e274a5da" ON "objectinfo_objectlocation" ("location_id");
CREATE INDEX "objectinfo_objectlocation_84c7ac35" ON "objectinfo_objectlocation" ("work_id");
CREATE INDEX "objectinfo_objectlocation_0b586d1f" ON "objectinfo_objectlocation" ("normal_location_id");
CREATE INDEX "objectinfo_objectinscription_d8597e5b" ON "objectinfo_objectinscription" ("inscription_author_id");
CREATE INDEX "objectinfo_objectinscription_2fc5f6f9" ON "objectinfo_objectinscription" ("inscription_method_id");
CREATE INDEX "objectinfo_objectinscription_0ac4a0d3" ON "objectinfo_objectinscription" ("inscription_language_id");
CREATE INDEX "objectinfo_objectdimension_84c7ac35" ON "objectinfo_objectdimension" ("work_id");
CREATE INDEX "objectinfo_materialtype_eb4b9aaa" ON "objectinfo_materialtype" ("material_id");
CREATE INDEX "objectinfo_materialtype_84c7ac35" ON "objectinfo_materialtype" ("work_id");
CREATE INDEX "objectinfo_location_efd378c7" ON "objectinfo_location" ("location_parent_id");
CREATE INDEX "objectinfo_location_ea8e5d12" ON "objectinfo_location" ("address_id");
CREATE INDEX "objectinfo_location_9b18f05f" ON "objectinfo_location" ("agent_id");
CREATE INDEX "objectinfo_contentmeta_e547f8f1" ON "objectinfo_contentmeta" ("content_lang_id");
CREATE INDEX "objectinfo_contentmeta_e14f02ad" ON "objectinfo_contentmeta" ("content_id");
CREATE INDEX "objectinfo_contentmeta_84c7ac35" ON "objectinfo_contentmeta" ("work_id");
CREATE INDEX "objectinfo_associatedobject_84c7ac35" ON "objectinfo_associatedobject" ("work_id");
CREATE INDEX "objectinfo_artifactdatetype_e400e55a" ON "objectinfo_artifactdatetype" ("date_value_id");
CREATE INDEX "objectinfo_artifactdatetype_d90a8332" ON "objectinfo_artifactdatetype" ("date_of_id");
CREATE INDEX "objectinfo_agentrole_9b18f05f" ON "objectinfo_agentrole" ("agent_id");
CREATE INDEX "objectinfo_agentrole_84c7ac35" ON "objectinfo_agentrole" ("work_id");
COMMIT;
