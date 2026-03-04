#![allow(unused)]

use std::sync::LazyLock;
use std::path::Path;
use serde::Deserialize;
use toml::Table;

pub mod retail_db;

#[derive(Debug, Deserialize)]
pub struct RetailDB {
    pub db_host: String,
    pub db_port: String,
    pub db_name: String,
    pub db_user: String,
    pub db_password: String,
}

#[derive(Debug, Deserialize)]
pub struct Config {
    pub port: String,
    pub host: String,
    pub retail_db: Option<RetailDB>,
}

static CONFIG: LazyLock<Config> = LazyLock::new(|| {
    let rel_proj = Path::new("../../../environment.ini"); // relative to cip_co project
    let repo_root = Path::new("environment.ini"); // relative to repository root

    let env = if rel_proj.exists() {
        rel_proj
    } else if repo_root.exists() {
        rel_proj
    } else {
        panic!("No environment file found")
    };

    let mut content = std::fs::read_to_string(env)
        .expect(env.to_str().unwrap())
        .replace(';', "#"); // TODO: double check if "replace()" conflicts with actual values inside config file..

    let table: Table = toml::from_str(&content)
        .expect("Invalid config format");

    let datawarehouse = &table["datawarehouse"];

    let retail_db = match table.get("retail") {
        Some(d) => {
            let mut missing = false;
            for k in ["db_host", "db_port", "db_name", "db_user", "db_password"] {
                if d[k].as_str().unwrap() == "INSERT" {
                    missing = true;
                }
            }
            if missing {
                None
            } else {
                let retail_db_conf = RetailDB {
                    db_host: d["db_host"].to_string(),
                    db_port: d["db_port"].to_string(),
                    db_name: d["db_name"].to_string(),
                    db_user: d["db_user"].to_string(),
                    db_password: d["db_password"].to_string(),
                };

                Some(retail_db_conf)
            }
        }
        None => None
    };

    Config {
        port: datawarehouse["cip_co_port"].to_string(),
        host: datawarehouse["cip_co_host"].to_string(),
        retail_db,
    }
});

pub fn load_config() -> &'static Config {
    &CONFIG
}
