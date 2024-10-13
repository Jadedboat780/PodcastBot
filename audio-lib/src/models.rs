use pyo3::prelude::{pyclass, pymethods};
use serde_json::Value;

#[derive(Debug)]
#[pyclass]
pub struct VideoInfo {
    #[pyo3(get)]
    id: String,
    #[pyo3(get)]
    title: String,
    #[pyo3(get)]
    duration: Option<u64>,
    #[pyo3(get)]
    is_live: bool,
}

impl VideoInfo {
    pub fn new(info: Value) -> Self {
        let id = info.get("id").unwrap().to_string().replace("\"", "");
        let title = info.get("fulltitle").unwrap().to_string().replace("\"", "");
        let duration = match info.get("duration") {
            Some(sec) => Some(sec.as_u64().unwrap()),
            None => None,
        };
        let is_live = info.get("is_live").unwrap().as_bool().unwrap();

        VideoInfo {
            id,
            title,
            duration,
            is_live,
        }
    }
}

#[pymethods]
impl VideoInfo {
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}
