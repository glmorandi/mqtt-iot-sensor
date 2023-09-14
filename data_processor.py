import numpy as np

class DataProcessor:
    def remove_outliers(self, data, threshold):
        data = np.array(data)

        # Calcula o z score para os dados
        z_scores = (data - np.mean(data)) / np.std(data)

        # Utiliza indexação booleana para remover outliers baseado no threshold
        cleaned_data = data[abs(z_scores) < threshold]

        # Calcula a média dos dados e retorna
        cleaned_mean = np.mean(cleaned_data)
        return cleaned_mean
    