-- Add new schema named "public"
CREATE SCHEMA IF NOT EXISTS "public";
-- Set comment to schema: "public"
COMMENT ON SCHEMA "public" IS 'standard public schema';
-- Create "users" table
CREATE TABLE "public"."users" ("id" serial NOT NULL, "email" character varying NOT NULL, "username" character varying NOT NULL, "password" character varying NOT NULL, "is_active" boolean NOT NULL, "is_superuser" boolean NOT NULL, "created_by" integer NULL, "created_at" timestamp NOT NULL, "updated_by" integer NULL, "updated_at" timestamp NOT NULL, PRIMARY KEY ("id"), CONSTRAINT "users_email_key" UNIQUE ("email"), CONSTRAINT "users_username_key" UNIQUE ("username"));
