#![allow(unused)]

use cip_co::CONFIG;

use axum::{
    routing::get,
    Router,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", CONFIG.port);

    let db = if CONFIG.use_dummy_data {
        ()
    } else {
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
