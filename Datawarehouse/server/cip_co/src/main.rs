#![allow(unused)]

use cip_co::load_config;

use axum::{
    routing::get,
    Router,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = load_config();

    let db = if config.retail_db.is_none() {
        // this is probably when running dev-environment
        ()
    } else {
        // this is probably when running prod-environment
        let db = cip_co::retail_db::connect();
        match db {
            Ok(db) => (),
            Err(e) => panic!("{e:?}"),
        }
    };

    Ok(())
}

async fn start() {
    // serve webpage
}
