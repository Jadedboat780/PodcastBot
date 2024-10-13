mod async_mod;
mod models;
mod sync_mod;

use models::VideoInfo;
use pyo3::prelude::*;

#[pymodule]
fn audio_lib(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<VideoInfo>()?;

    m.add_function(wrap_pyfunction!(sync_mod::get_video_info, m)?)?;
    m.add_function(wrap_pyfunction!(sync_mod::download_audio, m)?)?;

    async_module(py, m)?;

    Ok(())
}

fn async_module(py: Python<'_>, audio_lib: &PyModule) -> PyResult<()> {
    let m = PyModule::new(py, "asyncio")?;
    m.add_function(wrap_pyfunction!(async_mod::get_video_info, m)?)?;
    m.add_function(wrap_pyfunction!(async_mod::download_audio, m)?)?;
    audio_lib.add_submodule(m)?;
    Ok(())
}
