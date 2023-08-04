import pandas as pd
import os

csv_file = 'results_cv.csv'

def save_datas(results_list)->None:
    """
    Save the results of the detection in a csv file. If the file doesn't exist, it is created. If it exists, the results are added to the file.

    Args:
        results_list (list): list of the results of the detection
    """
    if not os.path.exists(csv_file):
        df_name = pd.DataFrame({'Sample nb': ['First detection', 'Second detection', 'Ground truth']})
        df = pd.DataFrame({'0': results_list})
        df = pd.concat([df_name, df], axis=1)
        df.to_csv(csv_file, index=False)
    else:
        df = pd.read_csv(csv_file)
        
        if len(results_list) == df.shape[0]:
            id = df.shape[1]
            df[str(id)] = results_list
            df.to_csv(csv_file, index=False)
        else:
            print("Error: results_list and results.csv have different lengths")
            
if __name__ == "__main__":
    results_list = [12, 0.85]  
    save_datas(results_list)
    

