import discord
from discord import app_commands
from discord.ui import View, Select
import datetime, random, traceback, json, os
from html2image import Html2Image
hti = Html2Image()
config = json.load(open("config.json"))
current_directory = os.getcwd().replace('\\', '/')

class BoostPage:
    def __init__(self, nitro_type, authorname, authoravatar, authortext, receiveravatar, receivername, receivertext):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""

        self.nitro_type = nitro_type

        self.authorname = authorname
        self.authoravatar = authoravatar
        self.authortext = authortext
        self.sender_message_datetime = self.actual_datetime - datetime.timedelta(minutes=random.randint(1, 300))
        self.sender_message_datetime = self.sender_message_datetime.strftime('Today at %I:%M %p')

        self.receivername = receivername
        self.receiveravatar = receiveravatar
        self.receivertext = receivertext
        self.receiver_message_datetime = self.actual_datetime + datetime.timedelta(minutes=random.randint(1, 120))
        self.receiver_message_datetime = self.receiver_message_datetime.strftime('Today at %I:%M %p')
    
    def get_proof(self):
        filename = ""
        nitro_image = ""
        
        if self.nitro_type == "boost":
            filename = "assets/boost_page.txt"
            nitro_image = f"{current_directory}/assets/nitro_boost_preset.png"
        elif self.nitro_type == "classic":
            filename = "assets/classic_page.txt"
            nitro_image = f"{current_directory}/assets/nitro_classic_preset.png"
        elif self.nitro_type == "promo":
            filename = "assets/promo_page.txt"
            nitro_image = f"{current_directory}/assets/nitro_promo_preset.png"
        else:
            filename = "assets/boost_page.txt"
            nitro_image = f"{current_directory}/assets/nitro_boost_preset.png"

        with open(filename, 'r') as boost_page:
            self.proof = boost_page.read() \
                .replace('WHITNEYFONT', f"{current_directory}/assets/Whitneyfont.woff") \
                .replace('WHITNEYMEDIUM', f"{current_directory}/assets/Whitneymedium.woff") \
                .replace('AUTHORNAME', self.authorname) \
                .replace('AUTHORAVATAR', self.authoravatar) \
                .replace('AUTHORDATETIME', self.sender_message_datetime) \
                .replace('AUTHORTEXT', self.authortext) \
                .replace('USERNAME', self.receivername) \
                .replace('USERAVATAR', self.receiveravatar) \
                .replace('USERDATETIME', self.receiver_message_datetime) \
                .replace('USERTEXT', self.receivertext) \
                .replace('NITROCODE', ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))) \
                .replace('NITROIMAGESRC', nitro_image)

        return self.proof

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.tree.remove_command('help')

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.all()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/proof"))
    print(f"[CONNEXION] {client.user} ({client.user.id})")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(client.user.mention):
        await message.channel.send(f"{message.author.mention}, do /proof to get a Proof!")

class NitroProofCustom(discord.ui.Modal, title='Fake Nitro Proof System'):
    nitrotype = discord.ui.TextInput(
        label='Type of Nitro code:',
        style=discord.TextStyle.short,
        placeholder='Example: classic or boost or promo',
        required=True,
        max_length=7,
    )

    authortext = discord.ui.TextInput(
        label='Text presumed to be sent by you:',
        placeholder='Example: Congratulation! Here is ur code ',
        style=discord.TextStyle.long,
        required=False,
    )

    receivername = discord.ui.TextInput(
        label='Name of the receiver:',
        style=discord.TextStyle.short,
        placeholder='Example: Astraa',
        required=True,
        max_length=32,
    )

    receiveravatar = discord.ui.TextInput(
        label='Avatar link of the receiver:',
        style=discord.TextStyle.short,
        placeholder='Example: https://image.com/XXXXXXX.png',
        required=False,
    )

    receivertext = discord.ui.TextInput(
        label='Text presumed to be sent by the receiver:',
        style=discord.TextStyle.paragraph,
        placeholder='Example: OMG thx it\'s a real giveaway!',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.receiveravatar.value == "":
            self.receiveravatar_value = config["default_avatar"]
        else:
            self.receiveravatar_value = self.receiveravatar.value
        proof = BoostPage(self.nitrotype.value, interaction.user.display_name, interaction.user.avatar.url, self.authortext.value, self.receiveravatar_value, self.receivername.value, self.receivertext.value).get_proof()
        image = hti.screenshot(html_str=proof, size=(random.randint(730, 1000), random.randint(320, 340)), save_as='proof.png')
        
        await interaction.followup.send(f"Proof generated! Check your DMs.", ephemeral=True)
        await interaction.user.send(file=discord.File('proof.png'))
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong. Please try again.', ephemeral=True)
        traceback.print_tb(error.__traceback__)

class NitroProofId(discord.ui.Modal, title='Fake Nitro Proof System'):
    nitrotype = discord.ui.TextInput(
        label='Type of Nitro code:',
        style=discord.TextStyle.short,
        placeholder='Example: classic or boost or promo',
        required=True,
        max_length=7,
    )

    authortext = discord.ui.TextInput(
        label='Text presumed to be sent by you:',
        placeholder='Example: Congratulation! Here is ur code ',
        style=discord.TextStyle.long,
        required=False,
    )

    receiverid = discord.ui.TextInput(
        label='ID of the receiver:',
        style=discord.TextStyle.short,
        placeholder='Example: 464457105521508354',
        required=True,
        max_length=25,
    )

    receivertext = discord.ui.TextInput(
        label='Text presumed to be sent by the receiver:',
        style=discord.TextStyle.paragraph,
        placeholder='Example: OMG thx it\'s a real giveaway!',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            self.user = await client.fetch_user(int(self.receiverid.value))
            self.author_avatar = interaction.user.display_avatar.url if interaction.user.avatar else config["default_avatar"]
            self.receiver_avatar = self.user.display_avatar.url if self.user.avatar else config["default_avatar"]
            proof = BoostPage(self.nitrotype.value, interaction.user.name, self.author_avatar, self.authortext.value, self.receiver_avatar, self.user.name, self.receivertext.value).get_proof()
            image = hti.screenshot(html_str=proof, size=(random.randint(730, 1000), random.randint(320, 340)), save_as='proof.png')
            
            await interaction.followup.send(f"Proof generated! Check your DMs.", ephemeral=True)
            await interaction.user.send(file=discord.File('proof.png'))
        except Exception as e:
            await interaction.followup.send(f'Oops! {e}', ephemeral=True)
            return
        
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong. Please try again.', ephemeral=True)
        traceback.print_tb(error.__traceback__)


@client.tree.command(description='Generate a Giveaway Proof.')
@app_commands.describe(receiverinfo='Find the name/avatar of an account with an ID or Cutomize it')
@app_commands.choices(receiverinfo=[app_commands.Choice(name='Receiver ID', value='id'),app_commands.Choice(name='Custom Receiver', value='custom')])
async def proof(interaction: discord.Interaction, receiverinfo: str):
    if receiverinfo == 'custom':
        await interaction.response.send_modal(NitroProofCustom())
    elif receiverinfo == 'id':
        await interaction.response.send_modal(NitroProofId())


if __name__ == '__main__':
    client.run(config['bot_token'])
