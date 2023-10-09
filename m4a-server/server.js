// Expressing ourselves, and by ourselves, I mean our server
const express = require('express');
const ejs = require('ejs');
const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');
const mime = require('mime');
const chalk = require('chalk');
const config = require('./config.json');  // Load the config file

const colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta'];

const randomColor = colors[Math.floor(Math.random() * colors.length)];

const app = express();
const filesDataCache = [];

// Dropping that fire logo in the console
console.log(`
 ## ##   ### ###  ##  ##   ####     
##   ##   ##  ##  ##  ##    ##      
####      ##      ##  ##    ##      
 #####    ## ##    ## ##    ##      
    ###   ##        ##      ##      
##   ##   ##        ##      ##  ##  
 ## ##   ####       ##     ### ###

🩳 Welcome to the #SFYL bot that all the threat actors use 🧦
🤲💎Version: 1.0.3
🧩Developer: PetRockMiner
📌Description: This bot does nefarious things!
`);


// 👑 Tweaking the console so its boujee af 👝 ⏰
['log', 'error', 'warn', 'info'].forEach(method => {
    const original = console[method];
    console[method] = function (...args) {
        const timestamp = new Date().toISOString();
        original(`[${timestamp}]`, ...args);
    };
});

console.log(chalk.blue('💅 Console just got a glow-up! 🤳'));

// Pulling in the Redis power, cause we're all about that cache money
const redis = require('redis');

// Setting up that Redis client with some retry vibes for when things get shaky
const client = redis.createClient({
    retry_strategy: function(options) {
        if (options.error && options.error.code === 'ECONNREFUSED') {
            console.error('The server is in its refused the connection era bruh...');
            return new Error('The server refused the connection');
        }
        if (options.total_retry_time > config.redis.retryStrategyOptions.totalRetryTime) {
            console.error('Retry time exhausted, yo you trippin homie...');
            return new Error('Retry time exhausted');
        }
        if (options.attempt > config.redis.retryStrategyOptions.maxAttempts) {
            console.error('Too many retry attempts. I give up, you fell off and is gatekeepin!');
            return undefined;
        }
        return Math.min(options.attempt * 100, 3000);
    }
});

// Counting our precious m4a files because numbers matter
let totalM4aFiles = 0; // Total number of m4a files found
let downloadingM4aFiles = 0; // Number of m4a files still downloading
// This flag is our vibe check for Redis
let redisReady = false; // Add this flag to track Redis readiness
// If Redis throws a tantrum, we gotta handle it
client.on('error', (err) => {
    console.error(chalk.red('💪 Bruh, Redis is tripping, its about to catch these hands! 🦴'), err);
    redisReady = false;  // explicitly set redisReady to false on error
});
// Celebrating when we link up with Redis 🎉
client.on('connect', () => {
    console.log('👅 Yasss Fam! Just connected to Redis! ONG let him cook.🍳');
    redisReady = true;
});
client.on('end', () => {
    console.log('👋 Bruh, we just got ghosted by Redis!');
    redisReady = false;  // set redisReady to false when the connection ends
});
client.on('reconnecting', () => {
    console.log('🔄 Hold up! We trying to holla at Redis again.');
});

// Serving looks with EJS as our view engine
app.set('view engine', 'ejs');

// Define the mime type, cause we ain't basic
express.static.mime.define({'audio/x-m4a': ['m4a']});

// Sharing our files with the world, cause sharing is caring, looking at you Netflix!
app.use('/baggies/files', express.static('/home/rocky/download'));

// Endpoint to serve a JSON list of available m4a files for bots or other services
app.get('/baggies/fileslist', (req, res) => {
    res.json(filesDataCache);
});

// Prepping our file parser, cause we're nosy like that
let parseFileMethod;

// These cache functions are our secret sauce to serve data faster than you can say "Sussy Baka"
async function getCachedFilesData() {
    return new Promise((resolve, reject) => {
        if (!redisReady) {
            console.warn('🛑 Ok Boomer, Redis is being a real Karen RN! Finna skip cache fetch, shit is trash 🚮');
            return resolve([]);
        }
        
        client.get('bopFilesDataCache', (err, result) => {
            if (err) reject(err);
            if (result) resolve(JSON.parse(result));
            resolve([]);
        });
    });
}

async function cacheFilesData(data) {
    if (!redisReady) {
        console.warn('👁‍🗨 Something is sus Redis is not ready yet! Weird flex bruh, Skipping cache set. ⛔️');
        return;
    }
    
    client.set('bopFilesDataCache', JSON.stringify(data), 'EX', config.redis.cacheExpiry);  // Using cache expiry from config
}

// Function to get that metadata parser on fleek
async function initializeParseFile() {
    if (!parseFileMethod) {
        // High-key excited to get these meta vibes
        const musicMetadata = await import('music-metadata');
        parseFileMethod = musicMetadata.parseFile;
    }
}

// Endpoint to serve up the deets, baggies bout to be shook... big mad
app.get('/baggies', async (req, res) => {
    await initializeParseFile();
    console.log(chalk[randomColor]('🥵 Incel Fantasy endpoint on deck and flexin! 🍆'));
    res.render('index', { files: filesDataCache });
});

// We out here vibing on port 3001, pull up!
app.listen(config.serverPort, () => {
    console.log(chalk.cyanBright(`💻 This server is living rent-free in korys brain 🧠 on port:${config.serverPort} fax, 📠 no printer! 🖨`));
    initializeFilesData().then(() => {
        watchDirectory(); 
    });
});

// Function to initialize data, cause we ain't playing with that basic cache
async function initializeFilesData() {
    await initializeParseFile();

    // Reset the downloading files counter each time we initialize the files data
    totalM4aFiles = 0;
    downloadingM4aFiles = 0;
    
    const cachedData = await getCachedFilesData();
    if (cachedData.length > 0) {
        filesDataCache.push(...cachedData);
        console.log('🍧 Yuh! Say less, serving it straight from the cache. We gucci flip flop, no cap! 🧢');
        return;
    }

    const directories = fs.readdirSync(config.downloadDirectory);
    console.log(chalk[randomColor]('🤭 My whole ass life is watching 👀 these directories to find those delicious 💧 baggie tears 💧'));

    for (const dir of directories) {
        const dirPath = path.join('/home/rocky/download', dir);
        if (fs.statSync(dirPath).isDirectory()) {
            console.log(`💥 Spittin str8 facts! 🥠 we spillin the tea on ${dir} 🍵`);
            const files = fs.readdirSync(dirPath).filter(file => file.endsWith('.m4a'));
            totalM4aFiles += files.length;
            for (const file of files) {
                console.log(`✅ Say Less! Found a baggie space!: ${file} 🔎`);
                const filePath = path.join(dirPath, file);
                
                try {
                    const metadata = await parseFileMethod(filePath);
                    if (!metadata || !metadata.format || typeof metadata.format.duration !== 'number') {
                        throw new Error("Metadata missing or incomplete");
                    }

                    const fileData = {
                        name: file,
                        path: `/baggies/files/${dir}/${encodeURIComponent(file)}`,
                        size: fs.statSync(filePath).size,
                        duration: metadata.format.duration,
                        date: fs.statSync(filePath).mtime,
                    };

                    filesDataCache.push(fileData);
                } catch (err) {
                    console.error(`❌ Couldn't fetch all details for: ${file}. Reason: ${err.message}`);
                }
            }
        }
    }

    cacheFilesData(filesDataCache);
    console.log(`📢 BREAKING NEWS! Yo good peeps, I found ${totalM4aFiles} total spaces, thats the situationship.™️`);
}

// Function to watch the directory, cause @me next time a bop drops, amirite?
async function watchDirectory() {
    await initializeParseFile();
    console.log('👀 Got my eyes peeled like a tarabull OF simp, watching for those hawt spaces 💋');
    const watcher = chokidar.watch(config.downloadDirectory, {
        ignored: /(^|[\/\\])\../,
        persistent: true,
        ignoreInitial: true,
        followSymlinks: true,
        usePolling: true,
        depth: 3,
        interval: 100,
    });

    watcher.on('add', async filePath => {
        if (filePath.endsWith('.m4a')) {
            const isDownloading = await isFileStillDownloading(filePath);
            if (!isDownloading) {
                try {
                    const metadata = await parseFileMethod(filePath);
                    if (!metadata || !metadata.format || typeof metadata.format.duration !== 'number') {
                        throw new Error("Metadata missing or incomplete");
                    }

                    const fileData = {
                        name: path.basename(filePath),
                        path: filePath,
                        size: fs.statSync(filePath).size,
                        duration: metadata.format.duration,
                        date: fs.statSync(filePath).mtime,
                    };

                    filesDataCache.push(fileData);
                    cacheFilesData(filesDataCache);
                    console.log(`👣 OK bet! New trauma bonding session alert. Just yeeted and cached it: ${path.basename(filePath)} ✂️`);
                } catch (err) {
                    console.error(`❌ Couldn't fetch all details for: ${path.basename(filePath)}. Reason: ${err.message}`);
                }
            }
        }
    });

    watcher.on('ready', () => {
        console.log(`🔜 Hopium sessions still downloading: ${downloadingM4aFiles} 🔜`);
    });
}

// Function to vibe check if file is still downloading or we're all Gucci
function isFileStillDownloading(file) {
    const initialSize = fs.statSync(file).size;
    return new Promise(resolve => {
        setTimeout(() => {
            const newSize = fs.statSync(file).size;
            if (initialSize !== newSize) {
                console.log(`🌭 Miss me with that ish trying to peep ${path.basename(file)} while it's still hotdog water... 🌊`);
            }
            resolve(initialSize !== newSize);
        }, 10000);
    });
}

// When we're out, we gotta say bye to Redis properly. It's just polite.
process.on('exit', () => {
    client.quit();
});
