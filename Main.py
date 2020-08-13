import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime as dt


def cleanDF(df, rollingDays):
    label = f'{rollingDays} Day Average New Cases By State'
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df = df.sort_values('Date', ascending=True)
    df[label] = df['New Cases'].rolling(window=rollingDays).mean()
    return df


def getJSONData(state, requestedData):
    url = "https://covidtracking.com/api/v1/states/" + state.lower() + "/daily.json"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    jsonLocalFilePath = f'{state}.json'
    # jsonFilePath = f'~/Desktop/pyCharm Projects/COVIDTracker/{jsonLocalFilePath}'
    # if os.path.exists(jsonFilePath):
    #     os.remove(jsonFilePath)
    if os.path.exists(jsonLocalFilePath):
        os.remove(jsonLocalFilePath)
    jsonFile = open(jsonLocalFilePath, 'w+')
    json.dump(data, jsonFile)
    jsonFile.close()
    df = pd.read_json(jsonLocalFilePath, orient='records')
    df = df.filter(items=requestedData.keys())
    df.rename(columns=requestedData, inplace=True)
    return df


def saveFigure(states, fig):
    figFileName = '_'.join(states) + '-' + dt.date.today().strftime("%Y-%m-%d") + '.pdf'
    # if os.path.exists(f'~/Desktop/pyCharm Projects/COVIDTracker/{figFileName}'):
    if os.path.exists(figFileName):
        os.remove(figFileName)
    fig.savefig(figFileName, format="pdf")


def main(states, rollingDays):
    fig, ax = plt.subplots()
    yLabel = f'{rollingDays} Day Average New Cases By State'
    for i in range(len(states)):
        newDF = getJSONData(states[i].upper(),
                            requestedData={'date': 'Date', 'state': 'State', 'positiveIncrease': 'New Cases'})
        stateDF = cleanDF(newDF, rollingDays)
        ax = stateDF.plot(ax=ax, kind='line', x='Date', y=yLabel, label=states[i].upper(), x_compat=False)
    plt.xticks(rotation=45)
    plt.title(yLabel)
    plt.ylabel('Avg Number of New Cases')
    plt.grid(linestyle='--', linewidth=1)
    fig.autofmt_xdate()
    saveFigure(states, fig)
    plt.show()


main(['tx'], 3)
# main(['GA', 'TX'], 3)
