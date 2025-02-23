import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# Función para descargar una parte del archivo
def download_chunk(url, start_byte, end_byte, file_name):
    headers = {'Range': f"bytes={start_byte}-{end_byte}"}
        request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                    chunk = response.read()
                            with open(file_name, 'r+b') as f:
                                        f.seek(start_byte)
                                                    f.write(chunk)
                                                            print(f"Descargado byte {start_byte} a {end_byte}")

                                                            # Función para obtener el tamaño del archivo
                                                            def get_file_size(url):
                                                                with urllib.request.urlopen(url) as response:
                                                                        return int(response.headers["Content-Length"])

                                                                        # Función principal para manejar la descarga concurrente
                                                                        def download_file(url, file_name, num_chunks=4):
                                                                            # Obtener el tamaño total del archivo
                                                                                file_size = get_file_size(url)

                                                                                    # Crear un archivo vacío en el disco con el tamaño del archivo
                                                                                        with open(file_name, 'wb') as f:
                                                                                                f.truncate(file_size)

                                                                                                    # Calcular el tamaño de cada fragmento
                                                                                                        chunk_size = file_size // num_chunks

                                                                                                            # Crear un ThreadPoolExecutor para la descarga en paralelo
                                                                                                                with ThreadPoolExecutor(max_workers=num_chunks) as executor:
                                                                                                                        futures = []
                                                                                                                                for i in range(num_chunks):
                                                                                                                                            start_byte = i * chunk_size
                                                                                                                                                        end_byte = start_byte + chunk_size - 1 if i < num_chunks - 1 else file_size - 1

                                                                                                                                                                    futures.append(executor.submit(download_chunk, url, start_byte, end_byte, file_name))

                                                                                                                                                                            # Esperar a que todas las descargas terminen
                                                                                                                                                                                    for future in futures:
                                                                                                                                                                                                future.result()

                                                                                                                                                                                                # Uso de la función
                                                                                                                                                                                                url = 'https://example.com/largefile.zip'  # URL del archivo a descargar
                                                                                                                                                                                                file_name = 'largefile.zip'  # Nombre del archivo a guardar
                                                                                                                                                                                                download_file(url, file_name, num_chunks=4)