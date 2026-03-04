#![allow(unused)]

use cip_co::CONFIG;

#[test]
fn config() {
    // verify values exist..
    assert!(!CONFIG.port.is_empty());
    assert!(!CONFIG.address.is_empty());
    assert!(!CONFIG.retail_db_user.is_empty());
    assert!(!CONFIG.retail_db_pwd.is_empty());
    assert!(CONFIG.use_dummy_data || !CONFIG.use_dummy_data);
}
