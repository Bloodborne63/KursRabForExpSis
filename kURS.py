import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QCheckBox, QStackedWidget,
                             QProgressBar, QMessageBox, QDialog, QScrollArea,
                             QGroupBox, QComboBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDateTime


class NameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод данных")
        self.setWindowIcon(QIcon('icon.png'))
        self.setModal(True)

        layout = QVBoxLayout()

        title = QLabel("Перед началом теста")
        title.setFont(QFont('Arial', 16, QFont.Bold))

        label = QLabel("Введите ваше ФИО:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Иванов Иван Иванович")

        self.start_btn = QPushButton("Начать тест")
        self.start_btn.clicked.connect(self.check_name)

        layout.addWidget(title)
        layout.addWidget(label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def check_name(self):
        name = self.name_input.text().strip()
        if len(name.split()) < 2:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите полное ФИО (минимум 2 слова)!")
            return
        self.accept()


class CovidRiskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.current_page = 0
        self.user_name = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('COVID-19 Risk Calculator')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QCheckBox {
                spacing: 8px;
            }
            QProgressBar {
                text-align: center;
                height: 10px;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        # Главный контейнер
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setMaximum(3)
        self.layout.addWidget(self.progress)

        # Стек страниц
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Страницы
        self.create_page1()  # Основные данные
        self.create_page2()  # Факторы здоровья
        self.create_page3()  # Образ жизни и контакты
        self.create_page4()  # Результат

        # Кнопки навигации
        self.nav_layout = QHBoxLayout()
        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(self.prev_page)
        self.btn_next = QPushButton("Далее")
        self.btn_next.clicked.connect(self.next_page)
        self.btn_history = QPushButton("История")
        self.btn_history.clicked.connect(self.show_history)

        self.nav_layout.addWidget(self.btn_back)
        self.nav_layout.addWidget(self.btn_next)
        self.nav_layout.addWidget(self.btn_history)
        self.layout.addLayout(self.nav_layout)

        self.update_nav_buttons()
        self.show_name_dialog()

    def show_name_dialog(self):
        dialog = NameDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.user_name = dialog.name_input.text().strip()
            return True
        else:
            return False

    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Шаг 1/4: Основные данные")
        title.setFont(QFont('Arial', 16, QFont.Bold))

        # Группа персональных данных
        personal_group = QGroupBox("Персональные данные")
        personal_layout = QVBoxLayout()

        age_label = QLabel("Возраст:")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Например: 35")

        gender_label = QLabel("Пол:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Мужской", "Женский"])

        personal_layout.addWidget(age_label)
        personal_layout.addWidget(self.age_input)
        personal_layout.addWidget(gender_label)
        personal_layout.addWidget(self.gender_combo)
        personal_group.setLayout(personal_layout)

        # Группа антропометрических данных
        anthro_group = QGroupBox("Антропометрические данные")
        anthro_layout = QVBoxLayout()

        weight_label = QLabel("Вес (кг):")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Например: 70")

        height_label = QLabel("Рост (см):")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Например: 175")

        anthro_layout.addWidget(weight_label)
        anthro_layout.addWidget(self.weight_input)
        anthro_layout.addWidget(height_label)
        anthro_layout.addWidget(self.height_input)
        anthro_group.setLayout(anthro_layout)

        layout.addWidget(title)
        layout.addWidget(personal_group)
        layout.addWidget(anthro_group)
        layout.addStretch()

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Шаг 2/4: Факторы здоровья")
        title.setFont(QFont('Arial', 16, QFont.Bold))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()

        # Хронические заболевания
        chronic_group = QGroupBox("Хронические заболевания")
        chronic_layout = QVBoxLayout()

        self.diabetes_check = QCheckBox("Сахарный диабет")
        self.hypertension_check = QCheckBox("Артериальная гипертензия")
        self.cvd_check = QCheckBox("Сердечно-сосудистые заболевания")
        self.lung_disease_check = QCheckBox("Хронические болезни лёгких")
        self.kidney_check = QCheckBox("Хроническая болезнь почек")
        self.liver_check = QCheckBox("Хронические заболевания печени")
        self.cancer_check = QCheckBox("Онкологические заболевания")
        self.autoimmune_check = QCheckBox("Аутоиммунные заболевания")

        chronic_layout.addWidget(self.diabetes_check)
        chronic_layout.addWidget(self.hypertension_check)
        chronic_layout.addWidget(self.cvd_check)
        chronic_layout.addWidget(self.lung_disease_check)
        chronic_layout.addWidget(self.kidney_check)
        chronic_layout.addWidget(self.liver_check)
        chronic_layout.addWidget(self.cancer_check)
        chronic_layout.addWidget(self.autoimmune_check)
        chronic_group.setLayout(chronic_layout)

        # Иммунный статус
        immune_group = QGroupBox("Иммунный статус")
        immune_layout = QVBoxLayout()

        self.immune_check = QCheckBox("Первичный иммунодефицит")
        self.hiv_check = QCheckBox("ВИЧ/СПИД")
        self.transplant_check = QCheckBox("Трансплантация органов")
        self.steroids_check = QCheckBox("Длительный приём кортикостероидов")
        self.chemotherapy_check = QCheckBox("Химиотерапия")

        immune_layout.addWidget(self.immune_check)
        immune_layout.addWidget(self.hiv_check)
        immune_layout.addWidget(self.transplant_check)
        immune_layout.addWidget(self.steroids_check)
        immune_layout.addWidget(self.chemotherapy_check)
        immune_group.setLayout(immune_layout)

        # Вакцинация
        vaccine_group = QGroupBox("Вакцинация")
        vaccine_layout = QVBoxLayout()

        self.vaccine_check = QCheckBox("Вакцинация от COVID-19 (последние 6 мес.)")
        self.flu_vaccine_check = QCheckBox("Вакцинация от гриппа (последний год)")
        self.pneumo_vaccine_check = QCheckBox("Вакцинация от пневмококка")

        vaccine_layout.addWidget(self.vaccine_check)
        vaccine_layout.addWidget(self.flu_vaccine_check)
        vaccine_layout.addWidget(self.pneumo_vaccine_check)
        vaccine_group.setLayout(vaccine_layout)

        content_layout.addWidget(title)
        content_layout.addWidget(chronic_group)
        content_layout.addWidget(immune_group)
        content_layout.addWidget(vaccine_group)
        content_layout.addStretch()

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_page3(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Шаг 3/4: Образ жизни и контакты")
        title.setFont(QFont('Arial', 16, QFont.Bold))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()

        # Вредные привычки
        habits_group = QGroupBox("Вредные привычки")
        habits_layout = QVBoxLayout()

        self.smoking_check = QCheckBox("Курение (текущее или в прошлом)")
        self.alcohol_check = QCheckBox("Злоупотребление алкоголем")
        self.drugs_check = QCheckBox("Употребление наркотических веществ")

        habits_layout.addWidget(self.smoking_check)
        habits_layout.addWidget(self.alcohol_check)
        habits_layout.addWidget(self.drugs_check)
        habits_group.setLayout(habits_layout)

        # Физическая активность
        activity_group = QGroupBox("Физическая активность")
        activity_layout = QVBoxLayout()

        self.sedentary_check = QCheckBox("Малоподвижный образ жизни")
        self.no_sport_check = QCheckBox("Отсутствие регулярных физических нагрузок")

        activity_layout.addWidget(self.sedentary_check)
        activity_layout.addWidget(self.no_sport_check)
        activity_group.setLayout(activity_layout)

        # Психологическое состояние
        psycho_group = QGroupBox("Психологическое состояние")
        psycho_layout = QVBoxLayout()

        self.stress_check = QCheckBox("Хронический стресс")
        self.depression_check = QCheckBox("Депрессия")
        self.sleep_check = QCheckBox("Нарушения сна")

        psycho_layout.addWidget(self.stress_check)
        psycho_layout.addWidget(self.depression_check)
        psycho_layout.addWidget(self.sleep_check)
        psycho_group.setLayout(psycho_layout)

        # Контакты и профессия
        contacts_group = QGroupBox("Контакты и профессия")
        contacts_layout = QVBoxLayout()

        self.contacts_check = QCheckBox("Контакт с больными COVID-19")
        self.medic_check = QCheckBox("Работа в медицинской сфере")
        self.crowd_check = QCheckBox("Частое нахождение в местах скопления людей")
        self.travel_check = QCheckBox("Недавние поездки в зоны риска")

        contacts_layout.addWidget(self.contacts_check)
        contacts_layout.addWidget(self.medic_check)
        contacts_layout.addWidget(self.crowd_check)
        contacts_layout.addWidget(self.travel_check)
        contacts_group.setLayout(contacts_layout)

        # Беременность
        self.pregnancy_check = QCheckBox("Беременность (для женщин)")

        content_layout.addWidget(title)
        content_layout.addWidget(habits_group)
        content_layout.addWidget(activity_group)
        content_layout.addWidget(psycho_group)
        content_layout.addWidget(contacts_group)
        content_layout.addWidget(self.pregnancy_check)
        content_layout.addStretch()

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        page.setLayout(layout)
        self.stacked_widget.addWidget(page)

    def create_page4(self):
        self.result_page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Результат оценки риска")
        title.setFont(QFont('Arial', 16, QFont.Bold))

        self.result_label = QLabel()
        self.result_label.setFont(QFont('Arial', 14))
        self.result_label.setAlignment(Qt.AlignCenter)

        self.recommendations_label = QLabel()
        self.recommendations_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(self.result_label)
        layout.addWidget(self.recommendations_label)
        layout.addStretch()

        self.result_page.setLayout(layout)
        self.stacked_widget.addWidget(self.result_page)

    def next_page(self):
        if self.current_page < self.stacked_widget.count() - 1:
            self.current_page += 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.progress.setValue(self.current_page)
            self.update_nav_buttons()

            if self.current_page == 3:
                self.save_to_history()
                self.calculate_risk()
        elif self.btn_next.text() == "Завершить":
            self.reset_to_start()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.stacked_widget.setCurrentIndex(self.current_page)
            self.progress.setValue(self.current_page)
            self.update_nav_buttons()

    def update_nav_buttons(self):
        self.btn_back.setVisible(self.current_page != 0)
        self.btn_next.setText("Далее" if self.current_page != 3 else "Завершить")

    def reset_to_start(self):
        """Сброс к начальному состоянию с запросом ФИО"""
        # Очистка всех полей ввода
        self.age_input.clear()
        self.weight_input.clear()
        self.height_input.clear()
        self.gender_combo.setCurrentIndex(0)

        # Сброс всех чекбоксов
        for cb in self.findChildren(QCheckBox):
            cb.setChecked(False)

        # Показываем диалог ввода ФИО
        if not self.show_name_dialog():
            return  # Если пользователь отменил ввод ФИО

        # Сброс страниц и прогресса
        self.current_page = 0
        self.stacked_widget.setCurrentIndex(0)
        self.progress.setValue(0)
        self.update_nav_buttons()

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "История", "История оценок пуста.")
            return

        history_text = "<b>История оценок:</b><br><br>"
        for record in reversed(self.history):
            history_text += f"<b>{record['дата']}</b><br>"
            history_text += f"ФИО: {record['ФИО']}<br>"
            history_text += f"Возраст: {record['данные']['возраст']}<br>"
            history_text += f"Пол: {record['данные']['пол']}<br>"
            history_text += f"Вес/рост: {record['данные']['вес']}кг/{record['данные']['рост']}см<br>"
            history_text += f"Факторы: {', '.join(record['данные']['факторы'])}<br>"
            history_text += f"<span style='color:{record['результат']['цвет']};'>"
            history_text += f"Результат: {record['результат']['текст']}</span><br><hr>"

        msg = QMessageBox()
        msg.setWindowTitle("История оценок")
        msg.setTextFormat(Qt.RichText)
        msg.setText(history_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def save_to_history(self):
        data = {
            "возраст": self.age_input.text(),
            "пол": self.gender_combo.currentText(),
            "вес": self.weight_input.text(),
            "рост": self.height_input.text(),
            "факторы": self.get_checked_factors()
        }

        self.history.append({
            "ФИО": self.user_name,
            "дата": QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm"),
            "данные": data,
            "результат": {
                "текст": self.result_label.text(),
                "цвет": "red" if "🔴" in self.result_label.text() else
                "orange" if "🟡" in self.result_label.text() else "green"
            }
        })

    def get_checked_factors(self):
        factors = []
        for cb in self.findChildren(QCheckBox):
            if cb.isChecked():
                factors.append(cb.text().split(" (")[0])  # Убираем пояснения в скобках

        return factors if factors else ["Нет факторов риска"]

    def calculate_risk(self):
        try:
            age = int(self.age_input.text())
            weight = float(self.weight_input.text())
            height = float(self.height_input.text()) / 100
            bmi = weight / (height ** 2)
            is_female = self.gender_combo.currentText() == "Женский"
        except:
            self.result_label.setText("⚠️ Ошибка: проверьте введённые данные!")
            return

        risk_score = 0

        # 1. Основные параметры
        if age >= 65:
            risk_score += 4
        elif age >= 50:
            risk_score += 3
        elif age >= 40:
            risk_score += 2
        elif age >= 30:
            risk_score += 1

        if bmi >= 40:
            risk_score += 3
        elif bmi >= 35:
            risk_score += 2
        elif bmi >= 30:
            risk_score += 1

        # 2. Хронические заболевания
        if self.diabetes_check.isChecked(): risk_score += 3
        if self.hypertension_check.isChecked(): risk_score += 2
        if self.cvd_check.isChecked(): risk_score += 3
        if self.lung_disease_check.isChecked(): risk_score += 3
        if self.kidney_check.isChecked(): risk_score += 3
        if self.liver_check.isChecked(): risk_score += 2
        if self.cancer_check.isChecked(): risk_score += 4
        if self.autoimmune_check.isChecked(): risk_score += 2

        # 3. Иммунный статус
        if self.immune_check.isChecked(): risk_score += 4
        if self.hiv_check.isChecked(): risk_score += 4
        if self.transplant_check.isChecked(): risk_score += 5
        if self.steroids_check.isChecked(): risk_score += 3
        if self.chemotherapy_check.isChecked(): risk_score += 4

        # 4. Вакцинация (снижают риск)
        if self.vaccine_check.isChecked(): risk_score -= 3
        if self.flu_vaccine_check.isChecked(): risk_score -= 1
        if self.pneumo_vaccine_check.isChecked(): risk_score -= 1

        # 5. Образ жизни
        if self.smoking_check.isChecked(): risk_score += 2
        if self.alcohol_check.isChecked(): risk_score += 1
        if self.drugs_check.isChecked(): risk_score += 2
        if self.sedentary_check.isChecked(): risk_score += 1
        if self.no_sport_check.isChecked(): risk_score += 1

        # 6. Психологическое состояние
        if self.stress_check.isChecked(): risk_score += 1
        if self.depression_check.isChecked(): risk_score += 1
        if self.sleep_check.isChecked(): risk_score += 1

        # 7. Контакты и профессия
        if self.contacts_check.isChecked(): risk_score += 2
        if self.medic_check.isChecked(): risk_score += 2
        if self.crowd_check.isChecked(): risk_score += 1
        if self.travel_check.isChecked(): risk_score += 1

        # 8. Беременность
        if is_female and self.pregnancy_check.isChecked(): risk_score += 2

        # Определение уровня риска
        if risk_score >= 15:
            risk, color = "🔴 Очень высокий", "darkred"
        elif risk_score >= 10:
            risk, color = "🔴 Высокий", "red"
        elif risk_score >= 6:
            risk, color = "🟡 Повышенный", "orange"
        elif risk_score >= 3:
            risk, color = "🟢 Умеренный", "green"
        else:
            risk, color = "🟢 Низкий", "darkgreen"

        self.result_label.setText(
            f'<span style="color: {color}; font-weight: bold;">{risk} риск (баллов: {risk_score})</span>'
        )
        self.recommendations_label.setText(self.get_recommendations(risk_score, age))

    def get_recommendations(self, risk_score, age):
        recommendations = []

        if risk_score >= 10:
            recommendations.append("🔴 Срочно проконсультируйтесь с врачом!")
            recommendations.append("🔴 Максимально ограничьте контакты с другими людьми")
        elif risk_score >= 6:
            recommendations.append("🟡 Рекомендуется консультация врача")
            recommendations.append("🟡 Избегайте людных мест, носите маску")

        # Рекомендации по вакцинации
        if not self.vaccine_check.isChecked():
            recommendations.append("💉 Сделайте прививку от COVID-19 как можно скорее")
        if not self.flu_vaccine_check.isChecked():
            recommendations.append("💉 Рекомендуется вакцинация от гриппа")
        if not self.pneumo_vaccine_check.isChecked() and (self.lung_disease_check.isChecked() or age >= 65):
            recommendations.append("💉 Рекомендуется вакцинация от пневмококка")

        # Рекомендации по образу жизни
        if self.smoking_check.isChecked():
            recommendations.append("🚭 Настоятельно рекомендуется бросить курить")
        if self.alcohol_check.isChecked():
            recommendations.append("🍷 Ограничьте потребление алкоголя")
        if self.sedentary_check.isChecked():
            recommendations.append("🏃 Начните регулярные физические упражнения")
        if self.stress_check.isChecked():
            recommendations.append("🧘 Практикуйте техники релаксации и снижения стресса")
        if self.sleep_check.isChecked():
            recommendations.append("😴 Нормализуйте режим сна (7-9 часов ежедневно)")

        # Общие рекомендации
        recommendations.append("🧼 Соблюдайте гигиену рук и социальную дистанцию")
        recommendations.append("🔄 Регулярно проветривайте помещения")

        if risk_score < 3:
            recommendations.append("🟢 Продолжайте соблюдать меры профилактики")

        return "\n".join(recommendations)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CovidRiskApp()
    ex.resize(600, 500)
    ex.show()
    sys.exit(app.exec_())