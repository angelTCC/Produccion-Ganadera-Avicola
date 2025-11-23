import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")



excel_path = ["./data/anuario_pecuaria_2024.xlsx",
              "./data/2730346-cuadros-en-excel-del-anuario-produccion-ganadera-y-avicola-2023.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2022.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2021.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2020.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2019.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2018.xls",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2017.xlsx",
              "./data/Cuadros en Excel del anuario _PRODUCCIÓN GANADERA Y AVÍCOLA_ 2016.xlsx",
              ]
years = ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"]
sheet_name = "C-4"
name_cuadro = "POBLACIÓN PECUARIA POR ESPECIE, SEGÚN REGIÓN"
regiones = ["Región", "Tumbes", "Piura", 
            "Lambayeque", "La Libertad", 
            "Cajamarca", "Amazonas", "Ancash", 
            "Lima","Ica", "Huánuco",
            "Pasco", "Junín", "Huancavelica",
            "Arequipa", "Moquegua", "Tacna",
            "Ayacucho", "Apurímac", "Cusco",
            "Puno", "San Martín", "Loreto",
            "Ucayali","Madre de Dios"]

'''
Load data
'''

data = {}

print("Loading data ...")
for path, year  in zip(excel_path, years):
    try :
        df = pd.read_excel(path, sheet_name)
        
        # select data
        starts = df.index[df.apply(lambda r: r.astype(str).str.contains("|".join(map(str, regiones))).any(), axis=1)]
        df = df.iloc[starts,:].reset_index(drop=True) # Selecting the frame

        # columns treatment
        df.dropna(axis=1, inplace=True, how="all")
        df.columns = df.iloc[0,:]
        df.columns = df.columns.astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
        df.columns = df.columns.astype(str).str.lower()


        data[year] = df

    except ValueError as e:
        print(f"❌ Error loading in excel {path}, {sheet_name}")


print(f"✅ Data loaded, only {len(data)} was loaded")

'''
Join data
'''

ref_year = "2024"
ref_cols = set(data[ref_year].columns)

print("verifying columns names ...")

for year, df in data.items():
    
    if year == ref_year:
        continue

    cols = set(df.columns)
    diff = ref_cols.symmetric_difference(cols)

    if len(diff)>0:
        print(f"\n📝 Differences vs {ref_year} for {year}:")
        print(diff)
        data.pop(year)
        print(f"Data frame from {year} was removed")
    
print("✅ Columns names are the same.")

print("Joining data frames ...")
