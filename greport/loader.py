import pandas as pd
from datetime import datetime as time
import glob


def dataloader():
    list_of_dataframes = []
    list_of_files = glob.glob("./media/reports/*.csv")
    for file in list_of_files:
        frame = pd.read_csv(file, header=0,
                            names=['PatientID', 'TestName', 'ParameterName', 'Result',
                                   'ResultDatetime', 'Normal', 'ReferenceRange'])
        list_of_dataframes.append(frame)
    list_of_files = glob.glob("./media/reports/*.xlsx")
    for file in list_of_files:
        frame = pd.read_excel(file, header=1, converters={'ResultDatetime': pd.to_datetime},
                              names=['PatientID', 'TestName', 'ParameterName', 'Result',
                                     'ResultDatetime', 'Normal', 'ReferenceRange'])
        frame['ResultDatetime'] = frame['ResultDatetime'].dt.strftime('%m-%d-%y %H:%M')
        #list_of_dataframes.append(frame)
    df = pd.concat(list_of_dataframes, axis=0, ignore_index=True)
    # todo duplicate drop
    df.drop_duplicates(inplace=True, keep="first")
    return df


def mod_time_and_sort(dat):
    r = []
    for i in dat:
        t = time.strptime(i[0], "%m-%d-%y %H:%M")
        m = [t] + i[1:]
        j = 0
        le = len(r)
        for j in range(le + 1):
            if j == le:
                break
            if t < r[j][0]:
                break
        if j == 0:
            r = [m] + r
        elif j == le:
            r.append(m)
        else:
            r = r[:j] + [m] + r[j:]
    for i in range(len(r)):
        r[i][0] = r[i][0].strftime("%d-%m-%Y %I:%M %p")
    return r


def get_data_object(pid):
    df = dataloader()
    df = df.loc[df['PatientID'] == pid]
    df = df[df['ParameterName'] != 'Comment']
    df = df[df['Result'] != 'Subhead']
    df = df[df['Result'] != 'SubHead']
    df['Result'] = df['Result'].astype(str)
    df['ResultDatetime'] = df['ResultDatetime'].astype(str)
    df['ReferenceRange'] = df['ReferenceRange'].astype(str)
    df['ParameterName'] = df[['ParameterName', 'Normal', 'Result',
                              'ReferenceRange']].agg('$'.join, axis=1)
    result = list()
    df['TestName'] = df['TestName']+df['ResultDatetime']
    for test_name in df['TestName'].unique():
        testlist = list()
        param_df = df[df['TestName'] == test_name]
        date_time = param_df['ResultDatetime'].iloc[0]
        if date_time[-5] == " ":
            date_time = date_time[:-4] + '0' + date_time[-4:]
            testlist.append(date_time)
            testlist.append(test_name[:-13])
        else:
            testlist.append(date_time)
            testlist.append(test_name[:-14])
        parameter_list = list()
        for parameter in param_df['ParameterName'].unique():
            parameter_list.append(parameter.split('$'))
        testlist.append(parameter_list)
        result.append(testlist)
    result = mod_time_and_sort(result)
    return result
