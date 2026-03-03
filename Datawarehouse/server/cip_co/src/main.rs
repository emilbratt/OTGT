#![allow(unused)]

use once_cell::sync::Lazy;

use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub port: String,
    pub address: String,
    pub retail_db_user: String,
    pub retail_db_pwd: String,
    pub use_dummy_data: bool,
}

pub static CONFIG: Lazy<Config> = Lazy::new(|| {
    let content = std::fs::read_to_string("config.toml")
        .expect("Failed to read config.toml");

    toml::from_str(&content)
        .expect("Invalid config format")
});

use axum::{
    routing::get,
    Router,
};

mod retail_db;

fn main() {
    let db = if CONFIG.use_dummy_data {
        ()
    } else {
        let db = retail_db::connect(&CONFIG);
        match db {
            Ok(db) => (),
            Err(e) => panic!("{e:?}"),
        }
    };
}

async fn start() {
    // serve webpage
}
