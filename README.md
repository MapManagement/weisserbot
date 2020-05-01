Bot
---
TwitchBot written in Python using [TwitchIO](https://github.com/TwitchIO/TwitchIO).
Currently, only [Weissemoehre](https://www.twitch.tv/weissemoehre) is using this bot on his Twitch Channel.
Further implementations are planned and listed at the "Future" section. If you also have ideas or want
to report a bug, either message [Mapman](https://twitter.com/MapManagement) or
[WeisseMoehre](https://twitter.com/WeisseMoehre) on Twitter including your concern or just contribute your ideas/fixes.
Each constructive contribution is welcomed and will hopefully improve the code and add more features to use.

HowTo
-------
    Commands to use in streamer's chat:
     
    Add command
    !new_cmd <command_name> <command_content>
    
    Edit command
    !edit_cmd <command_name> <command_content>
    
    Delete command
    !del_cmd <command_name>
    
    Enabling or disbling a commmand
    state can be "on" or "off"
    !turn_cmd <command_name> <state>
    
More commands
-------
    Sends the time (in days) the author has followed
    !followage
    
    Sends the time the author watched the stream
    !watchtime
    
    Sends the number of users who subscribed to the streamer
    !subcount
    
 CommandNotFound Error
-------
Since most of the commands which are created by users in the Twitch chat are not handled by my command_handler,
I decided to edit the event_command_error function in bot.py of TwitchIO so nothing will be printed to the
terminal when any message starts with a command prefix and a "CommandNotFound" Error as thrown.

Future
------
- [ ] creating a website connected to the bot
- [x] possibly creating a public repo on GitHub 
- [x] implementing MySQL databases for watchtime and other stuff
- [x] finishing sub count command
- [x] finding a solution for problems with followage command
- [x] replacing json file with database and message_handler
- [x] function for adding /me at the start of each bot message
- [x] consistent usage of ONE way to declare paths
- [x] catching CommandNotFound error
- [x] expand README with better instructions and explanations
- [ ] creating a Discord bot that is connected to the Twitch bot
- [ ] working on a better way of tracking the watched time of users