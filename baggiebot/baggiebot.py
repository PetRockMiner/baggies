import discord
from discord.ext import commands, tasks
from discord import Intents
from discord import TextChannel
from discord import Embed
from tweeterpy import TweeterPy
from tweeterpy import config
import requests
import configparser
from collections import defaultdict
import re
import asyncio
import time as t
import os

# Load configuration
config = configparser.ConfigParser()
config.read('cumloader.ini')

# Use data from config file
TOKEN = config['DEFAULT']['TOKEN']
YOUTUBE_API_KEY = config['DEFAULT']['YOUTUBE_API_KEY']
USERNAME = config['DEFAULT']['USERNAME']
DISCORD_CHANNEL_ID = int(config['DEFAULT']['DISCORD_CHANNEL_ID'])
ALPHA_VANTAGE_API_KEY = config['DEFAULT']['ALPHA_VANTAGE_API_KEY']
TWITTER_USERNAME = config['DEFAULT']['TWITTER_USERNAME']
TWITTER_PASSWORD = config['DEFAULT']['TWITTER_PASSWORD']
AUDIO_FILES_ENDPOINT = config['DEFAULT']['AUDIO_FILES_ENDPOINT']
MONITOR_USERNAME = config['DEFAULT']['MONITOR_USERNAME']
URL_TO_THUMBNAIL_IMAGE = config['DEFAULT']['URL_TO_THUMBNAIL_IMAGE']
URL_TO_FOOTER_ICON = config['DEFAULT']['URL_TO_FOOTER_ICON']

# Update intents to include member events
intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

config.TIMEOUT = 5
twitter = TweeterPy()

LAST_VIDEO_ID = None  # Store the last video ID


def convert_dynamic_to_playable(dynamic_url):
    master = dynamic_url.replace('/dynamic_playlist.m3u8?type=live',"/master_playlist.m3u8")
    response = requests.get(master)
    data = response.text.split('audio-space/')[1].replace(chr(10), "")
    play_url = dynamic_url.replace('dynamic_playlist.m3u8',data).replace('type=live',"type=replay")
    return play_url

# Helper functions to format the file details
def format_size(size_in_bytes):
    size_in_kb = size_in_bytes / 1024
    if size_in_kb < 1024:
        return f"{size_in_kb:.2f} KB"
    size_in_mb = size_in_kb / 1024
    if size_in_mb < 1024:
        return f"{size_in_mb:.2f} MB"
    size_in_gb = size_in_mb / 1024
    return f"{size_in_gb:.2f} GB"

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

def format_date(date_str):
    from datetime import datetime
    date_obj = datetime.fromisoformat(date_str.rstrip("Z"))
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')

@bot.event
async def on_ready():
    print(f'We have nefariously logged in on a malicious proxy ip as {bot.user} Now we will Flash Crash $AMC and take all the basement dwelling incels money once again! #Wobbed #SFYL')
    check_youtube.start()   

def get_channel_id(username):
    response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=id&type=channel&q={username}&key={YOUTUBE_API_KEY}')
    data = response.json()
    items = data.get("items", [])
    if items:
        return items[0].get("id", {}).get("channelId")
    return None

def get_latest_video(channel_id, max_results=1):
    # Fetch the uploads playlist ID
    channel_data = requests.get(f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={YOUTUBE_API_KEY}').json()
    uploads_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Fetch the latest video from the uploads playlist
    playlist_data = requests.get(f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={uploads_playlist_id}&maxResults={max_results}&key={YOUTUBE_API_KEY}').json()
    return playlist_data.get('items', [])

@tasks.loop(minutes=1440)  # Adjust the checking interval as needed
async def check_youtube():
    global LAST_VIDEO_ID
    channel_id = get_channel_id(MONITOR_USERNAME)
    video_items = get_latest_video(channel_id, 1)
    
    if video_items:
        video_id = video_items[0]['snippet']['resourceId']['videoId']
        
        # If video ID is different from the last known one, it's a new video
        if LAST_VIDEO_ID != video_id:
            LAST_VIDEO_ID = video_id
            video_title = video_items[0]['snippet']['title']
            embed = discord.Embed(title=f"kory made another video with mspaint {MONITOR_USERNAME}", description=video_title, color=0x1DA1F2, url=f"https://www.youtube.com/watch?v={video_id}")
            channel = bot.get_channel(DISCORD_CHANNEL_ID)  # Replace with your Discord channel ID
            await channel.send(embed=embed)

@bot.command()
async def latestvideo(ctx, username: str, count: int = 1):
    """Get the latest video(s) of a YouTube user."""
    channel_id = get_channel_id(username)
    if not channel_id:
        await ctx.send(f"🚫 Unable to find a channel with the username {username}.")
        return
    video_items = get_latest_video(channel_id, count)
    if video_items:
        for item in video_items:
            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            embed = discord.Embed(title=f"🎬 Latest video by @{username}", description=f"🔗 [Watch Here](https://www.youtube.com/watch?v={video_id})", color=0x1DA1F2)
            embed.add_field(name="📽️ Video Title", value=video_title, inline=False)
            embed.set_footer(text="Powered by #TeamPurple", icon_url=URL_TO_FOOTER_ICON)
            await ctx.send(embed=embed)
    else:
        await ctx.send(f"🚫 {username} does not have any videos or there was an issue fetching them.")


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f"Welcome {member.mention} to the server! Use `!info` for more information about the bot.")

@bot.command()
async def info(ctx):
    """Provides information about the bot."""
    embed = discord.Embed(title="🤖 Baggie-Bot 💜", description="Sup fam! 🚀 #TeamPurple in the house! Dive in to see the dopest commands we got for y'all! 💥", color=0x1DA1F2)
    
    embed.set_author(name="🏕 XXXX XXXXXX 🛶", url="https://example.com", icon_url="https://example.com/example.png")
    embed.set_image(url="https://example.com/example.png")
    embed.set_thumbnail(url=URL_TO_THUMBNAIL_IMAGE)
    
    # Twitter related commands
    embed.add_field(name="**Twitter Hacks** 🐦", value="Stay woke with these Twitter tools! 🔍", inline=False)
    embed.add_field(name="**!userid <TwitterUsername>**", value="Wanna know the ID behind the handle? Drop the @ and see the magic! 😎\nEx: `!userid elonmusk`", inline=False)
    embed.add_field(name="**!userdata <TwitterUsername>**", value="Peep into the deets of any Twitter homie! 💼\nEx: `!userdata elonmusk`", inline=False)
    embed.add_field(name="**!usertweets <TwitterUsername> [Number of Tweets]**", value="Slide through the latest tweets and spill the tea! 🍵\nEx: `!usertweets elonmusk 5`", inline=False)
    embed.add_field(name="**!converturl <DynamicURL>**", value="Convert Twitter Space Dynamic URLs to Playable ones!  🔗 \nEx: `!converturl https://prod-fastly-us-east-1.video.pscp.tv/Transcoding/v1/hls/HJ_mln8pK__VC2q-N-rT3NVos_Q142J1WRwalLbgKkuiVFSyJLWtmbIv1QhI3puicW--3EVsF5_39zARqZgLdw/non_transcode/us-east-1/periscope-replay-direct-prod-us-east-1-public/audio-space/dynamic_playlist.m3u8?type=live`", inline=False)
    
    # YouTube related command
    embed.add_field(name="**YouTube Vibes** 🎬", value="Catch the latest bops from YouTube creators! 🎥", inline=False)
    embed.add_field(name="**!latestvideo <YouTubeUsername> [Number of Videos]**", value="See what's poppin' on the Tube! 🍿\nEx: `!latestvideo mrbeast 5`", inline=False)

    # Stock related command
    embed.add_field(name="**Stock Hustle** 📈", value="Get that bread! See the latest stock moves! 💹", inline=False)
    embed.add_field(name="**!stockprice <TickerSymbol>**", value="Peek the latest price and flex on 'em! 💰\nEx: `!stockprice AMC`", inline=False)

    # Audio files command
    embed.add_field(name="**Beats & Bops** 🎵", value="Dig through the latest tracks and find your jam! 🎧", inline=False)
    embed.add_field(name="**!audiofiles**", value="Scope out all the artists in the hub! 🎤", inline=False)
    embed.add_field(name="**!artistfiles <ArtistName>**", value="Deep dive into an artist's latest tracks! 🔍\nEx: `!artistfiles hostname`", inline=False)
    
    embed.add_field(name="**Tech Support** 🛠️", value="Shoutout to PetRockMiner - #JuSuisAlgoHack #SFYL 🎧", inline=False)
    embed.set_footer(text="Powered by XXXXXXXX 🧼", icon_url=URL_TO_FOOTER_ICON)
    
    await ctx.send(embed=embed)

def parse_user_info(user_data):
    legacy = user_data.get('legacy', {})
    verification_info = user_data.get('verification_info', {})
    return {
        'username': legacy.get('screen_name'),
        'full_name': legacy.get('name'),
        'user_id': user_data.get('rest_id'),
        'bio': legacy.get('description'),
        'profile_image': legacy.get('profile_image_url_https'),
        'banner_image': legacy.get('profile_banner_url'),
        'followers_count': legacy.get('followers_count'),
        'following_count': legacy.get('friends_count'),
        'tweets_count': legacy.get('statuses_count'),
        'location': legacy.get('location'),
        'is_blue_verified': user_data.get('is_blue_verified'),
        'created_at': legacy.get('created_at'),
        'favourites_count': legacy.get('favourites_count'),
        'creator_subscriptions_count': user_data.get('creator_subscriptions_count'),
        'is_identity_verified': verification_info.get('is_identity_verified'),
        'listed_count': legacy.get('listed_count'),
        'media_count': legacy.get('media_count')
    }

def parse_tweet_data(tweet_data):
    legacy = tweet_data.get('legacy', {})
    return {
        'text': legacy.get('full_text'),
        'created_at': legacy.get('created_at'),
        'retweet_count': legacy.get('retweet_count'),
        'favorite_count': legacy.get('favorite_count'),
        'quoted_url': legacy.get('quoted_status_permalink', {}).get('expanded') if 'quoted_status_permalink' in legacy else None
    }

def paginate_audio_files(grouped_files, items_per_page=12):
    """Paginate the audio files into multiple embeds."""
    pages = []

    for artist, artist_files in grouped_files.items():
        for i in range(0, len(artist_files), items_per_page):
            embed = discord.Embed(title=f"Files from {artist}", color=0x1DA1F2)
            for file in artist_files[i:i+items_per_page]:
                duration = file.get('duration', 'N/A')
                size = file.get('size', 'N/A')
                date = file.get('date', 'N/A')
                path = file.get('path', 'N/A')
                embed.add_field(name=file['name'], value=f"Size: {file['size']} bytes\nDuration: {file['duration']} seconds\nDate: {file['date']}\n[Download](https://example.com{file['path']})", inline=False)
            pages.append(embed)

    return pages

@bot.command()
async def userid(ctx, username: str):
    """Get the user ID of a Twitter user."""
    user_id = twitter.get_user_id(username)
    embed = discord.Embed(title=f"🆔 User ID for @{username}", description=f"User ID: `{user_id}`", color=0x1DA1F2)
    embed.set_footer(text="Powered by #TeamPurple", icon_url=URL_TO_FOOTER_ICON)
    await ctx.send(embed=embed)

@bot.command()
async def userdata(ctx, username: str):
    """Get the user data of a Twitter user."""
    raw_user_data = twitter.get_user_data(username)
    user_data = parse_user_info(raw_user_data)
    
    # Create a rich embed
    embed = discord.Embed(title=f"📌 User Information for @{user_data['username']}", description=f"📝 {user_data['bio']}", color=0x1DA1F2)
    embed.set_thumbnail(url=user_data['profile_image'])
    embed.set_author(name="🏕 XXXX XXXXXX 🛶", url="https://example.com", icon_url="https://example.com/example.png")
    embed.set_image(url="https://campbaggie.com/bgpk.png")
    embed.add_field(name="🔠 Full Name", value=user_data['full_name'], inline=False)
    embed.add_field(name="🆔 User ID", value=user_data['user_id'], inline=False)
    embed.add_field(name="👥 Followers", value=f"{user_data['followers_count']:,}", inline=False)  # Use , as a thousand separator
    embed.add_field(name="🚶 Following", value=f"{user_data['following_count']:,}", inline=False)
    embed.add_field(name="🐦 Total Tweets", value=f"{user_data['tweets_count']:,}", inline=False)
    embed.add_field(name="🌍 Location", value=user_data['location'] or "N/A", inline=False)
    embed.add_field(name="🔵 Pays for X?", value="Yes" if user_data['is_blue_verified'] else "No", inline=False)
    embed.add_field(name="📅 Account Created", value=user_data['created_at'], inline=False)
    embed.add_field(name="❤️ Favourites", value=f"{user_data['favourites_count']:,}", inline=False)
    embed.add_field(name="🔗 Subscriptions", value=f"{user_data['creator_subscriptions_count']:,}", inline=False)
    embed.add_field(name="✅ Identity Verified?", value="Yes" if user_data['is_identity_verified'] else "No", inline=False)
    embed.add_field(name="📊 Listed Count", value=f"{user_data['listed_count']:,}", inline=False)
    embed.add_field(name="🖼️ Media Count", value=f"{user_data['media_count']:,}", inline=False)
    embed.set_footer(text="Powered by XXXXXXXXXX", icon_url=URL_TO_FOOTER_ICON)
    
    await ctx.send(embed=embed)

@bot.command()
async def usertweets(ctx, username: str, total: int = 1):
    """Get tweets of a Twitter user."""
    raw_tweets = twitter.get_user_tweets(username, total=total)
    if raw_tweets and 'data' in raw_tweets:
        for tweet_data in raw_tweets['data']:
            tweet = parse_tweet_data(tweet_data['content']['itemContent']['tweet_results']['result'])
            embed = discord.Embed(title=f"🐦 Tweet from @{username}", description=tweet['text'], color=0x1DA1F2)
            embed.set_footer(text=f"🔁 Retweets: {tweet['retweet_count']} | ❤️ Favorites: {tweet['favorite_count']} | 📅 Date: {tweet['created_at']}")
            if tweet['quoted_url']:
                embed.add_field(name="🔗 Quoted Tweet", value=tweet['quoted_url'], inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send(f"🚫 {username} does not have any tweets or there was an issue fetching them.")

async def fetch_stock_price(ticker):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "Global Quote" in data:
        return data["Global Quote"]
    else:
        return None

@bot.command()
async def stockprice(ctx, ticker: str):
    """Fetches the stock price for a given ticker."""
    stock_data = await fetch_stock_price(ticker)
    if stock_data:
        price = stock_data["05. price"]
        change = stock_data["09. change"]
        percent_change = stock_data["10. change percent"]
        embed = discord.Embed(title=f"📈 Stock Price for {ticker}", description=f"🏷️ Price: ${price}\n🔺 Change: ${change}\n📊 Percent Change: {percent_change}", color=0x1DA1F2)
        embed.set_footer(text="Powered by XXXXXXXXX", icon_url=URL_TO_FOOTER_ICON)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"🚫 Couldn't fetch data for {ticker}. Please ensure the ticker is correct.")

@bot.command()
async def audiofiles(ctx):
    response = requests.get(AUDIO_FILES_ENDPOINT)
    if response.status_code == 200:
        files = response.json()
        if not files:
            await ctx.send("No m4a files found.")
            return    
        
        grouped_files = defaultdict(list)
        for file in files:
            match = re.search(r'\[(.*?)\]', file['name'])
            if match:
                artist = match.group(1)
                grouped_files[artist].append(file)
            else:
                grouped_files['Unknown Artist'].append(file)

        artists = sorted(grouped_files.keys())

        # Formatting the artists list with emojis and dividers
        formatted_artist_list = ""
        artists_per_row = 1  # Number of artists per row
        divider = "\n" + "---------------------------------------" + "\n"
        for index, artist in enumerate(artists, start=1):
            formatted_artist_list += f"🎤 {artist}"
            if index % artists_per_row == 0:
                formatted_artist_list += divider
            else:
                formatted_artist_list += " | "

        embed.set_author(name="XXXX XXXXXXX", url="https://example.com", icon_url="https://example.com/example.png")
        embed.set_image(url="https://example.com/example.png")    
        embed = discord.Embed(title="🎵 Available Artists 🎵", description=formatted_artist_list.rstrip(divider), color=0x1DA1F2)
        embed.set_thumbnail(url=URL_TO_THUMBNAIL_IMAGE)
        embed.set_footer(text="Powered by XXXXXXXXXX", icon_url=URL_TO_FOOTER_ICON)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Failed to fetch m4a files. Server responded with: {response.status_code}.")

@bot.command()
async def artistfiles(ctx, *, artist_name: str):
    response = requests.get(AUDIO_FILES_ENDPOINT)
    if response.status_code == 200:
        files = response.json()
        
        grouped_files = defaultdict(list)
        for file in files:
            match = re.search(r'\[(.*?)\]', file['name'])
            if match:
                artist = match.group(1)
                grouped_files[artist].append(file)
            else:
                grouped_files['Unknown Artist'].append(file)

        artist_files = grouped_files.get(artist_name, None)
        if not artist_files:
            await ctx.send(f"No files found for artist: {artist_name}.")
            return

        embed = discord.Embed(title=f"🎵 Files from {artist_name} 🎵", description=f"Here are the latest tracks from {artist_name}!", color=0x1DA1F2)
        embed.set_author(name="🏕 xxxxx xxxxxx 🛶", url="https://example.com", icon_url="https://example.com/example.png")
        embed.set_image(url="https://example.com/example.png")
        embed.set_thumbnail(url=URL_TO_THUMBNAIL_IMAGE)  # You can replace this with a relevant image URL
        embed.set_footer(text="Powered by xxxxxxxxx", icon_url=URL_TO_FOOTER_ICON)  # You can replace the icon URL with your own

        for file in artist_files:
            song_title = file['name'].split('] ')[-1].rsplit('.', 1)[0]  # Extracting song title from filename
            size_str = format_size(file.get('size', 0))
            duration_str = format_duration(float(file.get('duration', 0)))
            date_str = format_date(file.get('date', ''))
            
            embed.add_field(name=f"🎤 {song_title} 🎤", value=f"📦 Size: {size_str}\n⏳ Duration: {duration_str}\n📅 Date: {date_str}\n[🔗 Download](https://example.com{file['path']})", inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Failed to fetch m4a files. Server responded with: {response.status_code}.")

@bot.command()
async def converturl(ctx, dynamic_url: str):
    """Converts a Twitter Space Dynamic URL to a Playable URL."""
    if "dynamic_playlist.m3u8?type=live" not in dynamic_url:
        await ctx.send("🚫 Please provide a valid dynamic URL.")
        return

    try:
        playable_url = convert_dynamic_to_playable(dynamic_url)
        embed = Embed(title="🔗 Twitter Space URL Converter", description=f"Here's the playable URL for the provided Twitter Space Dynamic URL.", color=0x1DA1F2)
        embed.add_field(name="Original Dynamic URL", value=dynamic_url, inline=False)
        embed.add_field(name="Converted Playable URL", value=playable_url, inline=False)
        embed.set_footer(text="Powered by #TeamPurple", icon_url=URL_TO_FOOTER_ICON)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"🚫 An error occurred while converting the URL: {str(e)}")

bot.run(TOKEN)
