import discord, discord.ext, os, discord_slash, flask, threading

## bot ##

targets = ['h0nde', 'metamask support']

intents = discord.Intents().default()
intents.members = True
bot = discord.ext.commands.Bot(command_prefix='/', intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

async def check_account(member):
    is_h0nde = member.id is not bot.user.id and any([target in member.name.lower() for target in targets])
    if is_h0nde:
        print(f'Banning {member.name} from {member.guild.name}...')
        await member.guild.ban(member, reason='h0nde spam account')
        print(f'Banned {member.name} from {member.guild.name}.')
    return is_h0nde

@bot.event
async def on_ready():
    print('Bot is running.')
    await bot.change_presence(activity=discord.Game(name='https://96lb.ml/h0ndeliminator'))

@bot.event
async def on_member_join(member):
    await check_account(member)

@slash.slash(
    name='ban',
    description='Bans all h0nde accounts currently on the server.',
)
async def ban(ctx):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send('You must have the "ban members" permission to run this command.')
        return
    await ctx.defer()
    count = 0
    for member in ctx.guild.members:
        if await check_account(member):
            count += 1
    await ctx.send(f'Banned {count} members.')

## webserver ##

app = flask.Flask('')

@app.route('/')
def main():
    return 'h0ndeliminator is running!'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = threading.Thread(target=run)
    server.start()

## main ##

keep_alive()
bot.run(os.getenv('TOKEN'))