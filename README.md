# raincoat

### EXPLANATION:

This is a movie game where users can create their own film and rate its success.

![screenshot](https://lh3.googleusercontent.com/Q3hw2CczmI3xHEHLjSieynBeiGdKKCsTjYG53lEVo_nwDio-W4SwxHg-LWfF7EKY4KkJxxRb5TZIqNxb530s-SCIVmKpBuF3wHGuK5UteyHKcfbtKWTlgQ9jxSk51Ma0tM33DsLTAwl71HY7u2dAmPWo6LVS9oT88bHFnuXApU3bqVcg1RQhFYyHiKjR4siwpeXxJOMrLLcerzW_riRZEOE3e2vqssRmU_FvPp_udoSkzVczgjL3NG8wxXvYcufHk54ruLsFY3Su_u59hu3CEgJlgXt_wxxt5zFxGTIlV7kh7ZBCIg6CkLICWdqzdHVnTrVntvHB5IsPZI_niNGGkC33-bj6UZdenKZuBHbY-0zcIWfBYtrmoDGXQYn9_aDsE4_BcY6p4uzL0XW9AeaQNiPqPXUbmzGeCrsmLOAklei87r3jFCfxYeqO381Bahmn99Ct_PdIJYoK5XKNbMJVhhMCfRX1JQl_7pkkmIdGQYYD9OKL1JIvmVjledntQZbWAyla6-_XgawM0xKFDftqCrGsTelXl77-YIsZGjt4ZR-RwqWGLtcl4nGSILl4GeYy2xvFIFr-Tuc6ChZUETr6W9GHjxcgKSeVayiV9NRt3Q=w1192-h670-no)

### REQUIREMENTS:

BeautifulSoup
requests
psycopg2
easygui

### HOW TO USE:

1. Run webscraper.py to scrape the IMDb top 250 and set up database.
2. Run queryfunctions.sql from command line to import data into database and perform computations.
3. Run gui.py to play the game!

### NOTES:

We put the actual database key in our file directly. This is probably bad form; in secure production the best way to do it is to have an environment variable directly on a local machine that is read into the program. However for the purpose of this project (which requires no data privacy) we didn't feel this level of security was necessary.
