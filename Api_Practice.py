import requests

api_key = "RGAPI-01661c2d-9539-4a00-93ea-ff882aad8fb0"
header = {"X-Riot-Token" : api_key}

def match(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    
    return requests.get(url, headers=header)

req = match('KR_6709531155')

if req.status_code == 200:
    data = req.json()

    queue_id = data['info']['queueId'] # 큐 id
    game_duration = data['info']['gameDuration'] # 게임 진행 시간
    game_start_timestamp = data['info']['gameStartTimestamp'] # 게임 시작 시간
    game_end_timestamp = data['info']['gameEndTimestamp'] # 게임 종료 시간


# 매치 데이터(포지션/챔피언/킬/데스/어시/CS 등)
    participants = data['info']['participants']

    for participant in participants:
        team_id = participant['teamId'] # 팀 id
        summoner_id = participant['summonerId'] 
        summoner_name = participant['summonerName'] 
        summoner_1_id = participant['summoner1Id'] 
        summoner_2_id = participant['summoner2Id'] 
        team_position = participant['teamPosition']
        champion_id = participant['championId']
        kills = participant['kills'] 
        deaths = participant['deaths'] 
        assists = participant['assists'] 
        kda = participant['challenges']['kda']
        neutral_minions_killed = participant['neutralMinionsKilled'] 
        total_minions_killed = participant['totalMinionsKilled'] 

        if team_position == 'UTILITY':
            team_position = 'SUPPORT'


# 팀 데이터
    teams = data['info']['teams']

    for team in teams:
        team_id = team['teamId'] 
        first_blood = team['objectives']['champion']['first'] 
        first_tower = team['objectives']['tower']['first'] 
        first_inhibitor = team['objectives']['inhibitor']['first'] 
        first_baron = team['objectives']['baron']['first']
        first_dragon = team['objectives']['dragon']['first'] 
        first_rift_herald = team['objectives']['riftHerald']['first'] 
        win = team['win'] # 승패
        bans = team['bans'] 
        bans_lst = []
        for ban in bans:
            if ban['championId'] != -1:
                bans_lst.append(ban['championId'])