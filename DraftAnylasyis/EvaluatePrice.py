import csv
from scipy import stats

# You can configure you league settings here
TEAM_NUM = 20               # there are 18 team in total in a league
TEAM_PLAYER = 11            # each team has 12 players
TEAM_CAP = 200              # each team has $200 cap
ONE_DOLLAR_PLAYER_NUM = 20   # suppose the last 20 players values $1 


def ReadRawValues(file_name):
    print('Reading Data from', file_name, '...')

    names = []  # name list
    values = []  # value list

    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row['Name'])
            values.append(float(row['Value']))
    
    # print(names)
    # print(values)

    return names, values

    # print(players['Value'])

    # d = {}  # name to raw value map
    # d1 = {}  # name to id multiple map, 
    # wb = openpyxl.load_workbook(file_name, data_only=True) # data_only flag will return the value not the formula
    # for ws in wb.worksheets:
    #     for x in range(2, ws.max_row + 1):  # start from 2 to skip the title
    #         name = ws.cell(row=x, column=1).value
    #         id = ws.cell(row=x, column=2).value

    #         if (id in d):
    #             print ('ALERT: duplicate id:', id)
    #         else:
    #             d[id] = name

    #         # name to id map 
    #         d1.setdefault(name,[]).append(id)

    # # for k, v in d.items():
    # #     print(k, v)
    # print ('Total id count:', len(d))
    # print ('Total name count:', len(d1))

    # return d, d1




def EvaluatePrices(rawValues):
    zScores = stats.zscore(rawValues)

    totalPlayer = int(TEAM_NUM) * int(TEAM_PLAYER)
    totalCap = int(TEAM_NUM) * int(TEAM_CAP)
    print('total player', totalPlayer)

    # the last 'ONE_DOLLAR_PLAYER_NUM' players are all price 1
    budget = totalCap - ONE_DOLLAR_PLAYER_NUM * 1
    playerCnt = totalPlayer - ONE_DOLLAR_PLAYER_NUM
    avePrice = budget / playerCnt

    midValueIdx = playerCnt // 2
    lowValueIdx = playerCnt

    # convert the z value to price
    # the formula is Price = a + b* zScore
    # and two  equation:
    #  avePrice = a + b* zScores[midValueIdx]
    #  1        = a + b* zScores[lowValueIdx]
    #  thus we can calculate a and b.
    b = (avePrice - 1) / (zScores[midValueIdx] - zScores[lowValueIdx])
    a = avePrice - b * zScores[midValueIdx]

    prices = []

    for score in zScores:
        price = a + b * score
        prices.append(int(round(price)))

    return prices

def main():
    print('main')
    names, values = ReadRawValues('player_value_2016.csv')
    prices = EvaluatePrices(values)

    totalPlayer = int(TEAM_NUM) * int(TEAM_PLAYER)

    print('write to file price.csv')
    with open('price.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Value', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, (name, value, price) in enumerate(zip(names, values, prices)):
            if i >= totalPlayer - 1:
                price = 0
            elif i >= totalPlayer - ONE_DOLLAR_PLAYER_NUM :
                price = 1

            writer.writerow({'Name': name, 'Value': value, 'Price' : price})

if __name__ == '__main__':
    main()
