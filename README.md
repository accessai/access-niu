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
python -m access_niu.train --template sample/colors/template.yml
```

## Inference
```bash
python -m access_niu --projects output
```
Now use this curl command to parse
```bash
curl -X POST \
  http://localhost:8000/parse \
  -F data=@samples/colors/train/red/1.jpg
```

## Docker

###Build image
 - clone the git repo
```bash
git clone https://github.com/accessai/access-niu.git
```
- Build the docker image
```bash
docker build -t access-niu:latest .
```
- Run the docker container.

  Note: You can attach a directory as a volume so that you can supply the templates from outside the docker container.
```bash
# we will use it as root directory for access-niu application
mkdir accessai
# copy samples folder
cp -r samples accessai/

# train the model
docker run -v $(pwd)/accessai:/accessai access-niu python -m access_niu.train --template samples/colors/template.yml
```
After running the train command you should get an output folder in the accessai directory

Now start the access_niu server
```bash
docker -d run -v $(pwd)/accessai:/accessai -p 8000:8000 access-niu --projects output
```

Now use this curl command to parse
```bash
curl -X POST \
  http://localhost:8000/parse \
  -F data=@samples/colors/train/red/1.jpg
```

## References
- This project is inspired from [RASA-NLU](https://github.com/RasaHQ/rasa) project.
