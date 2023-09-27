import pprint
import numpy as np
import getAPI
import getTempDataset
import getDataset
pp = pprint.PrettyPrinter(indent=4)



# pp.pprint(getGameInfo('KR_6708057039')['info']['teams'][0]['objectives'])


if __name__ == "__main__":
    pp.pprint(getTempDataset.tempResult('KR_6708057039', 10))
    pp.pprint(getDataset.getDataSet('KR_6708057039', 10))
# pp.pprint(getGameInfo('KR_6708057039')['info']['participants'][0])
# pp.pprint(getGameInfoTimeline('KR_6709531155').keys())
# pp.pprint(getGameInfoTimeline('KR_6708057039')['info']['frames'][10]['events'])