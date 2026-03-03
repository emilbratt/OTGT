use crate::Config;

pub fn connect(cnf: &Config) -> Result<(), std::io::Error> {
    let kind = std::io::ErrorKind::NotFound;
    let error = std::fmt::Error;
    let err = std::io::Error::new(kind, error);

    Err(err)
}
