import csv
import math
import statistics

from scipy.stats import zscore

dates = []
close_prices = []
open_prices = []
highs = []
lows = []
volumes = []
percentage_changes = []

csv_file_path = './DowJonesHistorialData.csv'

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        
        for row in reader:
            date = row[0].strip('"')
            close_price = float(row[1].replace(',', '').strip('"'))
            open_price = float(row[2].replace(',', '').strip('"'))
            high = float(row[3].replace(',', '').strip('"'))
            low = float(row[4].replace(',', '').strip('"'))
            volume = row[5].strip('"')
            percentage_change = row[6].strip('"')

            dates.append(date)
            close_prices.append(close_price)
            open_prices.append(open_price)
            highs.append(high)
            lows.append(low)
            volumes.append(volume)
            percentage_changes.append(percentage_change)

    # Print the lists
    #print("Dates:", dates)
    #print("Close Prices:", close_prices)
    #print("Open Prices:", open_prices)
    #print("Highs:", highs)
    #print("Lows:", lows)
    #print("Volumes:", volumes)
    #print("Percentage Changes:", percentage_changes)
        
def calculateEachIntervalePriceSumupVolumn(interval):
    min_close_price = math.floor(min(close_prices)/interval)*interval
    max_close_price = math.ceil(max(close_prices)/interval)*interval
    arraySize = math.ceil((max_close_price-min_close_price)/interval)
    sumUPList = [0] * arraySize
    for i in range(0, len(dates), 1):
        tempVolumns = volumes[i].replace("K", "")
        if(tempVolumns != None and tempVolumns != ""):
            tempVolumns = float(volumes[i].replace("K", ""))*1000
            arrayPosition = math.floor(int(close_prices[i] - min_close_price)/interval)
            if(arrayPosition==9):
                print()
            sumUPList[ arrayPosition ] += tempVolumns
    outputFile  = './outputFile(calculateEachIntervalePriceSumupVolumn).csv'
    with open(outputFile, 'w') as file:
        for i in range(len(sumUPList)-1, -1, -1):
            file.write("\"{a}\",\"{b}\"\n".format(a = str(min_close_price+(i*interval)), b = str(sumUPList[i])))
    return sumUPList
            

def calculateZscore(data):
    #caluculate the mean first
    mean = 0;
    for i in range(len(data)-1, -1, -1):
        mean += data[i]
    mean = mean / len(data)
    
    #setup standard_deviation
    standard_deviation = 0.1
    
    outputFile  = './outputFile(calculateZscore).csv'
    with open(outputFile, 'w') as file:
        for i in range(len(data)-1, -1, -1):
            z_scores = statistics.NormalDist(mean, standard_deviation).zscore(data[i])
            file.write("\"{a}\",\"{b}\"\n".format(a = str(data[i]), b = str(z_scores)))
    return z_scores


# Example usage
read_csv_file(csv_file_path)
result1 = calculateEachIntervalePriceSumupVolumn(10);
result2 = calculateZscore(result1);
