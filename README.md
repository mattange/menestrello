# menestrello

Menestrello is a Python project designed to provide [brief description of the project functionality]. 

## Installation

To install the project, you can use Poetry. First, ensure you have Poetry installed, then run:

```bash
poetry install
```

## Dependencies on Raspberri Pi

This project depends on an audio backend to be able to play audio. GStreamer or FFMpeg.
The backends supported are the ones supported by the playsound3 library.
[Check Pypi at this page.](https://pypi.org/project/playsound3/)

## Usage

To run the application, use the following command:

```bash
poetry run python -m menestrello.main
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.