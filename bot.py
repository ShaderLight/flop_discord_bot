import discord
from discord.ext import commands
import urbandictionary as ud
import shinden as sh

import json
from datetime import datetime, timedelta

import timer
import covid19



cv = covid19.Covid_data()
t = timer.Timer()

with open('settings.json') as f:
    content = json.load(f)

api_key = content['api']
prefix = content['prefix']


# Applying settings
bot = commands.Bot(command_prefix = prefix, help_command = None)


# Excuted when bot is connected and ready
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) # printing out the bot's nickname

    for guild in bot.guilds:
        print('Logged in ' + str(guild.name) +  ' (id: '+ str(guild.id) +')') # printing out server name, which bot is connected to

    members = ' - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}') # printing out a list of server members

    # Setting bot status to streaming (Never gonna give you up)
    stream = discord.Streaming(name = prefix + 'helperino', url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    await bot.change_presence(activity = stream) 

    print("Ready")


# Help command
@bot.command(name = 'help', aliases = ['helperino'], help = 'Lists available commands')
async def help(ctx):
    color = discord.Colour(16777215)
    response = discord.Embed(title = '**Flop bot**', type = 'rich', description = '() - parameter, [] - optional parameter with a default value.\nIn commands with optional which_result parameter and a number in last word of first param, it is recommended to enter the which_result param aswell, eq. **' + prefix +'shindenanime sao 2 1**', colour = color.dark_magenta(), url = 'https://github.com/ShaderLight/flop_discord_bot')

    response.add_field(name = prefix + 'urban (word) [which_result = 1]', value = 'Responds with Urban Dictionary definition', inline = False)
    response.add_field(name = prefix + 'urbanlist (word)', value = 'Results for maximum 10 first results from Urban Dictionary', inline = False)
    response.add_field(name = prefix + 'urbanrandom', value = 'Returns random Urban Dictionary definition', inline = False)
    response.add_field(name = prefix + 'shindenanime (title) [which_result = 1]', value = 'Returns an anime from shinden.pl', inline = False)
    response.add_field(name = prefix + 'shindenmanga (title) [which_result = 1]', value = 'Returns a manga from shinden.pl', inline = False)
    response.add_field(name = prefix + 'shindenanimelist (title)', value = 'Returns a list of anime from shinden.pl', inline = False)
    response.add_field(name = prefix + 'shindenmangalist (title)', value = 'Returns a list of manga results', inline = False)
    response.add_field(name = prefix + 'shindencharacter (name) [which_result = 1]', value = 'Returns a character result from shinden.pl', inline = False)
    response.add_field(name = prefix + 'shindencharacterlist (name)', value = 'Responds with a list of character results', inline = False)
    response.add_field(name = prefix + 'shindenuser (nickname) [which_result = 1]', value = 'Searches for a shinden user', inline = False)
    response.add_field(name = prefix + 'shindenuserlist (nickname)', value = 'Lists shinden users found', inline = False)
    response.add_field(name = prefix + 'covid', value = 'Returns actual data about COVID-19 for the world and Poland', inline = False)


    await ctx.send(embed = response)


 
# Urban Dictionary related commands



@bot.command(name = 'urban', aliases=['u','ud'], help = 'Responds with urban dictionary definition')
async def urban(ctx, *args):
    if args == (): # If no arguments were passed, then respond with help message
        help_string = ('**Command:** urban\n'
            '**Description:** Responds with urban dictionary definition.\n'
            '**Aliases:** `u, ud`\n'
            '**Usage:** `' + prefix + 'urban (word) [which_result = 1]`\n'
            '**Parameters:** \n'
            '\t*word* (str)\n'
            '\t*which_result* (int) - optional, default value = 1')
        return await ctx.send(help_string)

    if len(args) >= 2:
        args_list = list(args)
        which_result = 1
        possible_int = args_list.pop()

        try:
            which_result = int(possible_int)
        
        except:
            args_list.append(possible_int)
        
        words = ' '.join(args_list)
        
        defs = ud.define(words) # Using UrbanDictionary library to search for Urban Dictionary definitions
        try:
            definition = defs[which_result-1] # Selecting one result, based on which_result parameter (first result by default)
        except IndexError:
            await ctx.send("**No result**") # If index is out of range, then prints out that there was no result found
    
        response = '***' + definition.word + '***' + '\n\n`' + definition.definition + '\n\n' + definition.example + '`' # Reponse with some discord formatting for a nicer look
        await ctx.send(response)

    else:
        words = ' '.join(args)

        defs = ud.define(words) # Using UrbanDictionary library to search for Urban Dictionary definitions
        try:
            definition = defs[0]
        except IndexError:
            await ctx.send("**No result**") # If index is out of range, then prints out that there was no result found
    
        response = '***' + definition.word + '***' + '\n\n`' + definition.definition + '\n\n' + definition.example + '`' # Reponse with some discord formatting for a nicer look
        await ctx.send(response)



@bot.command(name = 'urbanlist', aliases = ['ul','udlist','udl', 'ulist'], help = 'Responds with urban dictionary definition list')
async def urbanlist(ctx, *args): # This function responds with every definition found on UD (maximum result count is 10 and maximum word count for every definition is 75, urban command does not have that restriction)
    if args == ():
        help_string = ('**Command:** urbanlist\n'
            '**Description:** Responds with urban dictionary definition list.\n'
            '**Aliases:** `ul, udlist, udl, ulist`\n'
            '**Usage:** `' + prefix + 'urbanlist (word)`\n'
            '**Parameters:** \n'
            '\t*word* (str)')
        return await ctx.send(help_string)
    
    t.start()

    words = ' '.join(args)

    defs = ud.define(words)
    response = discord.Embed(title = words, type = 'rich', description = 'Results for maximum 10 first results from Urban Dictionary' )
    try:
        check = 0 # This variable checks if there was at least one successful iteration
        for i in range(10):
            result = defs[i]
            check = 1 
            text = (result.definition[:75] + '...') if len(result.definition) > 75 else result.definition # This line checks if the word count of the definition is over 75, if true, then cuts it and adds '...'
            response.add_field(name = result.word, value = text, inline = False)
    except IndexError:
        if check == 0: # If there wasnt any correct iteration, then bot responds with No result message
            t.stop()
            return await ctx.send("No results")
    
    footer_text = 'From shinden.pl | Done in '
    execution_time = str(t.stop())
    response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

    await ctx.send(embed = response)



@bot.command(name = 'urbanrandom', aliases = ['ur', 'udrandom', 'udr', 'urandom'], help = 'Returns random Urban Dictionary definition')
async def urbanrandom(ctx):
    definition = ud.random()[0]  # selecting first definition from the list of random definitions
    response = '***' + definition.word + '***' + '\n\n`' + definition.definition + '\n\n' + definition.example + '`'

    await ctx.send(response)



# Shinden related commands



@bot.command(name ='shindenanime', aliases = ['sa', 'shindena', 'sha', 'sanime', 'shanime'], help = 'Returns an anime from shinden.pl')
async def shindenanime(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindenanime\n'
            '**Description:** Returns an anime from shinden.pl\n'
            '**Aliases:** `sa, shindena, sha, sanime, shanime`\n'
            '**Usage:** `' + prefix + 'shindenanime (title) [which_result]`\n'
            '**Parameters:** \n'
            '\t*title* (str)\n'
            '\t*which_result* (int) - optional, default value = 1')
        return await ctx.send(help_string)
    
    t.start()

    if len(args) >= 2:
        args_list = list(args)
        which_result = 1
        possible_int = args_list.pop()

        try:
            which_result = int(possible_int)
        except:
            args_list.append(possible_int)
        
        title = ' '.join(args_list)

        anime_list = sh.search_titles(title)

        try:
            anime = anime_list[which_result-1] # Selecting one anime result from the list of all found results
        except TypeError:
            t.stop()
            return await ctx.send('No results')
        except IndexError:
            await ctx.send('which_result param was too big, showing last result')
            anime = anime_list[-1]

        color = discord.Colour(16777215)

        # Creating a discord embed message object and adding fields with information
        response = discord.Embed(title = '***' + anime.title + '***', type = 'rich', description = 'Tags: ' + str(anime.tags), colour = color.teal(), url = anime.url) 
        response.add_field(name = 'Score', value = anime.top_score)
        response.add_field(name = 'Episodes', value = anime.episodes)
        response.add_field(name = "Status", value = anime.status)

        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

        await ctx.send(embed = response)

    else:
        title = ' '.join(args)
        anime_list = sh.search_titles(title)

        try:
            anime = anime_list[0] # Selecting one anime result from the list of all found results
        except TypeError:
            t.stop()
            return await ctx.send('No results')

        color = discord.Colour(16777215)

        # Creating a discord embed message object and adding fields with information
        response = discord.Embed(title = '***' + anime.title + '***', type = 'rich', description = 'Tags: ' + str(anime.tags), colour = color.teal(), url = anime.url) 
        response.add_field(name = 'Score', value = anime.top_score)
        response.add_field(name = 'Episodes', value = anime.episodes)
        response.add_field(name = "Status", value = anime.status)

        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

        await ctx.send(embed = response)



@bot.command(name = 'shindenmanga', aliases = ['sm', 'shindenm', 'shm','smanga', 'shmanga'], help = 'Returns a manga from shinden.pl')
async def shindenmanga(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindenmanga\n'
            '**Description:** Returns a manga from shinden.pl\n'
            '**Aliases:** `sm, shindenm, shm, smanga, shmanga`\n'
            '**Usage:** `' + prefix + 'shindenmanga (title) [which_result]`\n'
            '**Parameters:** \n'
            '\t*title* (str)\n'
            '\t*which_result* (int) - optional, default value = 1')
        return await ctx.send(help_string)

    t.start()

    if len(args) >= 2:
        args_list = list(args)
        which_result = 1
        possible_int = args_list.pop()

        try:
            which_result = int(possible_int)
        except:
            args_list.append(possible_int)

        title = ' '.join(args_list)

        manga_list = sh.search_titles(title, anime_or_manga = 'manga')

        try:
            manga = manga_list[which_result-1]
        except TypeError:
            t.stop()
            return await ctx.send('No results')
        except IndexError:
            await ctx.send('which_result param was too big, showing last result')
            manga = manga_list[-1]

        color = discord.Colour(16777215)

        response = discord.Embed(title = '***' + manga.title + '***', type = 'rich', description = 'Tags: ' + str(manga.tags), colour = color.teal(), url = manga.url)
        response.add_field(name = 'Score', value = manga.top_score)
        response.add_field(name = 'Chapters', value = manga.episodes)
        response.add_field(name = 'Status', value = manga.status)

        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')
        
        await ctx.send(embed = response)

    else:

        title = ' '.join(args)

        manga_list = sh.search_titles(title, anime_or_manga = 'manga')

        try:
            manga = manga_list[0]
        except TypeError:
            t.stop()
            return await ctx.send('No results')

        color = discord.Colour(16777215)

        response = discord.Embed(title = '***' + manga.title + '***', type = 'rich', description = 'Tags: ' + str(manga.tags), colour = color.teal(), url = manga.url)
        response.add_field(name = 'Score', value = manga.top_score)
        response.add_field(name = 'Chapters', value = manga.episodes)
        response.add_field(name = 'Status', value = manga.status)
        
        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')
        
        await ctx.send(embed = response)



@bot.command(name = 'shindenanimelist', aliases = ['sal', 'shindenal', 'shal', 'sanimelist', 'shanimelist'], help = 'Returns a list of anime from shinden.pl')
async def shindenanimelist(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindenanimelist\n'
            '**Description:** Returns a list of anime from shinden.pl\n'
            '**Aliases:** `sal, shindenal, shal, sanimelist, shanimelist`\n'
            '**Usage:** `' + prefix + 'shindenanimelist (title)`\n'
            '**Parameters:** \n'
            '\t*title* (str)\n')
        return await ctx.send(help_string)

    t.start()

    title = ' '.join(args)

    anime_list = sh.search_titles(title)
    color = discord.Colour(16777215)

    response = discord.Embed(title= '***Shinden anime list***', type = 'rich', description = 'Search results for: **' + title + '**', colour = color.teal())
    
    counter = 1
    for anime in anime_list:
        value_text = '[' + anime.title + ']' + '(' + anime.url + ')'
        response.add_field(name = str(counter) + '.', value = value_text) # Counter variable helps with returning many anime titles in a row (1. 2. 3. etc)
        counter = counter + 1

    footer_text = 'From shinden.pl | Done in '
    execution_time = str(t.stop())
    response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

    await ctx.send(embed = response)



@bot.command(name='shindenmangalist', aliases=['sml', 'shindenml', 'shml', 'smangalist', 'shmangalist'], help = 'Returns a list of manga results')
async def shindenmangalist(ctx, *args):
    t.start()

    if args == ():
        help_string = ('**Command:** shindenmangalist\n'
            '**Description:** Returns a list of manga results\n'
            '**Aliases:** `sml, shindenml, shml, smangalist, shmangalist`\n'
            '**Usage:** `' + prefix + 'shindenmangalist (title)`\n'
            '**Parameters:** \n'
            '\t*title* (str)')

        return await ctx.send(help_string)

    title = ' '.join(args)

    manga_list = sh.search_titles(title, anime_or_manga = 'manga')
    color = discord.Colour(16777215)

    response = discord.Embed(title= '***Shinden manga list***', type = 'rich', description = 'Search results for: **' + title + '**', colour = color.teal())
    
    counter = 1
    for manga in manga_list:
        value_text = '[' + manga.title + ']' + '(' + manga.url + ')'
        response.add_field(name = str(counter) + '.', value = value_text)
        counter = counter + 1

    footer_text = 'From shinden.pl | Done in '
    execution_time = str(t.stop())
    response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

    await ctx.send(embed = response)



@bot.command(name = 'shindencharacter', aliases = ['sc', 'shindenc', 'shc', 'scharacter', 'shcharacter', 'sch', 'shindench', 'shch'], help = 'Returns a character result from shinden.pl')
async def shindencharacter(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindencharacter\n'
            '**Description:** Returns a character result from shinden.pl\n'
            '**Aliases:** `sc, shindenc, shc, scharacter, shcharacter, sch, shindench, shch`\n'
            '**Usage:** `' + prefix + 'shindencharacter (name) [which_result]`\n'
            '**Parameters:** \n'
            '\t*name* (str)\n'
            '\t*which_result* (int) - optional, default value = 1')

        return await ctx.send(help_string)

    t.start()

    if len(args) >= 2:
        args_list = list(args)
        which_result = 1
        possible_int = args_list.pop()

        try:
            which_result = int(possible_int)
        except:
            args_list.append(possible_int)

        name = ' '.join(args_list)

        character_list = sh.search_characters(name)
        try:
            character = character_list[which_result-1]
        except TypeError:
            t.stop()
            return await ctx.send('No results')
        except IndexError:
            await ctx.send('which_result param was too big, showing last result')
            character = character_list[-1]

        color = discord.Colour(16777215)
        
        if len(character.description) > 2000: # Description of discord embed must be under 2048 characters
            desc = character.description[:2000] + '...'
        else:
            desc = character.description

        response = discord.Embed(title = '***' + character.name + '***', type = 'rich', description = '`' + desc + '`', colour = color.dark_gold(), url = character.url)

        response.add_field(name = 'Gender', value = character.gender)
        response.add_field(name = 'Is historical', value = character.is_historical)
        response.add_field(name = 'Appearance list', value = (', '.join(character.appearance_list)), inline = False)

        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')
        
        await ctx.send(embed = response)

    else:
        name = ' '.join(args)

        character_list = sh.search_characters(name)
        try:
            character = character_list[0]
        except:
            t.stop()
            return await ctx.send('No result')
        
        color = discord.Colour(16777215)

        response = discord.Embed(title = '***' + character.name + '***', type = 'rich', description = '`' + character.description + '`', colour = color.dark_gold(), url = character.url)

        response.add_field(name = 'Gender', value = character.gender)
        response.add_field(name = 'Is historical', value = character.is_historical)
        response.add_field(name = 'Appearance list', value = (', '.join(character.appearance_list)), inline = False)

        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')
        
        await ctx.send(embed = response)



@bot.command(name = 'shindencharacterlist', aliases = ['scl', 'shindencl', 'shcl', 'scharacterlist', 'shcharacterlist', 'schl', 'shindenchl', 'shchl'], help = 'Responds with a list of character results')
async def shindencharacterlist(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindencharacterlist\n'
            '**Description:** Returns with a list of character results\n'
            '**Aliases:** `scl, shindencl, shcl, scharacterlist, schl, shindenchl, shchl`\n'
            '**Usage:** `' + prefix + 'shindencharacter (name)`\n'
            '**Parameters:** \n'
            '\t*name* (str)\n')

        return await ctx.send(help_string)

    t.start()

    name = ' '.join(args)

    character_list = sh.search_characters(name)
    color = discord.Colour(16777215)

    response = discord.Embed(title = '***Shinden character list***', type = 'rich', description = 'Search results for: **' + name + '**', colour = color.green())

    counter = 1
    for ch in character_list:
        
        info = '[**Appears in: **]' + '(' + ch.url + ')'
        for appear in ch.appearance_list:
            info = info + str(appear) + ', '
        
        response.add_field(name = '`' + str(counter) + '. ' + ch.name + '`', value = info[:-2], inline = False)
        counter = counter + 1
    
    footer_text = 'From shinden.pl | Done in '
    execution_time = str(t.stop())
    response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

    await ctx.send(embed = response)



@bot.command(name = 'shindenuser', aliases = ['su', 'shindenu', 'shu', 'suser', 'shuser'], help = 'Searches for a shinden user')
async def shindenuser(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindenuser\n'
            '**Description:** Searches for a shinden user\n'
            '**Aliases:** `su, shindenu, shc, shu, suser, shuser`\n'
            '**Usage:** `' + prefix + 'shindencharacter (nickname) [which_result]`\n'
            '**Parameters:** \n'
            '\t*nickname* (str)\n'
            '\t*which_result* (int) - optional, default value = 1')

        return await ctx.send(help_string)

    t.start()

    if len(args) >= 2:
        args_list = list(args)
        which_result = 1
        possible_int = args_list.pop()

        try:
            which_result = int(possible_int)
        except:
            args_list.append(possible_int)

        nickname = ' '.join(args_list)

        user_list = sh.search_users(nickname)
        try:
            user = user_list[which_result-1]
        except IndexError:
            await ctx.send('which_result param too big, showing last result')
            user = user_list[-1]
        except TypeError:
            t.stop()
            return await ctx.send('No results')

        color = discord.Colour(16777215)
        response = discord.Embed(title = '**' + user.nickname + '**', type = 'rich', colour = color.red(), url = user.url)
        
        response.add_field(name = 'Anime titles watched', value = '`' + str(user.anime_titles_watched) + '`')
        response.add_field(name = 'Anime hours watched', value = '`' + str(int(user.anime_minutes_watched/60)) + '`')
        response.add_field(name = 'Anime episodes watched', value = '`' + str(user.anime_episodes_watched) + '`')
        response.add_field(name = 'Average anime ratings', value = '`' + str(user.average_anime_ratings) + '`')
        response.add_field(name = 'Achievement count', value = '`' + str(user.achievement_count) + '`')
        response.add_field(name = 'Points', value = '`' + str(user.points) + '`')
        response.add_field(name = 'Last seen', value = '`' + str(user.last_seen.strftime('%H:%M %d.%m.%Y')) + '`')
        
        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

        await ctx.send(embed = response)
    
    else:
        nickname = ' '.join(args)

        user_list = sh.search_users(nickname)
        try:
            user = user_list[0]
        except TypeError:
            t.stop()
            return await ctx.send('No results')

        color = discord.Colour(16777215)
        response = discord.Embed(title = '**' + user.nickname + '**', type = 'rich', colour = color.red(), url = user.url)
        
        response.add_field(name = 'Anime titles watched', value = '`' + str(user.anime_titles_watched) + '`')
        response.add_field(name = 'Anime hours watched', value = '`' + str(int(user.anime_minutes_watched/60)) + '`')
        response.add_field(name = 'Anime episodes watched', value = '`' + str(user.anime_episodes_watched) + '`')
        response.add_field(name = 'Average anime ratings', value = '`' + str(user.average_anime_ratings) + '`')
        response.add_field(name = 'Achievement count', value = '`' + str(user.achievement_count) + '`')
        response.add_field(name = 'Points', value = '`' + str(user.points) + '`')
        response.add_field(name = 'Last seen', value = '`' + str(user.last_seen.strftime('%H:%M %d.%m.%Y')) + '`')
        
        footer_text = 'From shinden.pl | Done in '
        execution_time = str(t.stop())
        response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

        await ctx.send(embed = response)



@bot.command(name = 'shindenuserlist', aliases = ['sul', 'shindenul', 'shul', 'suserlist', 'shuserlist'], help = 'Lists shinden users found')
async def shindenuserlist(ctx, *args):
    if args == ():
        help_string = ('**Command:** shindenuserlist\n'
            '**Description:** Lists shinden users found\n'
            '**Aliases:** `sul, shindenul, shul, suserlist, shuserlist`\n'
            '**Usage:** `' + prefix + 'shindencharacterlist (nickname)`\n'
            '**Parameters:** \n'
            '\t*nickname* (str)\n')
        return await ctx.send(help_string)

    t.start()

    nickname = ' '.join(args)

    user_list = sh.search_users(nickname)
    color = discord.Colour(16777215)
    response = discord.Embed(title = '***Shinden user list***', type = 'rich', description = 'Search results for: ***' + nickname + '***', colour = color.purple()) 
    
    counter = 1
    for user in user_list: # Formatting the data using datatime's strftime method
        profile_hyperlink = '[Profile]' + '(' + user.url + ')'
        info = '**Last seen:** ' + user.last_seen.strftime('%H:%M %d.%m.%Y') + '\n' + '**Hours watched: **' + str(int(user.anime_minutes_watched/60)) + '\n' + profile_hyperlink

        response.add_field(name = '`' + str(counter) + '.' + user.nickname + '`', value = info, inline = False)
        counter = counter + 1
    
    footer_text = 'From shinden.pl | Done in '
    execution_time = str(t.stop())
    response.set_footer(text = footer_text + execution_time[:5] + ' seconds')

    await ctx.send(embed = response)



# Other commands



@bot.command(name = 'covid', aliases = ['ncov', 'covid19', 'coronavirus'])
async def covid(ctx):
    if cv.when_last_update() == 'never':
        cv.update()
    elif (datetime.now() - cv.when_last_update()) > timedelta(days=1): # if covid data hasnt been updated in 1 day, then update (in order to minimalise requests sent)
        cv.update()
    
    data = cv.read_data()

    # Creating two separate embeds for world and poland respectively
    color = discord.Colour(16777215)
    world_embed = discord.Embed(title = '**COVID-19 - World**', type = 'rich', colour = color.red(), url = 'https://worldometers.info/coronavirus/')
    
    world_embed.add_field(name = 'Cases', value = data['world'].cases)
    world_embed.add_field(name = 'Deaths', value = data['world'].deaths)
    world_embed.add_field(name = 'Recovered', value = data['world'].recovered)

    poland_embed = discord.Embed(title = '**COVID-19 - Poland**', type = 'rich', colour = color.red(), url = 'https://worldometers.info/coronavirus/country/poland')
    
    poland_embed.add_field(name = 'Cases', value = data['poland'].cases)
    poland_embed.add_field(name = 'Deaths', value = data['poland'].deaths)
    poland_embed.add_field(name = 'Recovered', value = data['poland'].recovered)
    
    world_embed.set_footer(text = 'Data from worldometers.info/coronavirus')
    poland_embed.set_footer(text = 'Data from worldometers.info/coronavirus')

    await ctx.send(embed = world_embed)
    await ctx.send(embed = poland_embed)



@bot.command(name = 'truth', help = 'This basically responds with dino earth image and nothing else')
async def truth(ctx):
    response = discord.Embed(title = 'The truth')
    response.set_image(url = 'https://pbs.twimg.com/profile_images/1116994465464508418/E9UB9VPx.png')

    await ctx.send(embed = response)



# Finally running the bot with our api key from settings.json
bot.run(api_key)