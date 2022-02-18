import random
import discord
import finvizfinance
from finvizfinance.news import News
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.screener.overview import Overview
import pandas as pd
import finnhub
TOKEN = ''  # Enter your Discord Bot Token Here

client = discord.Client()

finnhub_client = finnhub.Client(api_key='') #finnhub API



@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return


    if message.content.startswith('!commandlist'): #List of commands
        await message.channel.send('COMMANDS\nGrab Chart - !chart {ticker} {timeframe\nInsider Info - !insider {latest or top week}\nSee Fundamentals - !fundamentals {ticker}\nNews - !pr {ticker}\nSympathy - !symp {ticker}')

    if message.content.startswith('!chart'): #Grab Chart of any ticker
        user = message.content.split(' ')[1]
        user_t = message.content.split(' ')[2]
        stock = finvizfinance(user)
        chart = stock.ticker_charts(timeframe=f'{user_t}')
        await message.channel.send(chart)

    if message.content.startswith('!insider latest'):#latest insider info


        inside_info = Insider(option='latest')
        output = inside_info.get_insider()
        await message.channel.send(output)

    if message.content == ('!insider top week'): #top insider trades of the week

        top_owner_trade = Insider(option='top week')
        top = top_owner_trade.get_insider()
        await message.channel.send(top)

    if message.content.startswith('!fundamentals'): #Grab most fundamentals from specified ticker
        ticker = message.content.split(' ')[1]
        ticker_choice = finvizfinance(f'{ticker}')
        funda = ticker_choice.ticker_fundament()
        for index, (key, value) in enumerate(funda.items()):
            await message.channel.send(f'{key}: {value}')

    if message.content.startswith('!desc'): #Written description of what the specified company does
        grab = message.content.split(' ')[1]
        grab_choice = finvizfinance(f'{grab}')
        desc = grab_choice.ticker_description()
        await message.channel.send(desc)

    if message.content.startswith('!pr'):#News on specific ticker
        keyword = message.content.split(' ')[1]
        grab_ticker = finvizfinance(f'{keyword}')
        news = grab_ticker.ticker_news()
        await message.channel.send(news[0:5].to_string())
        turn_to_dict = news.set_index('Title').T.to_dict('list')
        #for value in enumerate(turn_to_dict.items()):
            #await message.channel.send(f'Link: {value}')

        #await message.channel.send(news[0:5].to_string())

    if message.content.startswith('!symp'): #Stocks that are simillar to the specified ticker
        word = message.content.split(' ')[1]
        symp = finnhub_client.company_peers(f'{word}')
        await message.channel.send(str(symp))


client.run(TOKEN)

