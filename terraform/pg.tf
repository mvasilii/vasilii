# PostgreSQL service
resource "aiven_pg" "samplepg" {
  project                 = var.project_name
  cloud_name              = "google-europe-west4"
  plan                    = "startup-4"
  service_name            = "pg-vasilii-terra"
  maintenance_window_dow  = "monday"
  maintenance_window_time = "12:00:00"
  pg_user_config {
    pg {
      idle_in_transaction_session_timeout = 900
    }
  }
}

# PostgreSQL database
resource "aiven_pg_database" "sample_db" {
  project       = var.project_name
  service_name  = "pg-vasilii-terra"
  database_name = "sample_db"

  depends_on = [
    aiven_pg.samplepg,
  ]
}

# PostgreSQL user
resource "aiven_pg_user" "vasilii" {
  project      = var.project_name
  service_name = aiven_pg.samplepg.service_name
  username     = "vasilii"
}

resource "aiven_pg_user" "test_user" {
  project      = var.project_name
  service_name = aiven_pg.samplepg.service_name
  username     = "test_user"
}

# PostgreSQL connection pool
resource "aiven_connection_pool" "sample_pool" {
  project       = var.project_name
  service_name  = aiven_pg.samplepg.service_name
  database_name = aiven_pg_database.sample_db.database_name
  pool_name     = "samplepool"
  username      = aiven_pg_user.vasilii.username

  depends_on = [
    aiven_pg_database.sample_db,
  ]
}