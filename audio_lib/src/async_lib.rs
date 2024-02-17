pub mod async_mod {
    use pyo3::pyfunction;
    use pyo3::prelude::{PyResult, PyErr, Python, PyAny};
    use pyo3::exceptions::{PyIOError, PySystemError};
    use tokio::process::Command as TokioCommand;

    #[pyfunction]
    pub fn is_streaming(py: Python<'_>, url: String) -> PyResult<&PyAny> {
        pyo3_asyncio::tokio::future_into_py(py, async {
            //Проверка на что ведёт url: стрим или видео
            let output = TokioCommand::new("yt-dlp")
                .arg("--skip-download")
                .arg("--dump-json")
                .arg(url)
                .output()
                .await
                .expect("Wrong yt_dlp command");

            let is_stream = if output.status.success() {
                let is_stream: bool = String::from_utf8(output.stdout)
                    .expect("String is not utf-8")
                    .contains(" \"is_live\": true");
                Ok(is_stream)
            } else {
                Err(PyErr::new::<PyIOError, _>("Неправильный url"))
            };

            Python::with_gil(|_py| -> PyResult<bool>{
                is_stream
            })
        })
    }

    #[pyfunction]
    pub fn download_audio(py: Python<'_>, url: String, name: String) -> PyResult<&PyAny> {
        //Скачивает аудио дорожку по url в формате .opus
        pyo3_asyncio::tokio::future_into_py(py, async {
            let yt_download = TokioCommand::new("yt-dlp")
                .arg("-x")
                .arg("--audio-format")
                .arg("opus")
                .arg("-o")
                .arg(name)
                .arg(url)
                .output()
                .await
                .expect("Wrong url");

            Python::with_gil(|_py| -> PyResult<()>{
                if yt_download.status.success() {
                    Ok(())
                } else {
                    Err(PyErr::new::<PyIOError, _>(yt_download.stderr))
                }
            })
        })
    }

    #[pyfunction]
    pub fn audio_separation(py: Python<'_>, name: String, minute: usize) -> PyResult<&PyAny> {
        //Делит аудио файл на части по 55 минут + удаляет исходное аудио

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let audio_duration: usize = 60 * minute; // количество минут минут

            let output = TokioCommand::new("ffmpeg")
                .arg("-i")
                .arg(format!("{}.opus", name))
                .arg("-f")
                .arg("segment")
                .arg("-segment_time")
                .arg(audio_duration.to_string())
                .arg("-c")
                .arg("copy")
                .arg("-reset_timestamps")
                .arg("1")
                .arg(format!("audio/{}/{}_%d.opus", name, name))
                .output()
                .await
                .expect("Failed to execute ffmpeg");

            Python::with_gil(|_py| -> PyResult<()> {
                if output.status.success(){
                    Ok(())
                }
                else {
                    Err(PyErr::new::<PySystemError, _>(output.stderr))
                }
            })
        })
    }
}
