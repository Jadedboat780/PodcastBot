pub mod async_mod {
    use tokio::process::Command as TokioCommand;
    use pyo3::prelude::*;

    async fn is_streaming(url: &str) -> bool {
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

        return is_steramimg;
    }

    #[pyo3_asyncio::tokio::main]
    pub async fn download_audio() -> Result<(), Vec<u8>> {
        let url: &str = "";
        let name: &str = "";

        // Скачивает аудио дорожку видео в формате opus
        if is_streaming(url).await {
            panic!("This is stream")
        }

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


        if yt_download.status.success() {
            Ok(())
        } else {
            Err(yt_download.stderr)
        }
    }
}