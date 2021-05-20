import discord
from utils.db import db
async def _level_up_check_user(self, ctx, user):
    userinfo = db.users.find_one({"_id": user.id})
    titlesinfo = db.titles.find_one({"_id": user.id})
    if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
        userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
        userinfo["lvl"] = userinfo["lvl"] + 1
        userinfo["health"] = userinfo["MaxHealth"]
        em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
        await ctx.send(embed=em)
        if userinfo["exp"] >= 100 + ((userinfo["lvl"] + 1) * 3.5):
            userinfo["exp"] = userinfo["exp"] - (100 + ((userinfo["lvl"] + 1) * 3.5))
            userinfo["lvl"] = userinfo["lvl"] + 1
            userinfo["health"] = userinfo["MaxHealth"]
            em = discord.Embed(title=":tada: **{} gained a level!** :tada:".format(userinfo["name"]), color=discord.Colour(0xffd700))
            await ctx.send(embed=em)
        
    db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 10 and userinfo["friend_max_amount"] <= 15:
        userinfo["friend_max_amount"] = 15
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 25 and userinfo["friend_max_amount"] <= 20:
        userinfo["friend_max_amount"] = 15
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 50 and userinfo["friend_max_amount"] <= 25:
        userinfo["friend_max_amount"] = 25
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 75 and userinfo["friend_max_amount"] <= 30:
        userinfo["friend_max_amount"] = 30
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 100 and userinfo["friend_max_amount"] <= 35:
        userinfo["friend_max_amount"] = 35
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 125 and userinfo["friend_max_amount"] <= 40:
        userinfo["friend_max_amount"] = 40
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
        
    if userinfo["lvl"] >= 150 and userinfo["friend_max_amount"] <= 40:
        userinfo["friend_max_amount"] = 45
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
        
    if userinfo["lvl"] >= 175 and userinfo["friend_max_amount"] <= 45:
        userinfo["friend_max_amount"] = 50
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


    if userinfo["lvl"] >= 10 and userinfo["MaxHealth"] >= 102:
        userinfo["MaxHealth"] = 102
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 25 and userinfo["MaxHealth"] <= 104:
        userinfo["MaxHealth"] = 104
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 50 and userinfo["MaxHealth"] <= 106:
        userinfo["MaxHealth"] = 106
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 75 and userinfo["MaxHealth"] <= 108:
        userinfo["MaxHealth"] = 108
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 100 and userinfo["MaxHealth"] <= 110:
        userinfo["MaxHealth"] = 110
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 150 and userinfo["MaxHealth"] <= 120:
        userinfo["MaxHealth"] = 120
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 200 and userinfo["MaxHealth"] <= 130:
        userinfo["MaxHealth"] = 130
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 250 and userinfo["MaxHealth"] <= 140:
        userinfo["MaxHealth"] = 140
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 300 and userinfo["MaxHealth"] <= 150:
        userinfo["MaxHealth"] = 150
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 350 and userinfo["MaxHealth"] <= 160:
        userinfo["MaxHealth"] = 160
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 400 and userinfo["MaxHealth"] <= 170:
        userinfo["MaxHealth"] = 170
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 450 and userinfo["MaxHealth"] <= 180:
        userinfo["MaxHealth"] = 180
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)

    if userinfo["lvl"] >= 500 and userinfo["MaxHealth"] <= 190:
        userinfo["MaxHealth"] = 190
        db.users.replace_one({"_id": user.id}, userinfo, upsert=True)


    if userinfo["lvl"] >= 10 and not "Beginner" in titlesinfo["titles_list"]:
        newtitle = "Beginner"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 20 and not "Amateur" in titlesinfo["titles_list"]:
        newtitle = "Amateur"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 30 and not "Novice" in titlesinfo["titles_list"]:
        newtitle = "Novice"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 40 and not "Apprentice" in titlesinfo["titles_list"]:
        newtitle = "Apprentice"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["lvl"] >= 50 and not "Respected" in titlesinfo["titles_list"]:
        newtitle = "Respected"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["lvl"] >= 75 and not "Renowned" in titlesinfo["titles_list"]:
        newtitle = "Renowned"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["lvl"] >= 100 and not "Professional" in titlesinfo["titles_list"]:
        newtitle = "Professional"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["lvl"] >= 125 and not "Master" in titlesinfo["titles_list"]:
        newtitle = "Master"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
    
    if userinfo["lvl"] >= 150 and not "Grand-Master" in titlesinfo["titles_list"]:
        newtitle = "Grand-Master"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
    
    if userinfo["lvl"] >= 200 and not "Enlightened" in titlesinfo["titles_list"]:
        newtitle = "Enlightened"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 250 and not "Mighty" in titlesinfo["titles_list"]:
        newtitle = "Mighty"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 300 and not "Empowered" in titlesinfo["titles_list"]:
        newtitle = "Empowered"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 350 and not "Golden" in titlesinfo["titles_list"]:
        newtitle = "Golden"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 400 and not "Radiant" in titlesinfo["titles_list"]:
        newtitle = "Radiant"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 450 and not "Arcane" in titlesinfo["titles_list"]:
        newtitle = "Arcane"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 500 and not "Iridescent" in titlesinfo["titles_list"]:
        newtitle = "Iridescent"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 600 and not "Luminescent" in titlesinfo["titles_list"]:
        newtitle = "Luminescent"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 700 and not "Celestial" in titlesinfo["titles_list"]:
        newtitle = "Celestial"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 800 and not "Unbelievable" in titlesinfo["titles_list"]:
        newtitle = "Unbelievable"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["lvl"] >= 900 and not "Unreal" in titlesinfo["titles_list"]:
        newtitle = "Unreal"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 1000 and not "Godlike" in titlesinfo["titles_list"]:
        newtitle = "Godlike"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
        
    if userinfo["Rachikilled"] >= 100 and not "Rachi Killer" in titlesinfo["titles_list"]:
        newtitle = "Rachi Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Draugrkilled"] >= 100 and not "Draugr Killer" in titlesinfo["titles_list"]:
        newtitle = "Draugr Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Debinkilled"] >= 100 and not "Debin Killer" in titlesinfo["titles_list"]:
        newtitle = "Debin Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Stalkerkilled"] >= 100 and not "Stalker Killer" in titlesinfo["titles_list"]:
        newtitle = "Stalker Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["FireGolemkilled"] >= 100 and not "Fire Golem Killer" in titlesinfo["titles_list"]:
        newtitle = "Fire Golem Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Wyvernkilled"] >= 100 and not "Wyvern Killer" in titlesinfo["titles_list"]:
        newtitle = "Wyvern Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Ooferkilled"] >= 100 and not "Oofer Killer" in titlesinfo["titles_list"]:
        newtitle = "Oofer Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Souleaterkilled"] >= 100 and not "Souleater Killer" in titlesinfo["titles_list"]:
        newtitle = "Souleater Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Wolfkilled"] >= 100 and not "Wolf Killer" in titlesinfo["titles_list"]:
        newtitle = "Wolf Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Goblinkilled"] >= 100 and not "Goblin Killer" in titlesinfo["titles_list"]:
        newtitle = "Goblin Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Zombiekilled"] >= 100 and not "Zombie Killer" in titlesinfo["titles_list"]:
        newtitle = "Zombie Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["Phantasmkilled"] >= 100 and not "Phantasm Killer" in titlesinfo["titles_list"]:
        newtitle = "Phantasm Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["TheCorruptedkilled"] >= 100 and not "The Corrupted Killer" in titlesinfo["titles_list"]:
        newtitle = "The Corrupted Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["TheAccursedkilled"] >= 100 and not "The Accursed Killer" in titlesinfo["titles_list"]:
        newtitle = "The Accursed Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["ElderDragonkilled"] >= 100 and not "Elder Dragon Killer" in titlesinfo["titles_list"]:
        newtitle = "Elder Dragon Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                            
    if userinfo["Hadeskilled"] >= 100 and not "Hades Killer" in titlesinfo["titles_list"]:
        newtitle = "Hades Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["EbonyGuardiankilled"] >= 100 and not "Ebony Killer" in titlesinfo["titles_list"]:
        newtitle = "Ebony Guardian Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["Harpykilled"] >= 100 and not "Harpy Killer" in titlesinfo["titles_list"]:
        newtitle = "Harpy Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["Dormammukilled"] >= 100 and not "Dormammu Killer" in titlesinfo["titles_list"]:
        newtitle = "Dormammu Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["Ettinkilled"] >= 100 and not "Ettin Killer" in titlesinfo["titles_list"]:
        newtitle = "Ettin Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["TheNamelessKingkilled"] >= 100 and not "The Nameless King Killer" in titlesinfo["titles_list"]:
        newtitle = "The Nameless King Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
    if userinfo["Largoskilled"] >= 100 and not "Largos Killer" in titlesinfo["titles_list"]:
        newtitle = "Largos Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)			
        
    if userinfo["Deathclawkilled"] >= 100 and not "Deathclaw Killer" in titlesinfo["titles_list"]:
        newtitle = "Deathclaw Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Sauriankilled"] >= 100 and not "Saurian Killer" in titlesinfo["titles_list"]:
        newtitle = "Saurian Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                
    if userinfo["TheVenomouskilled"] >= 100 and not "The Venomous Killer" in titlesinfo["titles_list"]:
        newtitle = "The Venomous Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Skeletonkilled"] >= 100 and not "Skeleton Killer" in titlesinfo["titles_list"]:
        newtitle = "Skeleton Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Lizardmenkilled"] >= 100 and not "Lizardmen Killer" in titlesinfo["titles_list"]:
        newtitle = "Lizardmen Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["Giantkilled"] >= 100 and not "Giant Killer" in titlesinfo["titles_list"]:
        newtitle = "Giant Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["DeathKnightkilled"] >= 100 and not "Death Knight Killer" in titlesinfo["titles_list"]:
        newtitle = "Death Knight Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["IceWolveskilled"] >= 100 and not "Ice Wolves Killer" in titlesinfo["titles_list"]:
        newtitle = "Ice Wolves Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["FrostOrckilled"] >= 100 and not "Frost Orc Killer" in titlesinfo["titles_list"]:
        newtitle = "Frost Orc Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["FrostGoblinkilled"] >= 100 and not "Frost Goblin Killer" in titlesinfo["titles_list"]:
        newtitle = "Frost Goblin Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["FrostDragonkilled"] >= 100 and not "Frost Dragon Killer" in titlesinfo["titles_list"]:
        newtitle = "Frost Dragon Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
    
    if userinfo["enemieskilled"] >= 500 and not "Monster Slayer" in titlesinfo["titles_list"]:
        newtitle = "Monster Slayer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["enemieskilled"] >= 1000 and not "Monster Hunter" in titlesinfo["titles_list"]:
        newtitle = "Monster Hunter"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["enemieskilled"] >= 2000 and not "Monster Killer" in titlesinfo["titles_list"]:
        newtitle = "Monster Killer"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["enemieskilled"] >= 4000 and not "Monster Executioner" in titlesinfo["titles_list"]:
        newtitle = "Monster Executioner"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["enemieskilled"] >= 8000 and not "Monster Exterminator" in titlesinfo["titles_list"]:
        newtitle = "Monster Exterminator"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)


    if userinfo["deaths"] >= 15 and not "Uncoordinated" in titlesinfo["titles_list"]:
        newtitle = "Uncoordinated"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)	
                
    if userinfo["deaths"] >= 30 and not "Unhandy" in titlesinfo["titles_list"]:
        newtitle = "Unhandy"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                        
    if userinfo["deaths"] >= 60 and not "Clumsy" in titlesinfo["titles_list"]:
        newtitle = "Clumsy"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                        
    if userinfo["deaths"] >= 90 and not "Unskillful" in titlesinfo["titles_list"]:
        newtitle = "Unskillful"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)
                        
    if userinfo["deaths"] >= 120 and not "Inexpert" in titlesinfo["titles_list"]:
        newtitle = "Inexpert"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["deaths"] >= 999 and not "I'm playing the game wrong..." in titlesinfo["titles_list"]:
        newtitle = "I'm playing the game wrong..."
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)



    if userinfo["gold"] == 0 and not "Broke" in titlesinfo["titles_list"]:
        newtitle = "Broke"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["gold"] >= 500 and not "Poor" in titlesinfo["titles_list"]:
        newtitle = "Poor"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["gold"] >= 10000 and not "Rich" in titlesinfo["titles_list"]:
        newtitle = "Rich"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["gold"] >= 100000 and not "Wealthy" in titlesinfo["titles_list"]:
        newtitle = "Wealthy"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["gold"] >= 1000000 and not "Millionaire" in titlesinfo["titles_list"]:
        newtitle = "Millionaire"
        if not newtitle in titlesinfo["titles_list"]:
            titlesinfo["titles_list"].append(newtitle)
            titlesinfo["titles_amount"] = titlesinfo["titles_amount"] + 1
            db.titles.replace_one({"_id": user.id}, titlesinfo, upsert=True)
            em = discord.Embed(title="New Title", description=newtitle, color=discord.Colour(0x00ff00))
            try:
                await user.send(embed=em)
            except:
                await ctx.send(embed=em)

    if userinfo["lvl"] >= 30:
        if userinfo["class"] == "Thief":
            options = ["Rogue", "rogue", "Mesmer", "mesmer"]
            em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
            em.add_field(name="<:Mesmer:639473407401918485> Mesmer", value="Master of confusion and movement", inline=False)
            em.add_field(name="<:Rogue:639473412221304842> Rogue", value="Quick and brutal attacks", inline=False)
            await ctx.send(embed=em)

            answer = await self.check_answer(ctx, options)
            if answer == "Rogue" or answer == "rogue":
                spechoice = "Rogue"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Parry")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

            elif answer == "Mesmer" or answer == "mesmer":
                spechoice = "Mesmer"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Distort")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

        elif userinfo["class"] == "Mage":
            options = ["Necromancer", "necromancer", "Elementalist", "elementalist"]
            em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
            em.add_field(name="<:Elementalist:639473417376235551> Elementalist", value="Controll all the elements", inline=False)
            em.add_field(name="<:Necromancer:639473415295860767> Necromancer", value="Wield the power of the dead", inline=False)
            await ctx.send(embed=em)

            answer = await self.check_answer(ctx, options)
            if answer == "Necromancer" or answer == "necromancer":
                spechoice = "Necromancer"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Reap")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

            elif answer == "Elementalist" or answer == "elementalist":
                spechoice = "Elementalist"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Overload")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

        elif userinfo["class"] == "Knight":
            options = ["Samurai", "samurai", "Paladin", "paladin"]
            em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
            em.add_field(name="<:Paladin:639473415257980938> Paladin", value="Brutal attacks", inline=False)
            em.add_field(name="<:Samurai:639473412028497940> Samurai", value="Defensive playstile", inline=False)
            await ctx.send(embed=em)

            answer = await self.check_answer(ctx, options)
            if answer == "Paladin" or answer == "paladin":
                spechoice = "Paladin"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Fusillade")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

            elif answer == "Samurai" or answer == "samurai":
                spechoice = "Samurai"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Protrude")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

        elif userinfo["class"] == "Archer":
            options = ["Assassin", "assassin", "Ranger", "ranger"]
            em = discord.Embed(title=":military_medal: Specialization!", description="Please choose a specialization:", color=discord.Colour(0xffffff))
            em.add_field(name="<:Assassin:639473417791209472> Assassin", value="High damage but low health", inline=False)
            em.add_field(name="<:Ranger:639473419930304513> Ranger", value="Always sure to hit for a decent amount of damage", inline=False)
            await ctx.send(embed=em)

            answer = await self.check_answer(ctx, options)
            if answer == "Ranger" or answer == "ranger":
                spechoice = "Ranger"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Strike")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))

            elif answer == "Assassin" or answer == "assassin":
                spechoice = "Assassin"
                userinfo["class"] = spechoice
                userinfo["skills_learned"].append("Corrupt")
                db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
                await ctx.send("You are now a {}!\nGood luck on the rest of your journey.".format(spechoice))



    if userinfo["lvl"] >= 90:
        if userinfo["class"] == "Rogue":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a High Rogue", color=discord.Colour(0xffffff))
            em.add_field(name="<:Rogue:639473412221304842> High Rogue", value="faster and deadlier attacks.", inline=False)
            await ctx.send(embed=em)
            spechoice = "High Rogue"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Rupture")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Mesmer":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become an Adept Mesmer!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Mesmer:639473407401918485> Adept Mesmer", value="Master of confusion, illusion and movement.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Adept Mesmer"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Warp")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Necromancer":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Developed Necromancer!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Necromancer:639473415295860767>  Developed Necromancer", value="Master of The dead.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Developed Necromancer"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Arise")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Elementalist":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Adequate Elementalist!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Elementalist:639473417376235551> Adequate Elementalist", value="Master the air element.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Adequate Elementalist"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Surge")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Samurai":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Master Samurai!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Samurai:639473412028497940> Master Samurai", value="Master of The Sword.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Master Samurai"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Slice")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Paladin":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Grand Paladin!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Paladin:639473415257980938> Grand Paladin", value="Respected amongst Knights and Paladins.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Grand Paladin"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Blockade")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            

        if userinfo["class"] == "Assassin":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Night Assassin!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Assassin:639473417791209472> Night Assassin", value="One with the night.", inline=False)
            await ctx.send(embed=em)
            spechoice = "Night Assassin"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Sneak")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            
            
        if userinfo["class"] == "Ranger":
            em = discord.Embed(title=":military_medal: You reached an advancement!", description="You have now become a Skilled Ranger!", color=discord.Colour(0xffffff))
            em.add_field(name="<:Ranger:639473419930304513> Skilled Ranger", value="Most skilled with the bow out of all classes!", inline=False)
            await ctx.send(embed=em)
            spechoice = "Skilled Ranger"
            userinfo["class"] = spechoice
            userinfo["skills_learned"].append("Snipe")
            db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
            
    


    db.users.replace_one({"_id": user.id}, userinfo, upsert=True)
