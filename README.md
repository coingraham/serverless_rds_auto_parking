# Serverless RDS Auto Parking Utility
Serverless Implementation of an RDS Auto Parking utility.

## Getting Started

Install the serverless framework [here](https://serverless.com/).  
Clone this repo into your working folder.

## Configuration the project

The default configuration is in region "us-east-1", if you want to change to another region, edit the region serverless.yml file and in the lambda.py file.

## Installation

Run "serverless deploy" to install the project

## What is installed

This project when run as configured will create the following:  
Lambda function -- Cost ~$.0005/day.  
DynamoDB table -- Cost $.59/month.  
RDS instance -- Cost $.017/hr.  

## Configuring Auto Park

Go to the created DynamoDB table "rds_autoparking_config" and find the item for the day of the week you want to update.  Change the "exclude" attribute to "False" and change the "all_day" attribute to either "On", "Off", or "Schedule".  "On" or "Off" will keep your rds instance on or off all day.  Setting to "Schedule" will turn your rds instance on if the current time is in between the start_hour and stop_hour attributes and turn it off if it is outside of those hours.

## Go read the blog article

Check out www.2ndwatch.com/blog/.... (link coming)

## Authors

* **Coin Graham** - *Initial work* - [CoinGraham](https://github.com/CoinGraham)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

