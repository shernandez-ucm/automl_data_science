import pandas as pd
import os
import glob
from unidecode import unidecode

# Function to remove accents using unidecode
def remove_accents(text):
    if isinstance(text, str):
        return unidecode(text)
    else:
        return text
    

def process_dataset(data_dir,target_technologies):
    # Get a list of all CSV files in the directory
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

    # List to hold the filtered DataFrames
    filtered_dfs = []

    print(f"Found {len(csv_files)} CSV files to process.")

    for file_path in csv_files:
        try:
            # Read the CSV file using the semicolon separator
            df = pd.read_csv(file_path, sep=';',low_memory=False)
            df["Generacion_MWh"]=df["Generacion_MWh"].str.replace(',','.').astype("float")
            df["Codigo Central"]=df["Codigo Central"].astype("category")
            df["Tecnologia"]=df["Tecnologia"].astype("category")
            df["Clasificacion"]=df["Clasificacion"].astype("category")
            df["Tecnologia"]=df["Tecnologia"].cat.rename_categories(lambda x: x.upper().replace(' ','_'))
            df['Tecnologia']=df['Tecnologia'].apply(remove_accents)
            # Filter the DataFrame
            df_filtered = df[df['Tecnologia'].isin(target_technologies)].copy()

            # Append the filtered DataFrame to the list
            filtered_dfs.append(df_filtered)
            print(f"Processed {os.path.basename(file_path)}. Filtered rows: {len(df_filtered)}")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # Concatenate all filtered DataFrames into a single DataFrame
    #filtered_dfs["Tecnologia"] = filtered_dfs["Tecnologia"].cat.remove_unused_categories()
    final_df = pd.concat(filtered_dfs, ignore_index=True)
    print("\n--- Final Result ---")
    print(f"Successfully merged all filtered data.")
    print(f"Final DataFrame shape: {final_df.shape}")
    print(f"Unique Technologies in final DataFrame: {final_df['Tecnologia'].unique()}")
    return final_df
