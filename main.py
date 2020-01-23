import sys
sys.path.insert(1, '../py-jetanime')
import discord
from jetanime import getInfos, getAnimeList
import re
from urllib.parse import urljoin
from lib import average_colour_from_url
import time

TOKEN = 'NTI2NzY4NDYxNzcxNDQwMTI5.XiivCQ.Uy3I0fUKaf8_LWfnR1E8mUwS4H0'

global jetanime_url
jetanime_url = "https://www.jetanime.to/"

global search_emojis
search_emojis = {1:'1️⃣', 2:'2️⃣', 3:'3️⃣', 4:'4️⃣', 5:'5️⃣', 6:'6️⃣', 7:'7️⃣', 8:'8️⃣', 9:'9️⃣', 10:'🔟', '<':'⬅', '>':'➡', 'v':'✅'}

global temp_user_search
temp_user_search = list()

client = discord.Client()

@client.event
async def on_ready():
    channel = client.get_channel(432984228268081172)
    await channel.send('> Ready')

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.message.embeds[0].title == 'Searching...':

        # To delete any reaction from other than bot-master
        roles = [role.name.lower() for role in user.roles]
        if 'bot-master' in roles:
            pass
        else:
            await reaction.remove(user)

        temp = [reac.emoji for reac in reaction.message.reactions]
        index = temp.index('✅')
        temp = temp[:index + 1]
        if reaction.emoji not in temp:
            await reaction.remove(user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.author.id == 230563291146092545:
        if message.content == '!!shutdown':
            await client.logout()
        # if message.content == '!!test':
        #     channel = client.get_channel(439837382603309066)
        #     await channel.send('> Ready')

    for role in message.author.roles:
        if role.name.lower() == 'bot-master':

            comm = '!!jetanime'
            if message.content.startswith(comm):
                try:
                    url = message.content.replace(comm, '')
                    if url[:1] == ' ':
                        url = url[1:]
                    infos = getInfos(url)
                    infos = infos.anime()
                    image = infos['thumbnail']

                    color = average_colour_from_url(image)

                    embed=discord.Embed(title=infos['name'], type='rich', url=infos['link'], color=color)
                    embed.set_thumbnail(url=image)
                    embed.add_field(name="Original Name", value=infos['originalName'] , inline=False)
                    embed.add_field(name="Genres", value=', '.join(infos['genres']) , inline=False)
                    embed.add_field(name="Autors", value=', '.join(infos['autors']) , inline=False)
                    embed.add_field(name="Studios", value=', '.join(infos['studios']) , inline=False)
                    embed.add_field(name="Date", value=infos['date'] , inline=False)
                    embed.add_field(name="Synopsis", value=infos['synopsis'], inline=True)
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.send(sys.exc_info()[0])

            comm = '!!search '
            if message.content.startswith(comm):

                temp_user_search.append(message.channel.id)
                temp_user_search.append(message.author.id)

                search = re.search('!!search (.*)', message.content).group(1)
                await client.http.delete_message(message.channel.id, message.id)
                msg = await message.channel.send('Searching...')

                matching = list()
                animeList = getAnimeList()
                for content in animeList:
                    if search.lower() in content.lower():
                        matching.append(content)
                        matching.sort()

                N = 10
                matching = [matching[n:n+N] for n in range(0, len(matching), N)]
                # search = '\n'.join(matching)
                for idx, animes in enumerate(matching):
                    for i, anime in enumerate(animes):
                        animes[i] = [i + 1, anime]
                    matching[idx] = [idx + 1, animes]

                page1 = matching[0]
                color = average_colour_from_url(message.author.avatar_url)
                text = list()
                for elem in page1[1]:
                    text.append(f"[{elem[0]}] {elem[1]}")
                text = '\n'.join(text)
                embed=discord.Embed(title="Searching...", description=f"Search : {search}", type='rich', color=color)
                embed.add_field(name=f"Page {page1[0]}", value=text, inline=False)
                embed.set_footer(text=f"{len(matching)} pages")

                await msg.delete()
                msg = await message.channel.send(embed=embed)

                if page1[0] != 1:
                    await msg.add_reaction(emoji=search_emojis['<'])
                for num in page1[1]:
                    idx = num[0]
                    await msg.add_reaction(emoji=search_emojis[idx])
                if page1[0] == 1 and len(matching) > 1:
                    await msg.add_reaction(emoji=search_emojis['>'])
                if page1[0]:
                    await msg.add_reaction(emoji=search_emojis['v'])

                # # send_ = ', '.join(matching)[:2000]
                # # if send_:
                # await msg.delete()
                # 

                # else:
                #     msg = await message.channel.send('Bad search. Please retry..')
                #     time.sleep(2)
                #     await msg.delete()
            
            # comm = '!!test'
            # if message.content.startswith(comm):

if __name__ == "__main__":
    client.run(TOKEN)