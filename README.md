# Кузница Звука

<p align="center">
  <a href="https://github.com/dumuzeyn/Sonic-Forge/blob/main/dist/SonicForge.exe">
    <img src="https://img.shields.io/badge/Скачать_APK-Кцзница--Звука.apk-black?style=for-the-badge" alt="Скачать APK">
  </a>
</p>

[English version](#loleng)

Кузница Звука - настольное приложение для подготовки музыкальных файлов. Оно нормализует громкость, обновляет метаданные, создает обложки и сохраняет готовые файлы в выбранную папку только после успешного завершения всех этапов.

## Что умеет приложение

- Обрабатывает один аудиофайл или всю папку с песнями.
- Нормализует громкость через FFmpeg loudnorm.
- Может мягко снижать фоновый шум.
- Записывает название и жанр в метаданные.
- Может принудительно заменить существующий жанр.
- Создает обложку в одном из четырех режимов: `ocean`, `plasma`, `fusion`, `aurora`.
- Может встроить созданную обложку в MP3-файл.
- Работает через графический интерфейс на русском и английском языках.

## Скачать и запустить

Готовая сборка содержит FFmpeg и FFprobe внутри. Для обычного запуска достаточно скачать один файл:

[Скачать SonicForge.exe](https://github.com/dumuzeyn/Sonic-Forge/blob/main/dist/SonicForge.exe)

Запуск из PowerShell:

```powershell
.\dist\SonicForge.exe
```

Если `.exe` еще не собран, соберите его командой:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name SonicForge --icon ".\assets\sonic_forge_mark.ico" --add-data "Normalize-Music.py;." --add-data "assets\sonic_forge_mark.ico;assets" --add-data "assets\sonic_forge_mark.png;assets" --add-binary "C:\ffmpeg\bin\ffmpeg.exe;ffmpeg" --add-binary "C:\ffmpeg\bin\ffprobe.exe;ffmpeg" music_polisher_gui.py
```

## Основные настройки

- **Источник** - один аудиофайл или папка с песнями.
- **Папка назначения** - место, куда попадут готовые файлы. Во время обработки папка не изменяется.
- **Жанр** - жанр, который будет записан в метаданные. Если поле пустое, приложение попробует определить жанр автоматически.
- **Исполнитель, альбом, исполнитель альбома, композитор, год, номер трека, комментарий** - дополнительные метаданные. Если поле пустое, оно остается пустым.
- **Заменить существующий жанр** - принудительно заменяет жанр, который уже есть в файле.
- **Средняя громкость LUFS** - целевая средняя громкость трека.
- **Пиковый предел** - максимальный пик громкости после обработки.
- **Диапазон громкости** - степень сохранения динамики трека.
- **Финальное усиление** - дополнительное усиление после нормализации.
- **Шумоподавление** - мягкое снижение фонового шума.
- **Лимитер** - защита от перегруза после усиления.
- **Цветовая схема** - стиль обложки: `ocean`, `plasma`, `fusion`, `aurora`.
- **Seed** - число для повторяемой генерации обложек.
- **Не менять обложку** - пропускает создание и встраивание новой обложки.
- **Файл приложения** - `SonicForge.exe` уже содержит FFmpeg и FFprobe, поэтому отдельная установка FFmpeg для обычного запуска не требуется.

## Консольный запуск

Одна песня:

```powershell
python .\easy_music_process.py --source "C:\Music\Input\song.mp3" --output "C:\Music\Output" --color-mode plasma
```

Папка с песнями:

```powershell
python .\easy_music_process.py --source "C:\Music\Input" --output "C:\Music\Output" --color-mode plasma
```

Папка с песнями и принудительной заменой жанра:

```powershell
python .\easy_music_process.py --source "C:\Music\Input" --output "C:\Music\Output" --genre "Rock" --overwrite-genre --color-mode plasma
```

## Требования

Python-пакеты для запуска из исходников:

```powershell
pip install numpy pillow pyinstaller
```

Для собранного `.exe` FFmpeg устанавливать отдельно не нужно. Он встроен в файл приложения.

>**Автор проекта: Зейналов У.Р.о.**
---
<h1 id = loleng>
 Sonic Forge
</h1>

<p align="center">
  <a href="https://github.com/dumuzeyn/Sonic-Forge/blob/main/dist/SonicForge.exe">
    <img src="https://img.shields.io/badge/Download_APK-Sonic--Forge.apk-black?style=for-the-badge" alt="Скачать APK">
  </a>
</p>

Sonic Forge is a desktop application for preparing music files. It normalizes loudness, updates metadata, generates cover art, and publishes finished files to the selected output folder only after every processing step succeeds.

## Features

- Processes a single audio file or a folder of songs.
- Normalizes loudness with FFmpeg loudnorm.
- Can gently reduce background noise.
- Writes title and genre metadata.
- Can force-replace existing genres.
- Generates cover art in one of four modes: `ocean`, `plasma`, `fusion`, `aurora`.
- Can embed generated cover art into MP3 files.
- Provides a graphical interface in Russian and English.

## Download And Launch

The ready build includes FFmpeg and FFprobe. For normal use, downloading one file is enough:

[Download SonicForge.exe](https://github.com/dumuzeyn/Sonic-Forge/blob/main/dist/SonicForge.exe)

PowerShell launch:

```powershell
.\dist\SonicForge.exe
```

If the `.exe` has not been built yet, build it with:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name SonicForge --icon ".\assets\sonic_forge_mark.ico" --add-data "Normalize-Music.py;." --add-data "assets\sonic_forge_mark.ico;assets" --add-data "assets\sonic_forge_mark.png;assets" --add-binary "C:\ffmpeg\bin\ffmpeg.exe;ffmpeg" --add-binary "C:\ffmpeg\bin\ffprobe.exe;ffmpeg" music_polisher_gui.py
```

## Main Settings

- **Source** - one audio file or a folder containing songs.
- **Output folder** - where finished files are published. The folder is not changed while processing is still running.
- **Genre** - genre written to metadata. Leave empty to let the application estimate it.
- **Artist, album, album artist, composer, year, track number, comment** - additional metadata fields. Empty fields remain empty.
- **Overwrite existing genre** - replaces genres already stored in files.
- **Integrated LUFS** - target average loudness.
- **True peak** - maximum loudness peak after processing.
- **Loudness range** - how much dynamic range should be preserved.
- **Final gain** - additional gain after normalization.
- **Denoise** - gentle background-noise reduction.
- **Limiter** - protection from overload after gain.
- **Color mode** - cover style: `ocean`, `plasma`, `fusion`, `aurora`.
- **Seed** - integer for repeatable cover generation.
- **Do not change cover** - skips generating and embedding new cover art.
- **Application file** - `SonicForge.exe` already includes FFmpeg and FFprobe, so a separate FFmpeg installation is not required for normal use.

## Console Usage

Single song:

```powershell
python .\easy_music_process.py --source "C:\Music\Input\song.mp3" --output "C:\Music\Output" --color-mode plasma
```

Folder:

```powershell
python .\easy_music_process.py --source "C:\Music\Input" --output "C:\Music\Output" --color-mode plasma
```

Folder with forced genre replacement:

```powershell
python .\easy_music_process.py --source "C:\Music\Input" --output "C:\Music\Output" --genre "Rock" --overwrite-genre --color-mode plasma
```

## Requirements

Python packages for source runs:

```powershell
pip install numpy pillow pyinstaller
```

The built `.exe` does not require a separate FFmpeg installation. FFmpeg is bundled into the application file.

>**Author of project: Zeynalov U.R.o.**