import pandas
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model


class RegressionConstructor:
    def __init__(self, data_context: {}):
        self.linear_regression_model = None
        self.x_train = None
        self.x_test = None
        self.y_test = None
        self.y_train = None
        self.data = None
        self.data_context = data_context

    def create_data(self):
        match self.data_context['file_type']:
            case 'csv':
                self.data = pandas.read_csv(self.data_context['data_path'])
            case 'xls':
                self.data = pd.read_excel(self.data_context['data_path'])
            case 'xml':
                self.data = pd.read_xml(self.data_context['data_path'])
            case '*wf':
                self.data = pd.read_fwf(self.data_context['data_path'])
            case 'json':
                self.data = pd.read_json(self.data_context['data_path'])
        self.data = self.data.dropna(how='any')
        y = self.data[self.data_context['target_value']]
        x = self.data.drop(self.data_context['target_value'], axis=1)

        # Разбиение набора данных на обучающую и тестовую части
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y,
                                                                                test_size=0.20, random_state=21)
        # Нормировка данных
        scaler = StandardScaler()

        self.x_train = scaler.fit_transform(self.x_train)
        self.x_test = scaler.transform(self.x_test)

    def create_model(self):
        # Создание модели
        self.linear_regression_model = linear_model.LinearRegression()

        # Обучение модели
        self.linear_regression_model.fit(self.x_train, self.y_train)

    def create_graphics(self):
        # Тестирование модели
        test_predictions = self.linear_regression_model.predict(self.x_test)

        # Построение графика
        if self.data_context['graphics']['hist']:
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            axs[0].hist(test_predictions, color='lightblue')
            axs[0].set_title('Предсказанное значение')
            axs[1].hist(self.y_test, color='orange')
            axs[1].set_title('Настоящее значение')
        if self.data_context['graphics']['sct']:
            plt.figure(figsize=(5, 5))
            # рисуем точки, соответствущие парам настоящее значение - прогноз
            plt.scatter(self.y_test, test_predictions)
            # рисуем прямую, на которой предсказания и настоящие значения совпадают
            plt.plot([50, 500], [50, 500])
            plt.xlabel('Настоящее значение', fontsize=15)
            plt.ylabel('Предсказанное значение', fontsize=15)
        if self.data_context['graphics']['mtrx']:
            from sklearn.metrics import confusion_matrix
            import seaborn as sns
            # Отображение матрицы соответствий
            conf_matrix = confusion_matrix(test_predictions, self.y_test)
            sns.heatmap(conf_matrix, annot=True, fmt='.0f')

        # Расчет ошибки
        r2 = self.linear_regression_model.score(self.x_test, self.y_test)
        print(f'<h2 style="color: green;>"Точность: {str(r2)}<h2>')
        plt.show()

    def construct_model(self):
        self.create_data()
        self.create_model()
        self.create_graphics()
