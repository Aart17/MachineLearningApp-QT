import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model


class RegressionConstructor:
    def __init__(self, dataset_path, target, graphics, *args, **kwargs):
        self.dataset_path = dataset_path
        self.target = target
        self.graphics = graphics

    data = pd.read_excel('Concrete_Data.xls')
    y = data['Cement (component 1)(kg in a m^3 mixture)']
    x = data.drop('Cement (component 1)(kg in a m^3 mixture)', axis=1)

    # Разбиение набора данных на обучающую и тестовую части
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=21)

    # Нормировка данных
    scaler = StandardScaler()

    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    # Создание модели
    linear_regression_model = linear_model.LinearRegression()

    # Обучение модели
    linear_regression_model.fit(x_train, y_train)

    # Тестирование модели
    test_predictions = linear_regression_model.predict(x_test)

    # Построение графика
    plt.figure(figsize=(5, 5))
    plt.scatter(y_test, test_predictions)  # рисуем точки, соответствущие парам настоящее значение - прогноз
    plt.plot([50, 500], [50, 500])  # рисуем прямую, на которой предсказания и настоящие значения совпадают
    plt.xlabel('Настоящая прочность', fontsize=15)
    plt.ylabel('Предсказанная прочность', fontsize=15)

    # Расчет ошибки
    r2 = linear_regression_model.score(x_test, y_test)
    print('Точность: ' + str(r2))

    plt.show()
