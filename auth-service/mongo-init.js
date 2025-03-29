const username = process.env.MONGO_INITDB_ROOT_USERNAME;
const password = process.env.MONGO_INITDB_ROOT_PASSWORD;

// Initialize auth-service database
db = db.getSiblingDB("auth-db");
db.createUser({
  user: username,
  pwd: password,
  roles: [
    { role: "readWrite", db: "auth-db" },
    { role: "dbAdmin", db: "auth-db" }
  ]
});

// Initialize file_metadata_db for Knowledge Base
db = db.getSiblingDB("file_metadata_db");
db.createUser({
  user: username,
  pwd: password,
  roles: [
    { role: "readWrite", db: "file_metadata_db" },
    { role: "dbAdmin", db: "file_metadata_db" }
  ]
});

// Initialize file_storage_db for Knowledge Base
db = db.getSiblingDB("file_storage_db");
db.createUser({
  user: username,
  pwd: password,
  roles: [
    { role: "readWrite", db: "file_storage_db" },
    { role: "dbAdmin", db: "file_storage_db" }
  ]
});
