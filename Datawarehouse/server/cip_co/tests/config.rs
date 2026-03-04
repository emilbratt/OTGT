#![allow(unused)]

use cip_co::load_config;

#[test]
fn config() {
    let config = load_config();
    if let Some(ref d) = config.retail_db {
        println!("{:?}", d);
    } else {
        println!("retail db config missing");
    }

    // verify values exist..
    assert!(!config.port.is_empty());
    assert!(!config.host.is_empty());
}
