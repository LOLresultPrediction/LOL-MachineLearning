import pprint
import numpy as np
import getAPI
import getRealDataset
import getDataset
import getMatchId
pp = pprint.PrettyPrinter(indent=4)



# pp.pprint(getGameInfo('KR_6708057039')['info']['teams'][0]['objectives'])

'''
'KR_6710383118', 1. 브라이어(5/14/5)
'KR_6709906475', 2. 브라이어(7/9/1)
'KR_6709583655', 3. 브라이어(0/0/0)
'KR_6709531155', 4. 나피리(8/9/2)
'KR_6709504031', 5. 라이즈
'KR_6708057039', 6. 브라이어(0/9/0)
'KR_6708035868',
'KR_6707425375',
'KR_6707289771',
'KR_6704954051']
'''
if __name__ == "__main__":
    # 챌린저 매치 ID 가져오기
    print(len(getMatchId.getChallengerMatchId()))

    pp.pprint(getRealDataset.tempResult('KR_6704954051', 16))
    # gameTimelineInfo = getAPI.getGameInfoTimeline('KR_6708057039')
    # gameInfo = getAPI.getGameInfo('KR_6709906475')
    # for i in range(10):
    #     pp.pprint(gameInfo['info']['participants'][i]['participantId'])
    #     pp.pprint(gameInfo['info']['participants'][i]['summonerName'])
    #     pp.pprint(gameInfo['info']['participants'][i]['championName'])
    # pp.pprint(gameInfo['info']['teams'][1]['objectives'])

    # pp.pprint(getDataset.getDataSet('KR_6708057039', 15))
    # pp.pprint(getAPI.getGameInfo('KR_6708057039')['info']['teams'])