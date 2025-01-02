# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import zipfile
import csv

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```
    """
    # Define paths
    zip_file_path = "files/input.zip"
    unzip_folder_path = "files/input"
    output_folder_path = "files/output"
    train_csv_path = os.path.join(output_folder_path, "train_dataset.csv")
    test_csv_path = os.path.join(output_folder_path, "test_dataset.csv")

    # Ensure output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    def extract_zip(zip_path, extract_to):
        """Extracts a zip file to the specified location."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def find_correct_base_path(base_path):
        """Finds the correct base path by inspecting the folder structure."""
        for root, dirs, _ in os.walk(base_path):
            if "train" in dirs and "test" in dirs:
                return root
        return base_path

    def read_txt_files_to_csv(base_path):
        """Reads .txt files from directories and writes their content to CSV files."""
        base_path = find_correct_base_path(base_path)  # Dynamically find correct base path
        for split in ["train", "test"]:
            split_path = os.path.join(base_path, split)
            data = []
            for sentiment in ["negative", "neutral", "positive"]:
                sentiment_path = os.path.join(split_path, sentiment)
                if not os.path.exists(sentiment_path):
                    print(f"Directory not found: {sentiment_path}")
                    continue

                for txt_file in os.listdir(sentiment_path):
                    if txt_file.endswith(".txt"):
                        file_path = os.path.join(sentiment_path, txt_file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            phrase = f.read().strip()
                            data.append({"phrase": phrase, "sentiment": sentiment})

            # Write data to CSV
            csv_file_path = train_csv_path if split == "train" else test_csv_path
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["phrase", "sentiment"])
                writer.writeheader()
                writer.writerows(data)

    # Step 1: Extract the zip file
    extract_zip(zip_file_path, unzip_folder_path)

    # Step 2: Process the extracted files and write to CSV
    read_txt_files_to_csv(unzip_folder_path)

