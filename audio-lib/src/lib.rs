mod sync_lib;
mod async_lib;

use sync_lib::sync_mod;
use async_lib::async_mod;
use pyo3::prelude::*;


#[pymodule]
fn audio_lib(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    mod_sync(py, m)?;
    mod_async(py, m)?;
    Ok(())
}

fn mod_sync(py: Python<'_>, audio_lib: &PyModule) -> PyResult<()> {
    let m = PyModule::new(py, "sync_mod")?;
    m.add_function(wrap_pyfunction!(sync_mod::download_audio, m)?)?;
    m.add_function(wrap_pyfunction!(sync_mod::audio_separation, m)?)?;
    m.add_function(wrap_pyfunction!(sync_mod::yt_dlp, m)?)?;
    audio_lib.add_submodule(m)?;
    Ok(())
}

fn mod_async(py: Python<'_>, audio_lib: &PyModule) -> PyResult<()> {
    let m = PyModule::new(py, "async_mod")?;
    m.add_function(wrap_pyfunction!(async_mod::download_audio, m)?)?;
    audio_lib.add_submodule(m)?;
    Ok(())
}