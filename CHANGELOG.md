## Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project aims to follow [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2026-02-16

### Added
- Advanced README with detailed architecture, ML pipeline, charts and roadmap.
- MIT license and explicit contributor credit for @pyzit.
- `artifacts/` directory for model files (`model_lstm.h5`, `tokenizer.pkl`, `mlb.pkl`).

### Changed
- Refactored Flask app into modular `hashtag_predictor` package with clear separation of routes and prediction logic.
- Updated Python runtime requirement to 3.9.25 and aligned toolchain configuration.
- Improved project structure documentation and local development instructions.

---

## [1.0.0] - Initial release

### Added
- Core LSTM model for hashtag prediction.
- Trained tokenizer and MultiLabelBinarizer artifacts.
- Basic Flask application and HTML template for predicting hashtags from a tweet.

