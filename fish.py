import discord
import random
import datetime

def intCheck(s):
	b = True
	for i in range(len(s)):
		if(s[i]<'0')or(s[i]>'9'):
			b = False
			break
	return b

client = discord.Client()
prefix = '$'
fishin = ['Radical Fish','Bass','Salmon']
fishers = []
sdvig = 1
channeru = None
mesage = None
reaktu = None 
IDlen = 18

@client.event
async def on_ready():
	global channeru
	global mesage
	global reaktu
	channeru = client.get_channel(701003097601867817)
	mesage = channeru.last_message
	reaktu = discord.utils.get(client.emojis, id=746762370864513075)
	print('We have logged in as {0.user}'.format(client))
	

@client.event
async def on_reaction_add(reaction, user):
	#if(reaction.me):	#want to add $stats for checking emojis
	await reaction.remove(client.user)	#should delete bot reactions if I react
	#works on messages written while bot was working
	#clear_reaction clears all reactions with that emoji, remove removes reaction from that user
	
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if (message.channel.id==674679001582665728)or(message.channel.id==701003097601867817):#for using by me for only my purposes.edit:for using in special places for that
		if message.content.startswith(prefix):
			if message.content.startswith(prefix+'hello'):	#no one uses it,used for test
				await message.channel.send('Hello!')
			elif message.content.startswith(prefix+'print'):
				await message.channel.send('```'+message.conten[6:]t+'```')
			elif message.content.startswith(prefix+'fish'):	#no one uses it
				i = 0
				if len(fishers)!=0:
					for i in range(len(fishers)):
						if fishers[i][0] == message.author.id:
							break
					if fishers[i][0] != message.author.id:
						fishers.append([message.author.id,0,0,0]) #,(datetime.date.year*365+datetime.date.month*31+datetime.date.day)*24+datetime.time.hour+6
						i += 1
				else:
					fishers.append([message.author.id,0,0,0])#,(datetime.date.year*365+datetime.date.month*31+datetime.date.day)*24+datetime.time.hour+6
			#	if (fishers[i][1]<(time.datetime.date.year*365+time.datetime.date.month*31+time.datetime.day)*24+datetime.time.hour):
					f1 = random.randint(0,3)
					await message.channel.send("You caught "+fishin[f1]+", now you have "+str(fishers[i][f1+sdvig]+1)+" of them")
					fishers[i][f1+sdvig] += 1
			#		fishers[i][1] = (datetime.date.year*365+datetime.date.month*31+datetime.date.day)*24+datetime.time.hour+6
			#	else:
			#		await message.channel.send("Don't hurry, wait "+str(fishers[i][1]-(datetime.date.year*365+datetime.date.month*31+datetime.day)*24+datetime.time.hour)+" hours")
			elif message.content.startswith(prefix+'inv'):	#no one uses it
				if len(fishers) == 0:
					await message.channel.send("No one here has any fish")
				else:
					for i in range(len(fishers)):
						if fishers[i][0] == message.author.id:
							break
					if fishers[i][0] == message.author.id:
						l = 'You have '
						for j in range(len(fishin)):
							l += str(fishers[i][j+sdvig])+'x'+fishin[j]+', '
						await message.channel.send(l)
					else:
						await message.channel.send("It seems you haven't caught any fish. Use 'fish' command to catch your first")
			#elif message.content.startswith(prefix+'newprefix'):
			#	await message.channel.send("Set new prefix:")
			#	prefix = str(input())
			elif message.content.startswith(prefix+'react'):	#reworked:you can set channel,message, emoji in any order:
			#channel:id,name,mention,last used channel(empty),channel where message was sent(error)
			#message:id,content,"content",sender id,sender name,sender nick,sender ping,pre-last message(empty or error)
			#emoji:id,name,using emoji,previous emoji(empty),error emoji(i cant put yer dumb emoji)
				global channeru
				global mesage
				global reaktu
				l = ''
				if len(message.content)>7:
					l = message.content[6:]
				spisok = []
				state = 0
				isWord = False
				msgContent = False
				wasContent = False
				for i in range(len(l)):
					if((l[i]=='"')and(not isWord)and(not wasContent))or(msgContent)or((l[i]!=' ')and(l[i]!='"')):
						if(not isWord):
							spisok.append('')
							isWord = True
						spisok[state] += l[i]
						if(l[i]=='"'):
							if(msgContent):
								msgContent = False
								wasContent = True
								isWord = False
								state +=1
							else:
								msgContent = True
								isWord = True
						elif(not isWord):
							isWord = True
					elif(l[i]==' ')and(isWord):
						state += 1
						isWord = False
				#defining
				channeruFound = -1
				mesageFound = -1
				reaktuFound = -1
				for i in range(len(spisok)):
					if(mesageFound==-1)and(spisok[i][0]=='"')and(spisok[i][-1]=='"'):
						mesageFound = i
						spisok[i] = spisok[i][1:-1]
						print('Message set 1')
					elif(len(spisok[i])>=IDlen)and(intCheck(spisok[i])):
						if(client.get_channel(int(spisok[i]))!=None)and(channeruFound==-1):
							channeruFound = i
							print('Channel set 1')
						elif(discord.utils.get(client.emojis,id=int(spisok[i]))!=None)and(reaktuFound==-1):
							reaktuFound = i
							print('Emoji set 1')
						elif(mesageFound==-1):
							mesageFound = i
							print('Message set 2')
					elif(spisok[i][0:2]=='<:')and(spisok[i][-1]=='>')and(reaktuFound==-1):
						reaktuFound = i
						print('Emoji set 2')
					elif(spisok[i][:2]=='<#')and(spisok[i][-1]=='>')and(intCheck(spisok[i][2:-1]))and(len(spisok[i][2:-1])>=IDlen)and(channeruFound==-1):
						channeruFound = i
						spisok[i] = spisok[i][2:-1]
						print('Channel set 2')
					elif(spisok[i][:3]=='<@!')and(spisok[i][-1]=='>')and(intCheck(spisok[i][3:-1]))and(len(spisok[i][3:-1])>=IDlen)and(mesageFound==-1):
						mesageFound = i
						print('Message set 3')
					elif(reaktuFound==-1)and(discord.utils.get(client.emojis,name=spisok[i])!=None):
						reaktuFound = i
						print('Emoji set 3')
					elif(channeruFound==-1):
						chan = None
						for j in client.get_all_channels():
							if j.name==spisok[i]:
								chan = await client.fetch_channel(j.id)
								break
						if(chan!=None):
							channeruFound = i
							print('Channel set 3')
						elif(mesageFound==-1):
							mesageFound = i
							print('Message set 4')
						else:
							spisok.append('])])])])])])])])])])])])])])])])])])])])')
							channeruFound = len(spisok)-1
							mesageFound = len(spisok)-1
							reaktuFound = len(spisok)-1
							print('Unable to set 1')
							break
					elif(mesageFound==-1):
						mesageFound = i
						print('Message set 5')
					else:
						spisok.append('])])])])])])])])])])])])])])])])])])])])')
						channeruFound = len(spisok)-1
						mesageFound = len(spisok)-1
						reaktuFound = len(spisok)-1
						print('Unable to set 2')
						break
				#defining what string where to put
				channeruStr = ''
				mesageStr = ''
				reaktuStr = ''
				if(channeruFound!=-1):
					channeruStr = spisok[channeruFound]
				if(mesageFound!=-1):
					mesageStr = spisok[mesageFound]
				if(reaktuFound!=-1):
					reaktuStr = spisok[reaktuFound]
				#setting 'Str's
				if(channeruStr!='')and(intCheck(channeruStr))and(len(channeruStr)>=IDlen):
					channeru = await client.fetch_channel(int(channeruStr))
				elif(channeruStr!=''):
					channeru = None
					for chanel in client.get_all_channels():
						if chanel.name==channeruStr:
							channeru = await client.fetch_channel(chanel.id)
							break
				if(channeru==None):
					channeru = message.channel
				#channels are OK
				if(mesageStr!='')and(intCheck(mesageStr))and(len(mesageStr)>=IDlen):
					mesage = await channeru.fetch_message(int(mesageStr))
					if(mesage==None):
						yuzeru = discord.utils.get(message.guild.members,name=mesageStr)
						if(yuzeru==None):
							yuzeru = discord.utils.get(message.guild.members,nick=mesageStr)
						if(yuzeru!=None):
							for i in range(len(client.cached_messages)-1,0,-1):
								if(client.cached_messages[i].user.id==yuzeru.id)and(client.cached_messages[i].channel==channeru)and(client.cached_messages[i]!=message):
									mesage = client.cached_messages[i]
									break
				elif(mesageStr[:3]=='<@!')and(mesageStr[-1]=='>')and(intCheck(mesageStr[3:-1]))and(len(mesageStr[3:-1])>=IDlen):
					yuzeru = discord.utils.get(message.guild.members,name=mesageStr[3:-1])
					if(yuzeru!=None):
						for i in range(len(client.cached_messages)-1,0,-1):
							if(client.cached_messages[i].user.id==yuzeru.id)and(client.cached_messages[i].channel==channeru)and(client.cached_messages[i]!=message):
								mesage = client.cached_messages[i]
								break
					else:
						mesage = None
				elif(mesageStr!=''):
					mesage = None
					for i in range(len(client.cached_messages)-1,0,-1):
						if(client.cached_messages[i].channel==channeru)and(mesageStr in client.cached_messages[i].content)and(client.cached_messages[i]!=message):
							mesage = await channeru.fetch_message(client.cached_messages[i].id)
							break
					if(mesage==None):
						yuzeru = discord.utils.get(message.guild.members,name=mesageStr)
						if(yuzeru==None):
							yuzeru = discord.utils.get(message.guild.members,nick=mesageStr)
						if(yuzeru!=None):
							for i in range(len(client.cached_messages)-1,0,-1):
								if(client.cached_messages[i].user.id==yuzeru.id)and(client.cached_messages[i].channel==channeru)and(client.cached_messages[i]!=message):
									mesage = client.cached_messages[i]
									break
				if(mesageStr=='')or(mesage==None):
					for i in range(len(client.cached_messages)-1,0,-1):
						if(client.cached_messages[i]!=message)and(client.cached_messages[i].channel==channeru):
							mesage = await channeru.fetch_message(client.cached_messages[i].id)
							break
				#messages are OK,needs testing after thousands of messages
				if(reaktuStr!='')and(intCheck(reaktuStr))and(len(reaktuStr)>=IDlen):
					reaktu = discord.utils.get(client.emojis, id=int(reaktuStr))
				elif(reaktuStr!='')and(reaktuStr[0:2]=='<:'):
					for i in range(2,len(reaktuStr)):
						if(reaktuStr[i]!='_')and((reaktuStr[i]<'0')or(reaktuStr[i]>'9'))and((reaktuStr[i]<'a')or(reaktuStr[i]>'z'))and((reaktuStr[i]<'A')or(reaktuStr[i]>'Z')):
							reaktuStr = reaktuStr[2:i]
							break
					reaktu = discord.utils.get(client.emojis, name=reaktuStr)
				elif(reaktuStr!=''):
					j = 0
					for i in range(len(reaktuStr)):
						if(reaktuStr[i-j]!='_')and((reaktuStr[i-j]<'0')or(reaktuStr[i-j]>'9'))and((reaktuStr[i-j]<'a')or(reaktuStr[i-j]>'z'))and((reaktuStr[i-j]<'A')or(reaktuStr[i-j]>'Z')):
							reaktuStr=reaktuStr[0:i]+reaktuStr[i+1:]
							j += 1
					reaktu = discord.utils.get(client.emojis, name=reaktuStr)
				if(reaktu==None):
					reaktu = discord.utils.get(client.emojis, id=747176918406791199)
				#reactions are almost OK,but can't send non-custom emojis
				await mesage.add_reaction(reaktu)
			elif message.content.startswith(prefix+'emojisy'):	#rework this command:bad design
				for i in range(len(client.emojis)):
					await message.channel.send(client.emojis[i].name+' '+str(client.emojis[i].id)+' '+client.get_guild(client.emojis[i].guild_id).name)
			elif message.content.startswith(prefix+'version'):	#doesn't work for unknown reason
				l = discord.__version__							#don't need this command,can add in any moment
				await message.channel.send(l)
			elif message.content.startswith(prefix+'labyrinth'):#rework this command#something still wrong here:sometimes it creates labyrinths that have no way out
				map=[[6 for i in range(7)] for i in range(7)]
				map2=[[True for i in range(7)] for i in range(7)]
				for i in range(1,6):
					for j in range(1,6):
						if(i==1)and(j==1):map[i][j]=1
						else:map[i][j]=0
				for i in range(1,6):
					for j in range(1,6):
						map2[i][j]=False
				cells=24;x=1;y=1;c=0
				while (cells!=0):
					while(map[x][y]!=0):
						x=random.randint(1,5)
						y=random.randint(1,5)
					map[x][y]=random.randint(1,4)
					if((map2[x-1][y])and(map2[x+1][y])and(map2[x][y-1])and(map2[x][y+1])): #checks if its trapped in itself. while cycle below does the same. if it happens, we return to the cell that directs at this cell and trying to redirect it not at itself. its poor-written and it can get out definitely successfuly only by one cell. i hope algorythm wont need improvement(unfortunately it needs:every second labyrinth traps San inside itself)
						c=0	#c system:c is the direction where is positioned previous cell,so you wont return to it
						while((map2[x-1][y])and(map2[x+1][y])and(map2[x][y-1])and(map2[x][y+1])):
							if(map[x-1][y]==3)and(c!=1):
								map[x][y]=1
								x=x-1
								c=3
							elif(map[x][y-1]==4)and(c!=2):
								map[x][y]=2
								y=y-1
								c=4
							elif(map[x+1][y]==1)and(c!=3):
								map[x][y]=3
								x=x+1
								c=1
							elif(map[x][y+1]==2)and(c!=4):
								map[x][y]=4
								y=y+1
								c=2
					while((((x==1)and(map[x][y]==1))or((y==1)and(map[x][y]==2))or((x==5)and(map[x][y]==3))or((y==5)and(map[x][y]==4)))or(((map[x][y]==1)and(map2[x-1][y]))or((map[x][y]==2)and(map2[x][y-1]))or((map[x][y]==3)and(map2[x+1][y]))or((map[x][y]==4)and(map2[x][y+1])))):	#let me explain:x==1 and map[xy]==1 or etc until y==5 and map[xy]==4 checks is that cell directs at wall.map[xy]==1 and map2[x-1y] etc until the end checks if that cell directs at its part, so it shouldnt get cycled
							map[x][y]=random.randint(1,4)
					cells=cells-1
					map2[x][y]=True
					if(map[x][y]==1):x=x-1
					elif(map[x][y]==2):y=y-1
					elif(map[x][y]==3):x=x+1
					elif(map[x][y]==4):y=y+1
					if((x==1)and(y==1))or(((map[x][y]==1)and(map[x-1][y]!=0))or((map[x][y]==2)and(map[x][y-1]!=0))or((map[x][y]==3)and(map[x+1][y]!=0))or((map[x][y]==4)and(map[x][y+1]!=0))):	#if it reaches exit(1,1) or struck at something. we dont check if its wall or itself, because we did it earlier
						x=random.randint(1,5)
						y=random.randint(1,5)
						map2=[[True for i in range(7)] for i in range(7)]
						for i in range(1,6):
							for j in range(1,6):
								map2[i][j]=False
			#	l=""							#testing function
			#	for i in range(7):
			#		for j in range(7):
			#			l=l+str(map[i][j])
			#		l=l+"\n"
			#	await message.channel.send(l) 	#output of testing
				lab=[['0' for i in range(13)] for i in range(13)]
				for i in range(2,11,2):
					for j in range(2,11,2):
						if(map[i//2][j//2]==1):
							if (lab[i-1][j]!='#'):
								lab[i-1][j]='#'
							if (lab[i+1][j]!='#'):
								lab[i+1][j]='0'
							if (lab[i][j-1]!='#'):
								lab[i][j-1]='0'
							if (lab[i][j+1]!='#'):
								lab[i][j+1]='0'
						if (map[i//2][j//2]==2):
							if (lab[i-1][j]!='#'):
								lab[i-1][j]='0'
							if (lab[i+1][j]!='#'):
								lab[i+1][j]='0'
							if (lab[i][j-1]!='#'):
								lab[i][j-1]='#'
							if (lab[i][j+1]!='#'):
								lab[i][j+1]='0'
						if (map[i//2][j//2]==3):
							if (lab[i-1][j]!='#'):
								lab[i-1][j]='0'
							if (lab[i+1][j]!='#'):
								lab[i+1][j]='#'
							if (lab[i][j-1]!='#'):
								lab[i][j-1]='0'
							if (lab[i][j+1]!='#'):
								lab[i][j+1]='0'
						if (map[i//2][j//2]==4):
							if (lab[i-1][j]!='#'):
								lab[i-1][j]='0'
							if (lab[i+1][j]!='#'):
								lab[i+1][j]='0'
							if (lab[i][j-1]!='#'):
								lab[i][j-1]='0'
							if (lab[i][j+1]!='#'):
								lab[i][j+1]='#'
						lab[i][j]='#'
				for i in range(1,12):
					for j in range(1,12):
						if (lab[i][j] == '#'):
							lab[i][j] = ' '
						else:
							lab[i][j] = '█'
				l=""
				for i in range(1,12):
					for j in range(1,12):
						if(i==10)and(j==10):
							l=l+'<:SanCheese:688076226451341380>'
						elif(lab[i][j]==' '):
							l=l+lab[i][j]*3
						else:
							l=l+lab[i][j]
						if(j%2==0)and(not((i==10)and(j==10))):
							if(lab[i][j]==' '):
								l=l+lab[i][j]*3
							else:
								l=l+lab[i][j]
					l=l+'\n'
				await message.channel.send(l)
			elif message.content.startswith(prefix+'exit'):		#useful for quit,doesn't need reworking
				await client.logout()
				print("Bot has been logged out")
			elif message.content.startswith(prefix+'hawaii'):	#autoreact fish-bag-goto-palm
			#	671827822607859712-fish
			#	746762370864513075-bag
			#	671416950341238795-goto
			#	752218210555658381-palm
				channeruId = int(message.content[8:26])	#see $react
				mesageId = int(message.content[27:45])
				channeru = client.get_channel(channeruId)
				mesage = await channeru.fetch_message(mesageId)
				await mesage.add_reaction(discord.utils.get(client.emojis, id=671827822607859712))
				await mesage.add_reaction(discord.utils.get(client.emojis, id=746762370864513075))
				await mesage.add_reaction(discord.utils.get(client.emojis, id=671416950341238795))
				await mesage.add_reaction(discord.utils.get(client.emojis, id=752218210555658381))
			elif message.content.startswith(prefix+'durka'):	#autoreact SanEatar-goto-durka
			#	759483429602459648-SanEatar
				channeruId = int(message.content[7:25])	#see $react, but -1 to positions
				mesageId = int(message.content[26:44])
				channeru = client.get_channel(channeruId)
				mesage = await channeru.fetch_message(mesageId)
				await mesage.add_reaction(discord.utils.get(client.emojis, id=759483429602459648))
				await mesage.add_reaction(discord.utils.get(client.emojis, id=671416950341238795))
				await mesage.add_reaction('🏥')	#yeah,it's how it works
			elif message.content.startswith(prefix+'lefter'):	#autoreact pointAtAvatar-goto-fire
			#	764223528492204083-SanCheeseTam2
				channeruId = int(message.content[8:26])	#see $react
				mesageId = int(message.content[27:45])
				channeru = client.get_channel(channeruId)
				mesage = await channeru.fetch_message(mesageId)
				await mesage.add_reaction(discord.utils.get(client.emojis, id=764223528492204083))
				await mesage.add_reaction(discord.utils.get(client.emojis, id=671416950341238795))
				await mesage.add_reaction('🔥')	#yeah,it's how it works
#			else:
#				await message.channel.send("Try another commands\n'hello' - bot will say hello in respond\n'fish' - here you can fish\n'inv' - shows your fish")
#		else:
#			await message.channel.send("Shhh! Don't frighten off fish!")
client.run('No token for you, use your own')
#TODO:labyrinth generator(almost done)(needs reworking),ASCII Art maker(not there),description generator(maybe not there),emojis in messages and reacts of last messages counter,based on that stats,help about my bot
