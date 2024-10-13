use pyo3::prelude::*;
use pyo3::exceptions::PyIOError;
use serde_json::Value;
use tokio::process::Command;
use super::schemas::VideoInfo;

#[pyfunction]
pub fn get_video_info(py: Python<'_>, url: String) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let output = Command::new("yt-dlp")
            .arg("--skip-download")
            .arg("--dump-json")
            .arg(url)
            .output()
            .await
            .unwrap();

        if output.status.success() {
            let json_info: Value = serde_json::from_slice(output.stdout.as_slice()).unwrap();
            let video_info = VideoInfo::new(json_info);
            Ok(video_info)
        } else {
            Err(PyErr::new::<PyIOError, _>("Wrong url"))
        }
    })
}

#[pyfunction]
pub fn download_audio(py: Python<'_>, url: String, name: String) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let _ = Command::new("yt-dlp")
            .arg("-f")
            .arg("bestaudio")
            .arg("-o")
            .arg(format!("{}.m4a", name))
            .arg(url)
            .output()
            .await
            .unwrap();

        Ok(())
    })
}
