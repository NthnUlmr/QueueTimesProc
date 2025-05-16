
import requests
import time
import shutil
import os
import json


def grab_json():
    response = requests.get('https://queue-times.com/parks/59/queue_times.json')
    if response.status_code == 200:
            data = response
           
    else:
        print(f'Error: Unable to fetch data from the API. Status code: {response.status_code}')
        print(f'{response.text}')

    return (data)



def main():
    while(True):
        response = grab_json()

        importantLines = []
        try:
            responseJson = response.json()
            lands = responseJson['lands']
            rides = responseJson['rides']

            
            for ii in range(len(lands)):
                if 'coasters' in lands[ii]['name'].lower():
                    for jj in range(len(lands[ii]['rides'])):
                        curRide = lands[ii]['rides'][jj]
                        importantLines.append(json.dumps(curRide))
                        print(f"{curRide['last_updated']},{curRide['name']},{curRide['is_open']},{curRide['wait_time']}")
            print("")
        except Exception as e:
            print(e)

        responseText =response.text 
        
        

        save_fp = "timeSeriesDatabase.json"
        bkp_fp = "bkup.json"

        if os.path.exists(save_fp):
            shutil.copy(save_fp,bkp_fp)
        else:
            with open(save_fp,'a+') as saveFile:
                pass
            with open(bkp_fp,'a+') as saveFile:
                pass
        try:
            with open(save_fp,'a+') as saveFile:
                #saveFile.writelines(responseText) 
                saveFile.writelines(importantLines)
            
        except Exception as e:
            print(e)
            print('Restoring from backup')
            shutil.copy(bkp_fp,save_fp)
        time.sleep(5.0*60.0)

if __name__ == '__main__':
    main()