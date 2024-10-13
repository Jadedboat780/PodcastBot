use pyo3::exceptions::PyIOError;
use pyo3::prelude::*;
use serde_json::Value;
use std::process::Command;
use super::schemas::VideoInfo;

#[pyfunction]
pub fn get_video_info(url: &str) -> PyResult<VideoInfo> {
    let output = Command::new("yt-dlp")
        .arg("--skip-download")
        .arg("--dump-json")
        .arg(url)
        .output()
        .unwrap();

    if output.status.success() {
        let json_info: Value = serde_json::from_slice(output.stdout.as_slice()).unwrap();
        let video_info = VideoInfo::new(json_info);
        Ok(video_info)
    } else {
        Err(PyErr::new::<PyIOError, _>("Wrong url"))
    }
}

#[pyfunction]
pub fn download_audio(url: &str, name: &str) -> PyResult<()> {
    let _ = Command::new("yt-dlp")
        .arg("-f")
        .arg("bestaudio")
        .arg("-o")
        .arg(format!("{}.m4a", name))
        .arg(url)
        .output()
        .unwrap();

    Ok(())
}
