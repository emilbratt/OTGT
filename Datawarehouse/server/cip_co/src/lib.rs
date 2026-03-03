#![allow(unused)]

use std::sync::LazyLock;

use serde::Deserialize;

pub mod retail_db;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub port: String,
    pub address: String,
    pub retail_db_user: String,
    pub retail_db_pwd: String,
    pub use_dummy_data: bool,
}

pub static CONFIG: LazyLock<Config> = LazyLock::new(|| {
    let content = std::fs::read_to_string("config.toml")
        .expect("Failed to read config.toml");

    toml::from_str(&content)
        .expect("Invalid config format")
});
