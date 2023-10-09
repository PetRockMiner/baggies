# 🔥 #SFYL, Shit, wrong account...🔥

What it do what it be? 🌊 If you're looking for the most lit projects you've hit the jackpot! Dive in and let's ride this digital wave together! 🏄‍♂️🎉

---

## 🌌 twspace-crawler 🌌

Ever wanna keep tabs on those Twitter Spaces? Say less. With **twspace-crawler**, you can:
- **Monitor Spaces**: Keep an eye on your fave Twitter peeps and their Spaces.
- **Automatic Downloads**: Automatically snag those Spaces once they're over.
- **Discord Integration**: Get notified through Discord because who checks emails anyway?

---

## 🍕 #SFYL Server && Bot 🤩

This ain't your basic bot. Introducing **#SFYL Bot**, the boujee-est of them all. With this bad boy, you can:
- 🎧 Jam to those m4a files.
- 🚀 Cache like a speed demon with Redis.
- 📂 Have someone (or something) to stalk your directories.
- 🎨 Splash some color in that console. 
- 🧠 Get those views with EJS as the view engine.
- 🎉 Show off with a bomb logo and console messages.

---

## 🚀 #SFYL Web Experience 💥

Looking to flex on the web? **#SFYL Web Experience** is where it's at. Features include:
- **Floating Heads Rain**: Click and watch those profile pics rain from the sky.
- **Harlem Shake**: Throw it back with this iconic audio track.
- **Vibey Button**: Hover and see some aesthetic magic.
- **Responsive Design**: Cuz we gotta look good on every device, right?

---

## 🤖 #TeamPurple Bot 🤖

Brought to you by the legends of **#TeamPurple**, this Discord bot is the real MVP. Check these out:
- 🎬 Get the latest from YouTube.
- 🐦 Dive deep into Twitter and uncover those secrets.
- 📈 Stock market? We got you.
- 🎵 Find your next favorite jam.

---

💡 **Tip**: Life's too short for boring code. So, whether you're here for the memes or the tech, vibe with us and make some digital magic! ✨🌈

Remember, in a world full of 1s and 0s, be a 💯. Stay wavy! 🤙🌊



# 🔥 `twspace-crawler` Installation & Setup Guide 🔥

Yo fam! 🤙 If you're trying to get the 411 on how to set up `twspace-crawler` to monitor and download Twitter Spaces, you've come to the right spot! Let's get this bread! 🍞🚀

## 🛠️ Installation

### 1. **Command-line Installation** 🖥️
```bash
npm install --global twspace-crawler
```

### 2. **Module Installation** (for the nerdy devs out there) 🤓
```bash
npm install twspace-crawler
```

## 📝 Config Setup

### 1. **Create a `config.json`** 📄

Here's a sample for you to copy & vibe with:

```json
{
  "interval": 30000,
  "users": [
    {
      "username": "username"
    },
    "username_1",
    "username_2",
    "username_3",
    "username_4"
  ],  
  "webhooks": {
    "discord": [
      {
        "active": true,
        "urls": [
          "https://discord.com/api/webhooks/PLACEHOLDER_DISCORD_WEBHOOK_URLS_HERE"
        ],
        "usernames": [
          "<all>"
        ],
        "mentions": {
          "roleIds": [],
          "userIds": []
        }
      }
    ]
  }
}
```

**Note**: Replace the placeholders with the actual data, but keep it on the DL! Don't share sensitive info! 🙊

### 2. **Setup `.env` File** 🌍

This is where you keep those secret keys. Make sure to name it `.env` and keep it in the current working folder.

```env
TWITTER_AUTHORIZATION=PLACEHOLDER_YOUR_AUTHORIZATION_HERE
TWITTER_AUTH_TOKEN=PLACEHOLDER_YOUR_AUTH_TOKEN_HERE
TWITTER_CSRF_TOKEN=PLACEHOLDER_YOUR_CSRF_TOKEN_HERE
```

Again, fam, don't share those placeholder values! 🤫 Replace them with the real ones.

## 🚀 Usage

To monitor some dope users and save their Spaces when they're done:

```bash
twspace-crawler --user user1,user2,... --env ./.env --config ./config.json
```

## 🤘 Wrapping Up

That's it! You're all set to roll with `twspace-crawler`! Keep it groovy, and if you run into any issues, just remember... "The code is strong with this one!" 😎✌️

Stay vibey! 🌈🎉
