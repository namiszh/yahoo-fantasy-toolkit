# Yahoo Fanstasy Basketball Analysis and Visualization #

I have been a heavy gamer of yahoo fantasy basketball since 2007. There are also many tools about (Yahoo/Espn) fantasy basketball on GitHub. Now I'm going to develop my own tools taking the opportunity of learning python and web programing.

## Retrieve Data ##

**The first question is how to retrieve data from yahoo?**

At first, my only idea is to use selenium to scrape data from yahoo fantasy basketball website. It's **painfull** because I need to retrieve lots of data thus I need to redirect to many diffrent pages. Thus the work has been suspended for several months.

Once by chance, I find Yahoo provides [API](https://developer.yahoo.com/fantasysports/guide/) for developers. 
That's brilliant! ! ! Yahoo API is absolutely much better, because it's more stable and efficient.

## Create Yahoo APP ##

**The second question is how to use Yahoo API?**

To use Yahoo API, you first need to create a [Yahoo APP](https://developer.yahoo.com/apps/).


![alt text](https://github.com/namiszh/fba/blob/master/docs/images/create_yahoo_app.PNG "Create Yahoo APP")


If you select 'Web Application' in Application Type, a Callback Domain is required. However, localhost or 127.0.0.1 is not allowed.
But we do need to develop our app locally. The solution is to use **ngrok**.

Now ngrok only provides __random__ domain for Free Plan. What I do here is to start ngrok first, then a random domain is generated.

![alt text](https://github.com/namiszh/fba/blob/master/docs/images/ngrok.png "ngrok domain")

Then I will use this domain to create yahoo APP. The ngrok session is always kept running during my development process.

If I need to restart my computer one day, then I will start the ngrok again, and then create another yahoo app. After all, deleting and creating a Yahoo APP is very simple.
