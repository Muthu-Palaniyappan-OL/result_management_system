import { DB } from "kysely-codegen";
import SQLite from "better-sqlite3";
import { Kysely, SqliteDialect } from "kysely";

const dialect = new SqliteDialect({
  database: new SQLite(":memory:"),
});

const database = new Kysely<DB>({
  dialect,
});

export default database;
