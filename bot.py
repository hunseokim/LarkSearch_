from ast import alias
import asyncio
from cgi import print_directory
from codecs import register_error
from email import message
from logging import info
from typing import ContextManager
from aiohttp import request
import discord
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib import parse
from discord.ext import commands
import random
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime
import pytz

bot = commands.Bot(command_prefix = '!', help_command = None)

# 아래는 봇이 구동되었을 때 동작하는 부분
@bot.event
async def on_ready():
    print("Logged in as ",bot.user.name,bot.user.id)
    await bot.change_presence(activity=discord.Game(name='!도움말'))

#검색      
@bot.command(aliases=['정보','캐릭터','캐릭'])
async def 검색(ctx, context) :
    if ctx.author.bot:
        return None
    name=parse.quote(f'{context}') #입력된 캐릭터 닉네임
    
    #전투정보실 검색
    try:
        #전투정보실 PC 검색
        larkpcurl="https://lostark.game.onstove.com/Profile/Character/"+name
        larkpchtml=urlopen(larkpcurl)
        larkpcsoup=BeautifulSoup(larkpchtml,"html.parser")
    except:
        raise
    else:
        firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **검색중입니다. 잠시만 기다려주세요**", color=0X36393F)
        msg_show=await ctx.reply(embed=firstembed, mention_author=False)

    try:
        #아이템 레벨
        itemlv = larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)')
        #캐릭터 레벨
        charlv = larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span:nth-child(2)')
        #원정대 레벨
        playerlv = larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)')
        #영지 레벨
        landlv = larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__wisdom > span:nth-child(2)')
        #클래스/이미지
        class_img_name = larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')
        info_class=class_img_name['alt']
        #클래스이미지
        class_img=class_img_name['src']
        #칭호
        charnick=larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__title > span:nth-child(2)')
        #길드
        player_guild=larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__guild > span:nth-child(2)')
        #서버
        player_sever=larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server')
    except:
        pass
    else:
        int_itemlv=int(itemlv.get_text()[3:-3].replace(',',''))
        def gold_calc(itemlv):
            gold=0
            if 1325<=itemlv<1370:
                gold=1300
            elif 1370<=itemlv<1415:
                gold=2900
            elif 1415<=itemlv<1430:
                gold=4100
            elif 1430<=itemlv<1445:
                gold=6600
            elif 1445<=itemlv<1460:
                gold=8600
            elif 1460<=itemlv<1475:
                gold=10600
            elif 1475<=itemlv<1490:
                gold=13500
            elif 1490<=itemlv<1500:
                gold=13500
            elif 1500<=itemlv<1520:
                gold=15000
            elif 1520<=itemlv<1540:
                gold=17500
            elif 1540<=itemlv<1550:
                gold=18500
            elif 1550<=itemlv<1560:
                gold=19000
            elif 1560<=itemlv:
                gold=19500
            return gold    
        gold=gold_calc(int_itemlv)

    #간편검색
    try:
        searchemb = discord.Embed(title=context,description=player_sever.get_text()[1:], color=0X36393F, timestamp=datetime.utcnow())
        searchemb.set_author(name=info_class)
        searchemb.set_thumbnail(url=class_img)
        searchemb.add_field(name="아이템 레벨", value="**`"+itemlv.get_text()+"`**", inline=True)
        searchemb.add_field(name="원정대 레벨", value="**`"+playerlv.get_text()+"`**", inline=True)
        searchemb.add_field(name="길드", value="**`"+player_guild.get_text()+"`**", inline=True)
        searchemb.add_field(name="정보 더보기", value="[전투정보실]("+"https://lostark.game.onstove.com/Profile/Character/"+name+")\t[로아와]("+"https://loawa.com/char/"+name+")\n\n ⏬를 눌러 자세한 정보를 불러옵니다.", inline=False)
        searchemb.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    except:
        searchemb = discord.Embed(title=context,description="플레이어 정보가 존재하지 않습니다.", color=0X36393F, timestamp=datetime.utcnow())
        searchemb.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
        pass
    
    player_flag=1
    try:        
        #캐릭터 특성
        #공격력
        player_atk=larkpcsoup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(2)').get_text()
        #최대 생명력
        player_life=larkpcsoup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > span:nth-child(2)').get_text()
        #치명
        player_crit=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > span:nth-child(2)').get_text()
        #특화
        player_spec=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > span:nth-child(2)').get_text()
        #제압
        player_sup=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)').get_text()
        #신속
        player_speed=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > span:nth-child(2)').get_text()
        #인내
        player_pat=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)').get_text()
        #숙련
        player_mas=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)').get_text()
    except:
        player_flag=0
        pass
    
    #PC 보유캐릭터
    otherchar_list=larkpcsoup.find_all('ul','profile-character-list__char')
    othercount=larkpcsoup.select_one('#expand-character-list > h3 > span > em')
    otherchar_button=[]
    otherchar_onclick=[]
    othercharname_arr=[]
    othercharlink_arr=[]
    othercharname_full=[]
    othercharname_full_2=[]
    MAX=3
    othercountMAX=12
    count_flag=0
    try:
        #다른 캐릭터 정보
        try:
            othercountint=int(othercount.get_text())
        except:
            othercountint=0
        if MAX>othercountint:
            MAX=othercountint
        if othercountMAX>=othercountint:
            othercountMAX=othercountint
        else:
            count_flag=1

        for i in otherchar_list:
            otherchar_button.extend(i.find_all('button'))
            otherchar_onclick.extend(i.find_all('li'))
        for i in otherchar_onclick:
            othercharlink_arr.append(i.find('button')['onclick'][15:-1])
        for i in range(MAX):
            othercharname_arr.append("["+otherchar_button[i].get_text().strip()+"](https://lostark.game.onstove.com"+othercharlink_arr[i]+")")
        othercharname='\n'.join(othercharname_arr)
        for i in range(othercountMAX):
            othercharname_full.append("["+otherchar_button[i].get_text().strip()+"](https://lostark.game.onstove.com"+othercharlink_arr[i]+")")
        if count_flag==1:
            for i in range(12, othercountint):
                othercharname_full_2.append("["+otherchar_button[i].get_text().strip()+"](https://lostark.game.onstove.com"+othercharlink_arr[i]+")")
            othernamefull_2='\n'.join(othercharname_full_2)
        othernamefull='\n'.join(othercharname_full)
    except:
        print("캐릭터 검색 오류")
        pass
    #각인
    try:
        pc_caname_list=larkpcsoup.find('div','profile-ability-engrave').find_all('li')
    except:
        pc_cali=''
        ca_flag=0
        pass
    else:
        pc_ca=[]
        for i in pc_caname_list:
            try:
                pc_ca.append(i.find('span').get_text())
            except:
                pc_ca.append("")
        pc_cali='\n'.join(pc_ca)
        ca_flag=len(pc_caname_list)


    await msg_show.edit(embed=searchemb)
    await msg_show.add_reaction('⏬')
    def check_emoji(reaction, user):
        return reaction.emoji == '⏬' and reaction.message.id == msg_show.id and user.bot == False
    try:
        reaction, user = await bot.wait_for(event='reaction_add', timeout=30.0, check=check_emoji)
    except asyncio.TimeoutError:
        print ("Lark Search: "+context)
        pass
    else:
        await msg_show.delete()
        deepsearch=await ctx.reply(embed=firstembed, mention_author=False)
        #상세검색
        deepsearchembed = discord.Embed(title=context, color=0X36393F, timestamp=datetime.utcnow())
        try:
            deepsearchembed.set_thumbnail(url=class_img)
            deepsearchembed.add_field(name="캐릭터 정보",value="`서버`: "+player_sever.get_text()[1:]+"\n`길드`: "+player_guild.get_text()+"\n`클래스`: "+info_class+"\n`칭호`: "+charnick.get_text(),inline=True)
            deepsearchembed.add_field(name="레벨 정보",value="`캐릭터`: "+charlv.get_text()[:5]+"\n`아이템`: "+itemlv.get_text()+"\n`원정대`: "+playerlv.get_text()+"\n`영지`: "+landlv.get_text(),inline=True)
            if MAX!=0: deepsearchembed.add_field(name="보유 캐릭터("+othercount.get_text()+"개)",value=othercharname,inline=True)
            if player_flag!=0: deepsearchembed.add_field(name="캐릭터 특성",value="`공격력`: "+player_atk+"\n`생명력`: "+player_life+"\n`치명`: "+player_crit+"\n`특화`: "+player_spec+"\n`제압`: "+player_sup+"\n`신속`: "+player_speed+"\n`인내`: "+player_pat+"\n`숙련`: "+player_mas,inline=True)
            if ca_flag!=0: deepsearchembed.add_field(name="각인",value=pc_cali,inline=True)
            deepsearchembed.add_field(name="정보 더보기", value="[전투정보실]("+"https://lostark.game.onstove.com/Profile/Character/"+name+")\t[로아와]("+"https://loawa.com/char/"+name+")\n주간 **"+str(gold)+"**<:gold:931172260457361458> 획득가능\n\n⏬를 눌러 원정대 정보 불러오기", inline=False)
            deepsearchembed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
            await deepsearch.edit(embed=deepsearchembed)
            print ("Lark Deep Search: "+context)
        except:
            searchemb.add_field(name="** **", value="상세 정보를 불러오는데 오류가 발생했습니다.", inline=False)
            await deepsearch.edit(embed=searchemb)
        else:
            await deepsearch.add_reaction('⏬')
            def check_emoji(reaction, user):
                return reaction.emoji == '⏬' and reaction.message.id == deepsearch.id and user.bot == False
            try:
                reaction, user = await bot.wait_for(event='reaction_add', timeout=30.0, check=check_emoji)
            except asyncio.TimeoutError:
                pass
            else:
                ocharmsg= await ctx.reply(embed=firstembed, mention_author=False)
                try:
                    ocharembed = discord.Embed(title="원정대 캐릭터 정보", color=0X36393F, timestamp=datetime.utcnow())
                    ocharembed.add_field(name="보유 캐릭터("+othercount.get_text()+"개)",value=othernamefull,inline=True)
                    if count_flag==1: ocharembed.add_field(name="** **",value=othernamefull_2,inline=True)
                    ocharembed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
                    await ocharmsg.edit(embed=ocharembed)
                    print("Lark OtherCharacter Search: "+context)
                except:
                    await ocharmsg.edit("Error")
@검색.error
async def deepsearch_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Search Error")

@bot.command(aliases=['원정대','주간수익','주간골드','수익계산','주간'])
async def 수익(ctx, context) :
    if ctx.author.bot:
        return None
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **검색중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    try:
        #Heroku용 CHROME
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        #복사하는곳
        name=parse.quote(context)
        abyss=0
        argos=0
        valno=0
        valha=0
        bino=0
        biha=0
        kks=0
        abr=0
        abrha=0
        #MGX 검색
        mgxurl="https://www.mgx.kr/lostark/character/?character_name="+name
        driver.get(mgxurl)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="character_info"]/div[3]/div[4]').click()
        wait= WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#character_info > div.other_characters-category > div > div > div:nth-child(1) > div.character_text > div.character_name')))
        html=driver.page_source
        soup=BeautifulSoup(html,"html.parser")
        charlist=soup.select_one('#character_info > div.other_characters-category > div > div')
        charname=charlist.find_all('div', 'character_name')
        charlv=charlist.find_all('span',{'style': "color:#ff6000"})
        charclass=charlist.find_all('div',{'class':'character_server'})
        embed=discord.Embed(title="원정대 주간 수익",description="상위 6캐릭터의 주간 컨텐츠의 클리어 골드만을 계산한 결과입니다.", color=0X36393F, timestamp=datetime.utcnow())
        totalgold=0
        MAX=6
        if len(charname)<MAX:
            MAX=len(charname)
        for i in range(MAX):
            itemlv=int(float(charlv[i].get_text().strip()))
            if itemlv>=1325:
                gold=0  
                if itemlv<1370:
                    gold=1300
                    abyss+=1
                elif 1370<=itemlv<1415:
                    gold=2900
                    abyss+=1
                    argos+=1
                elif 1415<=itemlv<1430:
                    gold=4100
                    argos+=1
                    valno+=1
                elif 1430<=itemlv<1445:
                    gold=6600
                    argos+=1
                    valno+=1
                    bino+=1
                elif 1445<=itemlv<1460:
                    gold=8600
                    argos+=1
                    valha+=1
                    bino+=1
                elif 1460<=itemlv<1475:
                    gold=10600
                    argos+=1
                    valha+=1
                    biha+=1
                elif 1475<=itemlv<1490:
                    gold=13500
                    valha+=1
                    biha+=1
                    kks+=1
                elif 1490<=itemlv<1500:
                    gold=13500
                    valha+=1
                    kks+=1
                    abr+=1
                elif 1500<=itemlv<1520:
                    gold=15000
                    valha+=1
                    kks+=1
                    abr+=1
                elif 1520<=itemlv<1540:
                    gold=17500
                    valha+=1
                    kks+=1
                    abr+=1
                elif 1540<=itemlv<1550:
                    gold=18500
                    valha+=1
                    kks+=1
                    abrha+=1
                elif 1550<=itemlv<1560:
                    gold=19000
                    valha+=1
                    kks+=1
                    abrha+=1
                elif 1560<=itemlv:
                    gold=19500
                    valha+=1
                    kks+=1
                    abrha+=1
                charclassinfo=charclass[i].get_text().split('-')[0]
                embed.add_field(name=f'{charname[i].get_text()}', value=f'`LV.{itemlv} {charclassinfo}`\n**{gold}**<:gold:931172260457361458>\n*[갱신하기](https://www.mgx.kr/lostark/character/?character_name={parse.quote(charname[i].get_text())})*', inline=True)
                totalgold+=gold
        
        weeklyarr=[]
        if abyss!=0:
            weeklyarr.append(f"어비스 던전: {abyss}캐릭")
        if argos!=0:
            weeklyarr.append(f"아르고스: {argos}캐릭")
        if valno!=0:
            weeklyarr.append(f"발탄(노말): {valno}캐릭")
        if valha!=0:
            weeklyarr.append(f"발탄(하드): {valha}캐릭")
        if bino!=0:
            weeklyarr.append(f"비아키스(노말): {bino}캐릭")
        if biha!=0:
            weeklyarr.append(f"비아키스(하드): {biha}캐릭")
        if kks!=0:
            weeklyarr.append(f"쿠크세이튼(노말): {kks}캐릭")
        if abr!=0:
            weeklyarr.append(f"아브렐슈드(노말): {abr}캐릭")
        if abrha!=0:
            weeklyarr.append(f"아브렐슈드(하드): {abrha}캐릭")
        weekly='\n'.join(weeklyarr)
        
        embed.add_field(name="주간 숙제", value=f'```{weekly}```', inline=False)
        embed.add_field(name="총 획득 가능 골드", value=f'**{totalgold}** <:gold:931172260457361458>\n\아이템레벨에 오류 발생시 캐릭터 정보 갱신이 필요합니다.\n[[갱신하기]]({mgxurl})', inline=False)
        embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
        await msg.edit(embed=embed)
    except:
        embed = discord.Embed(title="검색 실패", color=0X36393F, timestamp=datetime.utcnow())
        embed.add_field(name=f"{context} 님의 원정대 아이템 레벨을 불러올 수 없습니다.", value=f'캐릭터 정보 갱신이 필요합니다.\n[[갱신하기]]({mgxurl})', inline=False)
        embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
        await msg.edit(embed=embed)
@수익.error
async def deepsearch_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Other Char Gold Error")
    
#사사게
@bot.command(aliases=['ㅅㅅㄱ', '인벤'])
async def 사사게(ctx, *contexts):   
    if ctx.author.bot:
        return None
    if len(contexts)==0 or len(contexts)>8:
        raise
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **검색중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    embed = discord.Embed(title="인벤 사건사고게시판 검색결과",description="인벤 사사게 1만개까지 검색한 결과 중 첫번째 게시물입니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_thumbnail(url="https://i.imgur.com/EngjExN.png")
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    print(f"inven searching: {','.join(contexts)}")
    #사사게
    for context in contexts:
        name=parse.quote(context) #입력된 캐릭터 닉네임
        try:
            invenurl = "https://www.inven.co.kr/board/lostark/5355?name=subjcont&keyword="+name
            invenhtml = urlopen(invenurl)
            invensoup = BeautifulSoup(invenhtml, "html.parser")
        except:
            embed.add_field(name=f"{context}", value=f"검색 결과가 없습니다.\n*[검색결과 더보기]({invenurl})*")
        else:
            try:
                invenlink=invensoup.select_one("#new-board > form > div > table > tbody > tr:nth-child(2) > td.tit > div > div > a")
                inven_name=invenlink.get_text()
                inven_link=invenlink["href"]
                embed.add_field(name=f"**{context}**",value=f"**[{inven_name.strip()}]({inven_link})**\n*[검색결과 더보기]({invenurl})*",inline=False)
            except:
                embed.add_field(name=f"{context}", value=f"검색 결과가 없습니다.\n*[검색결과 더보기]({invenurl})*", inline=False)
    await msg.edit(embed=embed, mention_author=False)
@사사게.error
async def inven_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Inven Error")
    
#경매
@bot.command(aliases=['전각'])
async def 경매(ctx, context: int):
    if ctx.author.bot:
        return None
    amount=str(context)
    embed = discord.Embed(title="경매 분배금 계산기",description="**`"+amount+"골드`**", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_thumbnail(url="https://i.imgur.com/tPQYPYM.png")
    embed.add_field(name="4인", value=f"1/N 입찰가: {context*0.95*3/4:.0f}\n1/N 선점입찰가: {context*0.95*3/4*10/11:.0f}\n",inline=False)
    embed.add_field(name="8인", value=f"1/N 입찰가: {context*0.95*7/8:.0f}\n1/N 선점입찰가: {context*0.95*7/8*10/11:.0f}\n",inline=False)
    embed.add_field(name="필드보스", value=f"1/N 입찰가: {context*0.95*29/30:.0f}\n1/N 선점입찰가: {context*0.95*29/30*10/11:.0f}\n",inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.reply(embed=embed, mention_author=True)
@경매.error
async def Auction_err(ctx, error) :
    embed = discord.Embed(title="계산 불가",description="올바른 숫자를 입력해 주십시오.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Auction Error")
    
#골드시세(로아도구)
@bot.command(aliases=['골드시세','크리스탈','크리',"화폐거래소", "시세","크리스탈 시세"])
async def 골드(ctx):
    if ctx.author.bot:
        return None
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
        url=requests.get("https://loatool.taeu.kr/lospi", headers=header).text
        soup=BeautifulSoup(url,"html.parser")
    except:
        raise
    buy=soup.select_one("#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(1) > span")
    sell=soup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(2) > span')
    current_time=datetime.now(pytz.timezone('Japan'))
    embed=discord.Embed(title="크리스탈 시세", description="**100**<:bluecrystal:931176316940726333>당  "+str(current_time)[:-13]+" 기준", color=0X36393F, timestamp=datetime.utcnow())
    embed.add_field(name="구매가",value="**"+buy.get_text().strip()+"** <:gold:931172260457361458>",inline=True)
    embed.add_field(name="판매가",value="**"+sell.get_text().strip()+"** <:gold:931172260457361458>",inline=True)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@골드.error
async def gold_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Gold Error")
    
#오레하 제작(로아도구)
@bot.command(aliases=['중레하','상레하',])
async def 오레하(ctx):
    if ctx.author.bot:
        return None
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
        highurl=requests.get("https://loatool.taeu.kr/calculator/craft/117", headers=header).text
        highsoup=BeautifulSoup(highurl,"html.parser")
        midurl=requests.get("https://loatool.taeu.kr/calculator/craft/131", headers=header).text
        midsoup=BeautifulSoup(midurl,"html.parser")
    except:
        raise
    #시세
    high_price=str(highsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(3) > div.pb-0.pl-md-2.col-md-6.col-12 > div > div.v-card__text.text--primary > div > div:nth-child(4) > span').get_text().strip())
    mid_price=str(midsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(3) > div.pb-0.pl-md-2.col-md-6.col-12 > div > div.v-card__text.text--primary > div > div:nth-child(4) > span').get_text().strip())
    #판매차익
    high_earn=str(highsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(3) > div.pb-0.pl-md-2.col-md-6.col-12 > div > div.v-card__text.text--primary > div > div:nth-child(16) > span').get_text().strip())
    mid_earn=str(midsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(3) > div.pb-0.pl-md-2.col-md-6.col-12 > div > div.v-card__text.text--primary > div > div:nth-child(16) > span').get_text().strip())
    #직접사용
    high_use=highsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(2) > span').get_text().strip()
    mid_use=midsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(2) > span').get_text().strip()
    #판매
    high_val=highsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(3) > span').get_text().strip()
    mid_val=midsoup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div:nth-child(1) > div > div > div.v-card__text.text-center > div:nth-child(2) > div:nth-child(3) > span').get_text().strip()
        
    
    current_time=datetime.now(pytz.timezone('Japan'))
    embed=discord.Embed(title="오레하 융화 재료(고고학) 시세", description=f"{str(current_time)[:-13]} 기준", color=0X36393F, timestamp=datetime.utcnow())
    embed.add_field(name="상급오레하(고고학)",value=f"`시세`: **{high_price}** <:gold:931172260457361458>\n`판매차익(20개당)`: **{high_earn}** <:gold:931172260457361458>\n\n`직접사용`: **{high_use}**\n`판매`: **{high_val}**",inline=True)
    embed.add_field(name="중급오레하(고고학)",value=f"`시세`: **{mid_price}** <:gold:931172260457361458>\n`판매차익(30개당)`: **{mid_earn}** <:gold:931172260457361458>\n\n`직접사용`: **{mid_use}**\n`판매`: **{mid_val}**",inline=True)
    embed.set_footer(text="LarkSearch | 실제 시세와 차이 날 수 있음", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@오레하.error
async def gold_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Oreha Error")
     
#도가토,도비스
@bot.command(aliases=['도가토','도비스','도가토도비스','도전가디언','도전어비스','도디언'])
async def 도전(ctx) :
    if ctx.author.bot:
        return None
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)  
    try:
        larkinven="https://lostark.inven.co.kr/"
        invenhtml = urlopen(larkinven)
        invensoup = BeautifulSoup(invenhtml, "html.parser")
    except:
        raise  
    date=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.head > h2 > strong')
    guardian_1=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(2) > a > p')
    guardian_2=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(3) > a > p')
    guardian_3=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(4) > a > p')
    abyss_1=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(5) > a > p')
    abyss_2=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(6) > a > p')
    embed=discord.Embed(title="이번 주 도전 가디언 & 어비스 던전", color=0X36393F, timestamp=datetime.utcnow())
    embed.add_field(name="도전 가디언",value="`"+guardian_1.get_text()+"` `"+guardian_2.get_text()+"` `"+guardian_3.get_text()+"`",inline=False)
    embed.add_field(name="도전 어비스 던전",value="`"+abyss_1.get_text()+"` `"+abyss_2.get_text()+"`",inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@도전.error
async def gold_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Challange Error")   
    
#전설지도
@bot.command(aliases=['지도', '전지', '카게지도', '지도경매'])
async def 전설지도(ctx) :
    if ctx.author.bot:
        return None
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    url=requests.get("https://loatool.taeu.kr/calculator/secret-map", headers=header).text
    soup=BeautifulSoup(url,"html.parser")
    map_gold=soup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div:nth-child(1) > div > div:nth-child(4) > div:nth-child(2) > span').get_text().strip()
    map_limit=soup.select_one('#app > div > main > div > div > div > div > div.d-flex.flex-row.justify-center > div > div > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div:nth-child(1) > div > div:nth-child(3) > div:nth-child(2) > span').get_text().strip()
    embed=discord.Embed(title="전설지도 시세", description="베른남부 전설지도", color=0X36393F, timestamp=datetime.utcnow())
    embed.add_field(name="입찰적정가",value="**"+map_gold+"** <:gold:931172260457361458>",inline=True)
    embed.add_field(name="손익분기점",value="**"+map_limit+"** <:gold:931172260457361458>",inline=True)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@전설지도.error
async def map_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Map Error")  

#공지사항
@bot.command(aliases=['공지사항','공지','업데이트','패치','업뎃','패치노트'])
async def 로아(ctx) :
    if ctx.author.bot:
        return None
    #공지 (상위 3개+알려진 이슈)
    try:
        larkhtml=urlopen('https://lostark.game.onstove.com/News/Notice/List?noticetype=all')
        larksoup=BeautifulSoup(larkhtml,"html.parser")
    except:
        raise
    loading = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X36393F)
    msg=await ctx.reply(embed=loading, mention_author=False)
    issue=larksoup.select_one('#list > div.list.list--default > ul:nth-child(1) > li:nth-child(1)')
    notice_1=larksoup.select_one('#list > div.list.list--default > ul:nth-child(2) > li:nth-child(1)')
    notice_2=larksoup.select_one('#list > div.list.list--default > ul:nth-child(2) > li:nth-child(2)')
    notice_3=larksoup.select_one('#list > div.list.list--default > ul:nth-child(2) > li:nth-child(3)')
    issue_name=issue.find('span',{'class':'list__title'}).get_text()
    issue_link="https://lostark.game.onstove.com"+issue.find('a')['href']
    notice_1_name=notice_1.find('span',{'class':'list__title'}).get_text()
    notice_1_link="https://lostark.game.onstove.com"+notice_1.find('a')['href']
    notice_2_name=notice_2.find('span',{'class':'list__title'}).get_text()
    notice_2_link="https://lostark.game.onstove.com"+notice_2.find('a')['href']
    notice_3_name=notice_3.find('span',{'class':'list__title'}).get_text()
    notice_3_link="https://lostark.game.onstove.com"+notice_3.find('a')['href']
    imghtml=urlopen('https://lostark.game.onstove.com/Artwork')
    imgsoup=BeautifulSoup(imghtml,"html.parser")
    imgarr=imgsoup.find('div',{"class": "list list--artwork"}).find_all('li')
    imgurlarr=[]
    for i in imgarr:
        imgurlarr.append(i.find('a')['href'])
    randimg=imgurlarr[random.randrange(1,len(imgurlarr))]
    embed=discord.Embed(title="로스트아크 공지사항",description="로스트아크 점검 시, 봇의 기능이 제한됩니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.add_field(name="** **", value=f"[:arrow_forward: {notice_1_name}]({notice_1_link})\n\n[:arrow_forward: {notice_2_name}]({notice_2_link})\n\n[:arrow_forward: {notice_3_name}]({notice_3_link})\n\n[:arrow_forward: {issue_name}]({issue_link})", inline=False)
    embed.set_image(url=randimg)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@로아.error
async def notice_error(ctx, error) :
    embed = discord.Embed(title="정보를 불러올 수 없습니다. 서비스 점검 중 입니다.", color=0X36393F, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Notice Error")
