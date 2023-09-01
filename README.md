# rss-feed-reader-aws-lambda
Python lambda function for storing rss feed into a dynamoDB database.

### Prequisits 
* Have Python 3 and the AWS CLI installed locally.
* Log in into your account with the AWS CLI.
* Create at least one dynamoDB table for storing the feed.

### Getting Started
* Add your feeds in the event.json file. As table_name add your dynamoDB table name
* It's possible to define different database tables for different feeds. 
* Call `make create` for publishing the lambda function to aws
* For updates call `make clean` and `make update`.
