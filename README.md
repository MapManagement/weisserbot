Bot
---
TwitchBot written in Python using [TwitchIO](https://github.com/TwitchIO/TwitchIO).
Currently only [Weissemoehre](https://www.twitch.tv/weissemoehre) is using this  specific bot on his Twitch Channel.
Further implementations are planned and listed at the "Future" section. If you also have ideas or want
to report a bug, either message [Mapman](https://twitter.com/MapManagement) or
[WeisseMoehre](https://twitter.com/WeisseMoehre) on Twitter including your concern or just contribute your ideas/fixes.
Each constructive contribution is welcomed and will hopefully improve the code and add more features to use.

HowTo
-------
    Commands to use in the streamer's chat:
     
    Add command
    !new_cmd <command_name> <command_content>
    
    Edit command
    !edit_cmd <command_name> <command_content>
    
    Delete command
    !del_cmd <command_name>
    
    Reload a module
    !reload_mod <module_name>

Future
------
- [ ] creating a website connected to the bot
- [x] possibly creating a public repo on GitHub 
- [x] implementing MySQL databases for watchtime and other stuff
- [ ] finishing sub count command
- [ ] finding a solution for problems with followage command
- [ ] replacing json file with database and message_handler
- [ ] function for adding /me at the start of each bot message
- [ ] consistent usage of ONE way to declare paths