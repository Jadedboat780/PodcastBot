pub mod async_mod {
    use tokio::process::Command as TokioCommand;
    use pyo3::prelude::*;


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
                .expect("Wrong url");

            let is_steramimg: bool = String::from_utf8(output.stdout)
                .expect("")
                .contains(" \"is_live\": true");

            Ok(is_steramimg)
        })
    }


    #[pyfunction]
    pub fn download_audio(py: Python<'_>, url: String, name: String) -> PyResult<&PyAny> {
        pyo3_asyncio::tokio::future_into_py(py, async {
            // Скачивает аудио дорожку видео в формате opus
            // if is_streaming(py, url).await {
            //     panic!("This is stream")
            // }

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

            //
            // if yt_download.status.success() {
            //     Ok(())
            // } else {
            //     Err(yt_download.stderr)
            // }
            Ok(true)

        })
    }
}
