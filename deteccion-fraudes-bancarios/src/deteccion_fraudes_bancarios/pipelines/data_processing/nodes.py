import pandas as pd

def minusculizar_columnas(data) -> pd.DataFrame:
    """
    Convierte los nombres de las columnas a minúsculas.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos.
        
    Returns:
        pd.DataFrame: DataFrame con los nombres de columnas en minúsculas.
    """
    data.columns = data.columns.str.lower()
    print("Nombres de columnas convertidos a minúsculas.")
    return data

def eliminar_duplicados(data) -> pd.DataFrame:
    """
    Elimina filas duplicadas del DataFrame.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos.
        
    Returns:
        pd.DataFrame: DataFrame sin filas duplicadas.
    """
    antes = len(data)
    data = data.drop_duplicates()
    despues = len(data)
    print(f"Duplicados eliminados: {antes - despues}. Filas restantes: {despues}.")
    return data

def eliminar_nulos(data) -> pd.DataFrame:
    """
    Elimina filas con valores nulos del DataFrame.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos.
        
    Returns:
        pd.DataFrame: DataFrame sin filas con valores nulos.
    """
    antes = len(data)
    data = data.dropna()
    despues = len(data)
    print(f"Filas con valores nulos eliminadas: {antes - despues}. Filas restantes: {despues}.")
    return data

def is_number(columna) -> bool:
    """
    Verifica si una columna contiene valores numéricos.
    
    Args:
        columna (pd.Series): Columna del DataFrame.
        
    Returns:
        bool: True si la columna es numérica, False en caso contrario.
    """
    return pd.to_numeric(columna, errors='coerce').notnull().all()

def convertir_a_numerico(data) -> pd.DataFrame:
    """
    Convierte las columnas numéricas a tipo numérico.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos.
        
    Returns:
        pd.DataFrame: DataFrame con las columnas numéricas convertidas.
    """
    for col in data.columns:
        if is_number(data[col]):
            data[col] = pd.to_numeric(data[col], errors='coerce')
            print(f"Columna '{col}' convertida a numérica.")
    return data