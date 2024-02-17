pub mod sync_mod {
    use pyo3::pyfunction;
    use pyo3::prelude::{PyResult, PyErr};
    use pyo3::exceptions::{PyIOError, PySystemError};
    use std::process::{Command, Output};

    #[pyfunction]
    pub fn is_streaming(url: &str) -> PyResult<bool> {
        //Проверка на что ведёт url: стрим(true) или видео(false)
        let output: Output = Command::new("yt-dlp")
            .arg("--skip-download")
            .arg("--dump-json")
            .arg(url)
            .output()
            .expect("Wrong yt_dlp command");

        let result: Result<bool, PyErr> = if output.status.success() {
            let is_stream: bool = String::from_utf8(output.stdout)
                .expect("String is not utf-8")
                .contains(" \"is_live\": true");

            Ok(is_stream)
        } else {
            Err(PyErr::new::<PyIOError, _>("Неправильный url"))
        };

        return result;
    }

    #[pyfunction]
    pub fn download_audio(url: &str, name: &str) -> PyResult<()> {
        //Скачивает аудио дорожку по url в формате .opus
        let is_stream: PyResult<bool> = is_streaming(url);

        if let Ok(true) = is_stream {
            return Err(PyErr::new::<PyIOError, _>(
                "Нельзя отправлять ссылки на прямую трансляцию",
            ));
        } else if let Err(pyerr) = is_stream {
            return Err(pyerr);
        }

        let _yt_download: Output = Command::new("yt-dlp")
            .arg("-x")
            .arg("--audio-format")
            .arg("opus")
            .arg("-o")
            .arg(name)
            .arg(url)
            .output()
            .expect("Wrong yt_dlp command");

        Ok(())
    }

    #[pyfunction]
    pub fn audio_separation(name: &str, minute: usize) -> PyResult<()> {
        //Делит аудио файл на части по x минут
        let audio_duration: usize = 60 * minute; // количество минут

        let output = Command::new("ffmpeg")
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
            .expect("Failed to execute ffmpeg");

        if output.status.success() {
            Ok(())
        } else {
            Err(PyErr::new::<PySystemError, _>(output.stderr))
        }
    }
}
