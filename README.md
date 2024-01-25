Welcome to Krinlee's Discord Bot (Porkchop is just the name I gave mine).


I have built this bot to be run from an unRaid server. If you have an unRaid server and wanted to use this bot, it could essentially be possible.

This REEADME file is to explain how you would go about using this template for your own Discord Bot.

For starters, you can add the docker image from the CA store in unRaid. You just search for porkchop, then on the right click where it says
"click here for more options from Docker Hub". After that (for me anyway) it is the first one in the 2nd row. It is just called porkchop, but underneath it says mrkrinlee (that's me).

Once added you can add a folder in your appdata directory. I labled this folder porkchop because that is what I named my Discord Bot, and for now it is the name of my image and container.
In this folder I also added 3 more folders labled config, assets, and trivia and also added in the files that they have in this github in those folders. I'm not 100% sure if adding all of
the files is really needed but it was what I did. In theory I suppose all of the txt documents should create themselves and it seems like the assets and the trivia_list.py files were reading
before I added them to the folder, but I had some issues with trivia working correctly so I just added all of the files I was using here and added the paths in the unRaid edit settings for the
container.

You will also need to create your .env file that goes in the config folder. I had a sample file here in the github but I kept getting flagged and having to create new tokens for Discord/Openai/Twitch
so I ommited that file from here. You should be able to tell from the secrets.py file though what you need to include in the .env file.

I'm pretty sure that is it for now though. If you do decide to give this a try let me know what you think, and if you have any issues let me know and I will see what I can do to help.






