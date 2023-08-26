# Yahoo NBA Fantasy Analysis and Visualization

Web application to display yahoo fantasy basketball data analysis result.

**Technology stack**

- Flask Framework - Web Framework
- Bootstrap - Web page display style
- Pandas/matplotlib - Create all kinds of chart
- Yahoo OAuth - Yahoo Authorization
- Yahoo Fantasy API - Read data using Restful API
- Route53 - Register a domain for deployment
- [aws-lambda-web-adapter](https://github.com/awslabs/aws-lambda-web-adapter) - deploy the web application to AWS

## For Users

goto https://fba.laowang.org (not ready yet) and try it

**Demo**

   ![Demo](/flask-web-app/docs/demo.gif)

## For Developers

### Prerequisites

1. have python installed

1. create an application in Yahoo developer https://developer.yahoo.com/apps/
   ![Create Yahoo Application](/flask-web-app/docs/create_yahoo_applicaton.PNG)
   - Homepage URL: The url you plan to deploy your website to
   - Redirect URI(s): Besides the deployed url, also add https://127.0.0.1:5000/callback for your local deployment. 
     
     Please Note: you can only add http**s**, not http, so when you run locally, you also need to run it with https.
   - OAuth Client Type: Choose 'Confidential Client' 
   - API Permissions: Fantasy Sports - Read

   Then note down the client id and client secret, we will use it later.
### Hwo to run it locally


1. create a virtual enviroment 
   `python -m venv .\venv`

1. Activate the virtual environment
   `.\venv\Scripts\activate.bat`  (Windows)

   Then it will show something like this
   > (venv) D:\personal\project\yfb\flask-web-app>

1. set pip version (the latest version may have problem in install )

   `python -m pip install pip==21.3.1`

1. install dependency
   `pip install -r requirements.txt`

1. create a credential file in the root folder. Put the *Client ID (Consumer Key)* in the first line, and *Client Secret (Consumer Secret)* in the second line.
   ![Yahoo Application credential](/flask-web-app/docs/credentaial.png)

1. run the application
   `flask run --cert=.\cert\cert.pem --key=.\cert\key.pem --debugger`

### Deployment

Try to deploy to AWS using 
