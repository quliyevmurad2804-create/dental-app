import sys
import json
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Универсальный адрес через локальное имя (.local) — одинаково работает и дома, и на работе
SERVER_URL = "http://dental-server.local:8000/calendar"

class MobileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dental Soft Mobile")
        self.setGeometry(100, 100, 400, 700)

        # Главный контейнер интерфейса
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # WebView компонент для отображения мобильной версии софта
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(SERVER_URL))
        layout.addWidget(self.browser)

        # Таймер автоматической двусторонней синхронизации каждые 12 секунд
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.trigger_sync)
        self.sync_timer.start(12000) # 12 секунд

    def trigger_sync(self):
        # Фоновый скрипт синхронизации данных с компьютером
        js_code = """
        (async function() {
            try {
                const localData = JSON.parse(localStorage.getItem("offline_db")) || { patients: [], calendar: [] };
                const response = await fetch("http://dental-server.local:8000/api/sync", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(localData)
                });
                if (response.ok) {
                    const result = await response.json();
                    localStorage.setItem("offline_db", JSON.stringify(result.data));
                    console.log("Мобильная автосинхронизация успешна");
                }
            } catch (e) {
                console.log("Сервер вне зоны доступа, работаем офлайн");
            }
        })();
        """
        self.browser.page().runJavaScript(js_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MobileApp()
    window.show()
    sys.exit(app.exec())
