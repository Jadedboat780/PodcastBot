pub mod sync_mod {
    use std::thread;
    use std::process::{Command, Output};
    use std::fs::{create_dir, remove_file};
    use pyo3::prelude::*;
    use pyo3::exceptions::{PyFileExistsError, PyIOError, PySystemError, PyValueError};


    #[pyfunction]
    pub fn yt_dlp(url: String, name: String) -> PyResult<bool> {
        let thr = thread::spawn(move || -> PyResult<bool>
            {
                let download_result: PyResult<()> = download_audio(&url, &name);

                let result = match download_result {
                    Err(pyerr) => Err(pyerr),

                    Ok(()) => match create_dir(format!("audio/{}", name)) {
                        Ok(_) => {
                            audio_separation(&name).expect("Error");
                            return Ok(true);
                        }
                        Err(err) => return Err(PyErr::new::<PyFileExistsError, _>(err.to_string())),
                    },
                };

                return result;
            });

        let res = thr.join().expect("Thread error");
        return res;
    }

    fn is_streaming(url: &str) -> bool {
        //Проверка на что ведёт url: стрим или видео
        let output: Output = Command::new("yt-dlp")
            .arg("--skip-download")
            .arg("--dump-json")
            .arg(url)
            .output()
            .expect("Wrong url");

        let is_steramimg: bool = String::from_utf8(output.stdout)
            .expect("")
            .contains(" \"is_live\": true");

        return is_steramimg;
    }

    #[pyfunction]
    pub fn download_audio(url: &str, name: &str) -> PyResult<()> {
        if is_streaming(url) {
            return Err(PyErr::new::<PyIOError, _>("Нельзя отправлять ссылки на стрим"));
        }

        let yt_download = Command::new("yt-dlp")
            .arg("-x")
            .arg("--audio-format")
            .arg("opus")
            .arg("-o")
            .arg(name)
            .arg(url)
            .output()
            .expect("Video not download");

        if yt_download.status.success() {
            Ok(())
        } else {
            Err(PyErr::new::<PyValueError, _>(yt_download.stderr))
        }
    }

    #[pyfunction]
    pub fn audio_separation(name: &str) -> PyResult<()> {
        //Делит аудио файл на части по 60 минут + удаляет исходное аудио
        let audio_duration: i32 = 60 * 55; // 55 минут

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
            remove_file(format!("{}.opus", name)).expect("Failed to delete file");
            Ok(())
        } else {
            Err(PyErr::new::<PySystemError, _>(output.stderr))
        }
    }
}