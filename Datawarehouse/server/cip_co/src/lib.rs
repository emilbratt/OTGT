#![allow(unused)]

use std::sync::LazyLock;
use std::path::Path;
use toml::Table;

pub mod retail_db;

#[derive(Debug)]
pub struct RetailDB {
    pub db_host: String,
    pub db_port: String,
    pub db_name: String,
    pub db_user: String,
    pub db_password: String,
}

#[derive(Debug)]
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

    let mut port = datawarehouse["cip_co_port"].as_str().unwrap().to_string();
    let mut host = datawarehouse["cip_co_host"].as_str().unwrap().to_string();

    let retail_db = match table.get("retail") {
        Some(d) => {
            let db_host = d["db_host"].as_str().unwrap().to_string();
            let db_port = d["db_port"].as_str().unwrap().to_string();
            let db_name = d["db_name"].as_str().unwrap().to_string();
            let db_user = d["db_user"].as_str().unwrap().to_string();
            let db_password = d["db_password"].as_str().unwrap().to_string();

            let retail_db_conf = RetailDB {
                db_host,
                db_port,
                db_name,
                db_user,
                db_password,
            };

            let missing = [
                &retail_db_conf.db_host,
                &retail_db_conf.db_port,
                &retail_db_conf.db_name,
                &retail_db_conf.db_user,
                &retail_db_conf.db_password,
            ].iter().any(|s| *s == "INSERT");

            if missing {
                None
            } else {
                Some(retail_db_conf)
            }
        }
        None => None
    };

    Config {
        port,
        host,
        retail_db,
    }
});

pub fn load_config() -> &'static Config {
    &CONFIG
}
