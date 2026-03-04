#![allow(unused)]

use cip_co::load_config;

#[test]
fn config() {
    let config = load_config();
    println!("{:?}", config);

    // verify values exist..
    assert!(!config.port.is_empty());
    assert!(!config.host.is_empty());
}
