# canyon-scraper-lambda

This is a very basic implementation of Python scraper lambda which checks when new stock will be available for a certain model of bicycle on the Belgian website of Canyon. It uses AWS EventBridge to trigger a Lambda (1 minute interval). When the stock is not sold out anymore I will receive an e-mail.

### Build Layer
```
$ docker run --rm \
--volume=$(pwd):/lambda-build \
-w=/lambda-build \
lambci/lambda:build-python3.8 \
pip install -r requirements.txt --target python

$ zip -vr python.zip python/

$ aws s3 cp python.zip s3://xxx/python.zip
```

### Build app
```
sam build -t template.yaml --use-container
sam package --template-file template.yaml --s3-bucket yyy --output-template-file template-out.yaml
sam deploy --template-file ./template-out.yaml --stack-name canyon-scraper --capabilities CAPABILITY_NAMED_IAM
```