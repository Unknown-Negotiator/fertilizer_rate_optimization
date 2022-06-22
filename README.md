# fertilizer_rate_optimization
## Цель модели
Основная функциональная цель модели «Оптимизация МУ»: автоматически подобрать оптимальные минеральные удобрения (МУ), а также нормы их внесения. Оптимальное решение - наиболее благоприятное решение для максимизации маржинальной прибыли (Gross Margin) по конкретному варианту «поле-продукция-плановая урожайность».
## Термины и сокращения
Поле - участок земли, который используется для сельскохозяйственных целей. Иерархия: Территория (Холдинг) -> Хозяйство -> Поле.
Продукция - сырой товар растительного происхождения. Пример: Сахарная свекла, Пшеница, Горох, Семена гороха.
Урожайность продукции в т/га - объем собранного урожая (готовой продукции).
МУ (минеральное удобрение) - неорганическое соединение, содержащее необходимые для растений элементы питания. МУ повышает урожайность, способствует насыщению почвы необходимыми макроэлементами.
Норма внесения МУ - объем МУ в кг/га, который необходимо внести на поле для соблюдения норм внесения макроэлементов. Каждое МУ содержит некоторое кол-во каждого макроэлемента. Норма внесения МУ рассчитывается в модели оптимизации. 
Норма внесения макроэлемента (P, K) - объем макроэлемента в кг д.в./га, который необходимо внести на поле для достижения плановой урожайности - входные данными модели.
Агрооперация - период внесения удобрений. Пример: Предпосевное внесение удобрений, Подкормка культуры, Основное внесение удобрений, Внесение жидких удобрений.
## Принцип работы модели
Модель должна позволять выполнять расчеты на 1 сезон (год) для 1 хозяйства (хозяйство содержит ограниченное множество полей).
Расчет включает следующие этапы:
*	определение оптимальных норм внесения МУ, затрат на МУ при максимизации маржинальной прибыли для конкретного варианта «поле-продукция-плановая урожайность»;
*	формирование выходных витрин для всех допустимых вариантов «поле-продукция-плановая урожайность»: финансовые показатели, вносимые МУ.
Источники данных
## Постановка задачи 
Необходимо по заданному Хозяйству на заданный сезон реализовать последовательный вызов расчетов для каждого варианта «поле-продукция-плановая урожайность», каждый отдельный расчет должен выдать сколько и каких минеральных удобрений должно быть внесено для достижения оптимального значения целевой функции.
## Целевая функция
Решение оптимизационной задачи выбора минеральных удобрений для поля достигается путем максимизации целевой функции Gross Margin = TR - VC → max.
Gross Margin – маржинальная прибыль;
TR – суммарная выручка от реализации ГП;
VC – сумма переменных и постоянных затрат на выращивание продукции.
## Параметры управления
Параметры управления оптимизационной задачи – это такие параметры, с помощью изменения которых формируется оптимальное решение.
1.	Объем внесенных МУ (условные единицы) - целое число >=0.
2.	Факт внесения МУ в конкретную агрооперацию (бинарная переменная, 1 – внесли, 0 – не внесли).
##	Ограничения
Основные ограничения, принятые в рамках модели:
1.	Допустимые удобрения для хозяйства (in_farm_fert_available_mm);
2.	Допустимые удобрения для каждой продукции и агрооперации (in_product_fertilizers);
3.	Диапазон объема внесенного удобрения в агрооперацию (in_product_fertilizers);
4.	Нижняя граница количества внесенного макроэлемента – норма внесения макроэлемента для достижения плановой урожайности поля (in_fields_data_chain_item);
5.	Нижняя граница доз удобрений, который может внести разбрасыватель удобрений (по типу удобрений) - шаг внесения (in_fert_step_mm);
6.	Ограничение на количество внесений МУ в 1 агрооперацию: в 1 агрооперацию можно внести только 1 МУ. Пример: Если в агрооперацию "Подкормка культуры" внесено МУ "Аммофос (N:P=12:52)", другие МУ в эту агрооперацию вносить нельзя.
7.	Одно МУ может применяться только в 1 агрооперацию (одно МУ нельзя использовать более чем в 1 агрооперации). Пример: Если МУ "Аммофос (N:P=12:52)" внесено в агрооперацию "Подкормка культуры", то это МУ нельзя вносить в другие агрооперации.
## Результат работы модели
Результатом оптимизационного моделирования являются выходные витрины, содержащие затраты на МУ, плановую маржинальную прибыль, определенные в ходе решения оптимизационной задачи, а также нормы внесения МУ.
Допустимая точность решения = 1%
Состав выходных данных
Перечень выходных данных по результатам работы модели включает:
1.	Финансовые показатели;
2.	Внесенные удобрения.
Выходные витрины должны содержать результаты оптимизации МУ вариантов «поле-продукция-плановая урожайность», для которых расчет оптимизации окончился успешно.
Если в расчет закончился неуспешно (решение не найдено или найдено неоптимальное решение, не удовлетворяющее ограничениям), то в выходные таблицы для варианта ничего не сохраняется.
