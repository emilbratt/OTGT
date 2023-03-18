-- DOWNLOADED ELSPOT DATA FROM NORDPOOL
CREATE TABLE IF NOT EXISTS elspot_raw (
  elspot_date TEXT NOT NULL PRIMARY KEY,
  elspot_data JSON NOT NULL
);

-- HOLDS THE USER CONFIGURED CONTROL-PLANS FOR SETTING THE STATE OF IoT-DEVICES
CREATE TABLE IF NOT EXISTS control_plans (
  plan_name    TEXT NOT NULL PRIMARY KEY,
  plan_data    TEXT NOT NULL, -- HOLDS RAW YAML STRING
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- STORE FUTURE (GENERATED) AND PAST (HISTORY) STATE VALUES
CREATE TABLE IF NOT EXISTS state_schedule (
  plan_name       TEXT NOT NULL,
  device_type     TEXT NOT NULL, -- switch | message | percent ..
  state_value     TEXT NOT NULL, -- ON | OFF | HIGH | LOW | 50% | 10c | 3kW/h ...
  state_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  UNIQUE (plan_name, device_type, state_value, state_timestamp)
);
