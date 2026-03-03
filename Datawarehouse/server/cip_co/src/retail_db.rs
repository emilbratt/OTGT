use crate::CONFIG;

pub fn connect() -> Result<(), std::io::Error> {
    let cnf = &CONFIG;

    let kind = std::io::ErrorKind::NotFound;
    let error = std::fmt::Error;
    let err = std::io::Error::new(kind, error);

    Err(err)
}
