from ast import alias
import asyncio
from email import message
from logging import info
from typing import ContextManager
import discord
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib import parse
from discord.ext import commands
import random
from datetime import datetime

bot = commands.Bot(command_prefix = '!', help_command = None)

# 아래는 봇이 구동되었을 때 동작하는 부분
@bot.event
async def on_ready():
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='!명령어'))

#검색      
@bot.command(aliases=['정보'])
async def 검색(ctx, context) :
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **검색중입니다. 잠시만 기다려주세요**",description="전투정보실에서 캐릭터 정보를 가져오는 중입니다.", color=0X4441A6)
    msg_show=await ctx.reply(embed=firstembed, mention_author=False)
    name=parse.quote(f'{context}') #입력된 캐릭터 닉네임
    #전투정보실 모바일 검색
    larkurl = "https://m-lostark.game.onstove.com/Profile/Character/"+name
    print ("LARK Deep Searching: "+context)
    larkhtml = urlopen(larkurl)
    larksoup = BeautifulSoup(larkhtml, "html.parser")
    
    #전투정보실 PC 검색
    larkpcurl="https://lostark.game.onstove.com/Profile/Character/"+name
    larkpchtml=urlopen(larkpcurl)
    larkpcsoup=BeautifulSoup(larkpchtml,"html.parser")
    
    #MGX 검색
    mgxurl="https://www.mgx.kr/lostark/character/?character_name="+name
    mgxhtml=urlopen(mgxurl)
    mgxsoup=BeautifulSoup(mgxhtml, "html.parser")
    
    #아이템 레벨
    itemlv = larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__contents-level > div:nth-child(2) > dl.define.item > dd")
    #캐릭터 레벨
    charlv = larksoup.select_one('#myinfo__character--button2')
    #원정대 레벨
    playerlv=larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__contents-level > div:nth-child(1) > dl:nth-child(1) > dd")
    #영지 레벨
    landlv=larkpcsoup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__wisdom > span:nth-child(2)')
    #클래스
    info_class = larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__user > dl.myinfo__user-names > dd > div.wrapper-define > dl:nth-child(2) > dd")
    #칭호
    charnick=larksoup.select_one('#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__contents-level > div:nth-child(1) > dl:nth-child(2) > dd')
    #클래스이미지
    class_img=larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__user > dl.myinfo__badge > dd > img")
    #길드
    player_guild=larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__contents-level > div:nth-child(3) > dl:nth-child(1) > dd")
    #서버
    player_sever=larksoup.select_one("#lostark-wrapper > div > main > div > div > div.myinfo__contents-character > div.myinfo__user > dl.myinfo__user-names > dd > div.wrapper-define > dl:nth-child(1) > dd")
    
    #캐릭터 특성
    #공격력
    player_atk=larkpcsoup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(2)')
    #최대 생명력
    player_life=larkpcsoup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > span:nth-child(2)')
    #치명
    player_crit=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > span:nth-child(2)')
    #특화
    player_spec=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > span:nth-child(2)')
    #제압
    player_sup=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)')
    #신속
    player_speed=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > span:nth-child(2)')
    #인내
    player_pat=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)')
    #숙련
    player_mas=larkpcsoup.select_one('#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)')
    
    #PC 보유캐릭터
    otherchar_list=larkpcsoup.find_all('ul','profile-character-list__char')
    othercount=larkpcsoup.select_one('#expand-character-list > h3 > span > em')
    otherchar_button=[]
    otherchar_onclick=[]
    othercharname_arr=[]
    othercharlink_arr=[]
    MAX=3
    #다른 캐릭터 정보
    try:
        if MAX>int(othercount.get_text()):
            MAX=int(othercount.get_text())
    except:
        MAX=0
    
    for i in otherchar_list:
        otherchar_button.extend(i.find_all('button'))
        otherchar_onclick.extend(i.find_all('li'))
    for i in otherchar_onclick:
        othercharlink_arr.append(i.find('button')['onclick'][15:-1])
    for i in range(MAX):
        othercharname_arr.append("["+otherchar_button[i].get_text().strip()+"](https://lostark.game.onstove.com"+othercharlink_arr[i]+")")
    othercharname='\n'.join(othercharname_arr)
    
    #MGX 각인
    caname_list=mgxsoup.find_all('div', {'class': "carving_category"})
    calv_list=mgxsoup.find_all('div', {'class': "carving_level"})
    ca_list=[]
    for i in range(len(caname_list)) :
        try:
            ca_list.append(caname_list[i].get_text()+" "+calv_list[i].get_text())
        except:
            ca_list.append("")
    ca_li='\n'.join(ca_list)
    
    #간편검색
    try:
        searchemb = discord.Embed(title=context,description=player_sever.get_text()[1:], color=0X4441A6, timestamp=datetime.utcnow())
        searchemb.set_author(name=info_class.get_text())
        searchemb.set_thumbnail(url=class_img.get("src"))
        searchemb.add_field(name="아이템 레벨", value="**`"+itemlv.get_text()+"`**", inline=True)
        searchemb.add_field(name="원정대 레벨", value="**`"+playerlv.get_text()+"`**", inline=True)
        searchemb.add_field(name="길드", value="**`"+player_guild.get_text()+"`**", inline=True)
        searchemb.add_field(name="정보 더보기", value="[전투정보실]("+"https://lostark.game.onstove.com/Profile/Character/"+name+")\t[로아와]("+"https://loawa.com/char/"+name+")\n\n **`더보기`**를 입력해 자세한 정보를 불러올 수 있습니다.", inline=False)
        searchemb.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    except:
        searchemb = discord.Embed(title=context,description="플레이어 정보가 존재하지 않습니다.", color=0X4441A6, timestamp=datetime.utcnow())
        searchemb.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")


    if ctx.author.bot:
        return None
    def check(msg) :
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["상세", "상세검색", "각인", "상세보기","더보기"]
    try:
        await msg_show.edit(embed=searchemb)
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await msg_show.edit(embed=searchemb)
    else:
        await msg_show.delete()
        deepsearch=await ctx.reply(embed=firstembed, mention_author=False)
        #상세검색
        try:
            deepsearchembed = discord.Embed(title=context, color=0X4441A6, timestamp=datetime.utcnow())
            deepsearchembed.set_thumbnail(url=class_img.get("src"))
            deepsearchembed.add_field(name="캐릭터 정보",value="`서버`: "+player_sever.get_text()[1:]+"\n`클래스`: "+info_class.get_text()+"\n`길드`: "+player_guild.get_text()+"\n`칭호`: "+charnick.get_text(),inline=True)
            deepsearchembed.add_field(name="레벨 정보",value="`캐릭터`: "+charlv.get_text()[:5]+"\n`아이템`: "+itemlv.get_text()+"\n`원정대`: "+playerlv.get_text()+"\n`영지`: "+landlv.get_text(),inline=True)
            if MAX!=0: deepsearchembed.add_field(name="보유 캐릭터("+othercount.get_text()+"개)",value=othercharname,inline=True)
            deepsearchembed.add_field(name="캐릭터 특성",value="`공격력`: "+player_atk.get_text()+"\n`생명력`: "+player_life.get_text()+"\n`치명`: "+player_crit.get_text()+"\n`특화`: "+player_spec.get_text()+"\n`제압`: "+player_sup.get_text()+"\n`신속`: "+player_speed.get_text()+"\n`인내`: "+player_pat.get_text()+"\n`숙련`: "+player_mas.get_text(),inline=True)
            if ca_li!='': deepsearchembed.add_field(name="각인",value=ca_li,inline=True)
            deepsearchembed.add_field(name="정보 더보기", value="[전투정보실]("+"https://lostark.game.onstove.com/Profile/Character/"+name+")\t[로아와]("+"https://loawa.com/char/"+name+")", inline=False)
            deepsearchembed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
            await deepsearch.edit(embed=deepsearchembed)
        except:
            deepsearchembed = discord.Embed(title=context,description="상세검색이 불가능한 플레이어입니다.", color=0X4441A6, timestamp=datetime.utcnow())
            deepsearchembed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
            await deepsearch.edit(embed=deepsearchembed)
@검색.error
async def deepsearch_error(ctx, error) :
    embed = discord.Embed(title="검색오류",description="없는 닉네임이거나 서비스 점검중입니다. <:08:876347062122344448>", color=0XF2F0F2, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Search Error")

#사사게  
@bot.command(aliases=['ㅅㅅㄱ', '인벤'])
async def 사사게(ctx, context):
    name=parse.quote(context) #입력된 캐릭터 닉네임
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **검색중입니다. 잠시만 기다려주세요**", color=0X2D3073)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    #사사게
    invenurl = "https://www.inven.co.kr/board/lostark/5355?name=subjcont&keyword="+name
    invenhtml = urlopen(invenurl)
    print("Inven Searching: "+context)
    invensoup = BeautifulSoup(invenhtml, "html.parser")
    invenlink=invensoup.select_one("#new-board > form > div > table > tbody > tr:nth-child(2) > td.tit > div > div > a")
    invenlink_sever=invensoup.select_one("#new-board > form > div > table > tbody > tr:nth-child(2) > td.tit > div > div > a > span")
    
    if ctx.author.bot:
        return None
    
    try:
        embed = discord.Embed(title=context, description="인벤 사사게 1만개까지 검색한 결과 중 첫번째 게시물입니다.", color=0X2D3073, timestamp=datetime.utcnow())
        embed.set_author(name="인벤 사건사고게시판 검색결과")
        embed.set_thumbnail(url="https://i.imgur.com/EngjExN.png")
        embed.add_field(name="** **",value="**["+invenlink.text.strip()+"]("+invenlink["href"]+")**\n\n*[검색결과 더보기]("+invenurl+")*",inline=False)
        embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
        await msg.edit(embed=embed, mention_author=False)
    except:
        embed = discord.Embed(title="인벤 사건사고게시판 검색결과",description="인벤 사사게 1만개까지 검색한 결과 중 첫번째 게시물입니다.", color=0XF2F0F2, timestamp=datetime.utcnow())
        embed.set_thumbnail(url="https://i.imgur.com/EngjExN.png")
        embed.add_field(name=context, value="검색 결과가 없습니다.")
        embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
        await msg.edit(embed=embed, mention_author=False)
@사사게.error
async def inven_error(ctx, error) :
    embed = discord.Embed(title="검색오류",description="올바른 닉네임을 입력해 주십시오.", color=0XF2F0F2, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Inven Error")
    
#경매
@bot.command(aliases=['전각'])
async def 경매(ctx, context: int):
    amount=str(context)
    print ("Auction "+amount)
    embed = discord.Embed(title="경매 분배금 계산기",description="**`"+amount+"골드`**", color=0X62DBCB, timestamp=datetime.utcnow())
    embed.set_thumbnail(url="https://i.imgur.com/tPQYPYM.png")
    embed.add_field(name="4인", value=f"1/N 입찰가: {context*0.95*3/4:.0f}\n1/N 선점입찰가: {context*0.95*3/4*10/11:.0f}\n",inline=False)
    embed.add_field(name="8인", value=f"1/N 입찰가: {context*0.95*7/8:.0f}\n1/N 선점입찰가: {context*0.95*7/8*10/11:.0f}\n",inline=False)
    embed.add_field(name="필드보스", value=f"1/N 입찰가: {context*0.95*29/30:.0f}\n1/N 선점입찰가: {context*0.95*29/30*10/11:.0f}\n",inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.reply(embed=embed, mention_author=True)
@경매.error
async def Auction_err(ctx, error) :
    embed = discord.Embed(title="오류가 발생했습니다.",description="올바른 숫자를 입력해 주십시오. <:08:876347062122344448>", color=0XF2F0F2, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Auction Error")
    
#골드시세(MGX)
@bot.command(aliases=['골드시세','크리스탈','크리',"화폐거래소", "시세","크리스탈 시세"])
async def 골드(ctx):
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X05E0CF)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    if ctx.author.bot:
        return None
    larkhtml = urlopen("https://mgx.kr/lostark/goldexchange/")
    loatoolsoup = BeautifulSoup(larkhtml, "html.parser")
    buy=loatoolsoup.select_one("#content > div > div.inner_content > div.chart_change > div.live_price > div.price_box.buy_box > div.price.buy > span")
    sell=loatoolsoup.select_one('#content > div > div.inner_content > div.chart_change > div.live_price > div.price_box.sell_box > div.price.sell > span')
    date=loatoolsoup.select_one('#content > div > div.inner_content > div.chart_change > div.searched_time')
    embed=discord.Embed(title="크리스탈 시세", description="**100**<:bluecrystal:931176316940726333>당  "+date.get_text()[:19]+" 기준", color=0X05E0CF, timestamp=datetime.utcnow())
    embed.add_field(name="구매가",value="**"+buy.get_text()+"** <:gold:931172260457361458>",inline=True)
    embed.add_field(name="판매가",value="**"+sell.get_text()+"** <:gold:931172260457361458>",inline=True)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@골드.error
async def gold_error(ctx, error) :
    embed = discord.Embed(title="오류가 발생했습니다.",description="정보를 불러올수 없습니다.", color=0XF2F0F2, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Gold Error")   
     
#도가토,도비스
@bot.command(aliases=['도가토','도비스','도가토도비스','도전가디언','도전어비스'])
async def 도전(ctx) :
    firstembed = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X05E0CF)
    msg=await ctx.reply(embed=firstembed, mention_author=False)
    if ctx.author.bot:
        return None
    larkinven="https://lostark.inven.co.kr/"
    invenhtml = urlopen(larkinven)
    invensoup = BeautifulSoup(invenhtml, "html.parser")
    date=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.head > h2 > strong')
    guardian_1=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(2) > a > p')
    guardian_2=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(3) > a > p')
    guardian_3=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(4) > a > p')
    abyss_1=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(5) > a > p')
    abyss_2=invensoup.select_one('#imid_820b68367ec0fa0 > div > div.content > ul > li:nth-child(6) > a > p')
    embed=discord.Embed(title="이번 주 도전 가디언 & 어비스 던전", color=0X05E0CF, timestamp=datetime.utcnow())
    embed.add_field(name="도전 가디언",value="`"+guardian_1.get_text()+"` `"+guardian_2.get_text()+"` `"+guardian_3.get_text()+"`",inline=False)
    embed.add_field(name="도전 어비스 던전",value="`"+abyss_1.get_text()+"` `"+abyss_2.get_text()+"`",inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@도전.error
async def gold_error(ctx, error) :
    embed = discord.Embed(title="오류가 발생했습니다.",description="정보를 불러올수 없습니다.", color=0XF2F0F2, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Challange Error")   
           
#공지사항
@bot.command(aliases=['공지사항','공지','업데이트','패치','업뎃','패치노트'])
async def 로아(ctx) :
    if ctx.author.bot:
        return None
    loading = discord.Embed(title="<a:Rolling:931525359122403338> **정보를 불러오는 중입니다. 잠시만 기다려주세요**", color=0X05E0CF)
    msg=await ctx.reply(embed=loading, mention_author=False)
    #공지 (상위 3개+알려진 이슈)
    larkhtml=urlopen('https://lostark.game.onstove.com/News/Notice/List?noticetype=all')
    larksoup=BeautifulSoup(larkhtml,"html.parser")
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
    embed=discord.Embed(title="로스트아크 공지사항",description="로스트아크 점검 시, 봇의 기능이 제한됩니다.", color=0X05E0CF, timestamp=datetime.utcnow())
    embed.add_field(name="** **", value=f"[:arrow_forward: {notice_1_name}]({notice_1_link})\n\n[:arrow_forward: {notice_2_name}]({notice_2_link})\n\n[:arrow_forward: {notice_3_name}]({notice_3_link})\n\n[:arrow_forward: {issue_name}]({issue_link})", inline=False)
    embed.set_image(url=randimg)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await msg.edit(embed=embed)
@로아.error
async def notice_error(ctx, error) :
    embed = discord.Embed(title="검색오류",description="서비스 점검중입니다.", color=0X05E0CF, timestamp=datetime.utcnow())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    print("Notice Error")
    
    
#기타 명령어(비활성화됨)

#업데이트/봇 정보    
@bot.command(aliases=['LarkSearch','봇소개','개발자','개발'])
async def 로아봇(ctx):
    if ctx.author.bot:
        return None
    embed = discord.Embed(title="LarkSearch 정보", color=0XF2C094, timestamp=datetime.utcnow())
    embed.add_field(name="**봇 업데이트 내역**",value="22.01.15```로스트아크 공지사항 불러오기를 추가하였습니다.```",inline=False)
    embed.add_field(name="개발자",value="디스머스 @카제로스 <:35:909731098735575072>\n건의사항, 버그문의: larksearchhelp@gmail.com | ㅎㅅ#8977\n[*donate*](https://toss.me/larksearch)", inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)
    
#help
@bot.command(aliases=['도움말', 'help'])
async def 명령어(ctx):
    embed = discord.Embed(title="LarkSearch 도움말", color=0XF2C094, timestamp=datetime.utcnow())
    embed.add_field(name="**!검색/정보 [닉네임]**",value="전투정보실에서 플레이어의 정보를 불러옵니다.\n정보가 나온 후 **`더보기`**를 입력해 자세한 정보를 불러올 수 있습니다.",inline=False)
    embed.add_field(name="gi**!사사게/ㅅㅅㄱ [닉네임]**",value="로스트아크 인벤 사건사고게시판에서 검색한 결과를 불러옵니다.",inline=False)
    embed.add_field(name="**!경매/전각 [금액]**",value="경매시 1/N을 할수있는 입찰가 입니다.",inline=False)
    embed.add_field(name="**!골드**",value="현재 화폐 거래소의 시세를 불러옵니다.",inline=False)
    embed.add_field(name="**!도비스/도디언**",value="이번주 도전 가디언 토벌&어비스 던전 정보를 불러옵니다.",inline=False)
    embed.add_field(name="**!공지사항**",value="로스트아크 홈페이지의 공지사항을 불러옵니다.")
    embed.add_field(name="**!명령어/도움말**",value="도움말을 출력합니다.",inline=False)
    embed.add_field(name="**!로아봇**",value="LarkSearch의 업데이트 내역과 정보를 출력합니다.",inline=False)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await ctx.send(embed=embed)

bot.run('')
