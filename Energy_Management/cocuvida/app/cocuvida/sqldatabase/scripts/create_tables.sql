/*
  - ELSPOT TABLES -
*/
-- RAW ELSPOT DATA FROM NORDPOOL
CREATE TABLE IF NOT EXISTS elspot_raw (
  elspot_date DATETIME NOT NULL PRIMARY KEY, -- iso timestamp 'YYYY-MM-DD'
  elspot_data JSON NOT NULL
);
-- PROCESSED ELSPOT DATA FROM RAW ELSPOT DATA
CREATE TABLE IF NOT EXISTS elspot_processed (
  elspot_date   DATETIME NOT NULL, -- iso timestamp 'YYYY-MM-DD'
  elspot_data   JSON NOT NULL,
  elspot_region TEXT NOT NULL,
  last_updated  INT DEFAULT ( CAST(STRFTIME('%s','now', 'localtime') AS INT) ) NOT NULL, -- Unix Epoch
  UNIQUE (elspot_date, elspot_region)
);
-- PLOT PRICES FOR SPECIFIC DATE FROM PROCESSED ELSPOT DATA
CREATE TABLE IF NOT EXISTS elspot_plot_date (
  plot_date    DATETIME NOT NULL,
  plot_data    TEXT NOT NULL, -- RAW SVG STRING
  plot_region  TEXT NOT NULL,
  last_updated INT DEFAULT ( CAST(STRFTIME('%s','now', 'localtime') AS INT) ) NOT NULL, -- Unix Epoch
  UNIQUE (plot_date, plot_region)
);

/*
  - CONTROL-PLAN TABLES -
*/
-- HOLDS THE USER CONFIGURED CONTROL-PLANS FOR SETTING THE STATE OF IoT-DEVICES
CREATE TABLE IF NOT EXISTS control_plans (
  plan_name    TEXT NOT NULL PRIMARY KEY,
  plan_data    TEXT NOT NULL, -- HOLDS RAW YAML STRING
  last_updated INT DEFAULT ( CAST(STRFTIME('%s','now', 'localtime') AS INT) ) NOT NULL -- Unix Epoch
);
-- STORE FUTURE (GENERATED) AND PAST (HISTORY) STATE VALUES
CREATE TABLE IF NOT EXISTS state_schedule (
  plan_name    TEXT NOT NULL,
  target_type  TEXT NOT NULL, -- shelly | mqtt  ..
  state_value  TEXT NOT NULL, -- ON | OFF | HIGH | LOW | 50% | 10c | 3kW/h ...
  state_time   DATETIME NOT NULL, -- iso timestamp 'YYYY-MM-DD HH:MM'
  state_status INTEGER DEFAULT 0 NOT NULL, -- 0 = not published, 1 = is published, 2 = target disabled, 3 = publish failed
  UNIQUE (plan_name, target_type, state_value, state_time)
);
