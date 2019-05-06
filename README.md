[![Build Status](https://travis-ci.org/accessai/access-niu.svg?branch=master)](https://travis-ci.org/accessai/access-niu)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
# access-niu
This repository contains application to train models for Image classification and Regression tasks.

## Tasks
- [x] Create a basic app for training and inference
- [ ] Support for training regression models
- [ ] Support of training multi input/output models
- [ ] Incorporate Bayesian Inference for finding uncertainty in the predictions.
- [x] Create Docker Image
- [ ] Support for serving the application with gunicorn
- [ ] Anything else? 

## Installation
```bash
pip install access-niu
```

## Training
```bash
python -m access_niu.train --template access_niu/sample/colors/sample_template.yml
```
Docker:
```bash
docker exec {CONTAINER} python -m access_niu.wsgi --project /access-ui/access_ui/sample_project
```

## Inference
```bash
python -m access_niu.wsgi --project ./output/colors
```
Now use this curl command to parse
```bash
curl -X POST \
  http://localhost:8000/parse \
  -F data=@test_image.jpg
```
Docker:
```bash
docker exec {CONTAINER} python -m access_niu.train --template /access-niu/access_niu/sample/sample_template.yml
```
Now use this curl command to parse
```bash
docker exec {CONTAINER} curl -X POST \
  http://localhost:8000/parse \
  -F data=@image_leisure_0.jpg
```

## References
- This project is inspired from [RASA-NLU](https://github.com/RasaHQ/rasa) project.
