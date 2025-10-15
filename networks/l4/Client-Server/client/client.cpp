#include <iostream>
#include <fstream>
#include <string>
#include <limits>

#define NOMINMAX
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 4096

// Отправка байтов
bool sendAll(SOCKET sock, const char* buffer, int length) {
    int totalSent = 0;
    while (totalSent < length) {
        int sent = send(sock, buffer + totalSent, length - totalSent, 0);
        if (sent == SOCKET_ERROR) {
            int errorCode = WSAGetLastError();
            if (errorCode == WSAECONNRESET || errorCode == WSAECONNABORTED || errorCode == WSAENOTCONN) {
                std::cerr << "Ошибка: сервер разорвал соединение.\n";
            } else {
                std::cerr << "Ошибка отправки данных: " << errorCode << "\n";
            }
            return false;
        }
        totalSent += sent;
    }
    return true;
}

// Получение байтов
bool recvAll(SOCKET sock, char* buffer, int length) {
    int totalReceived = 0;
    while (totalReceived < length) {
        int received = recv(sock, buffer + totalReceived, length - totalReceived, 0);
        if (received == SOCKET_ERROR) {
            int errorCode = WSAGetLastError();
            if (errorCode == WSAECONNRESET || errorCode == WSAECONNABORTED || errorCode == WSAENOTCONN) {
                std::cerr << "Ошибка: сервер разорвал соединение.\n";
            } else {
                std::cerr << "Ошибка получения данных: " << errorCode << "\n";
            }
            return false;
        }
        if (received == 0) {
            std::cerr << "Ошибка: сервер закрыл соединение.\n";
            return false;
        }
        totalReceived += received;
    }
    return true;
}

// Отправка 64-битного числа
bool sendInt64(SOCKET sock, int64_t value) {
    int64_t networkValue = _byteswap_uint64(value); // Преобразуем в network byte order
    return sendAll(sock, reinterpret_cast<const char*>(&networkValue), sizeof(networkValue));
}

// Получение 64-битного числа
bool recvInt64(SOCKET sock, int64_t& value) {
    int64_t networkValue;
    if (!recvAll(sock, reinterpret_cast<char*>(&networkValue), sizeof(networkValue))) {
        return false;
    }
    value = _byteswap_uint64(networkValue); // Преобразуем из network byte order
    return true;
}

// Отправка строки с префиксом длины
bool sendString(SOCKET sock, const std::string& str) {
    int64_t length = static_cast<int64_t>(str.length());
    if (!sendInt64(sock, length)) {
        return false;
    }
    if (length > 0) {
        return sendAll(sock, str.c_str(), static_cast<int>(length));
    }
    return true;
}

// Получение строки с префиксом длины
bool recvString(SOCKET sock, std::string& str) {
    int64_t length;
    if (!recvInt64(sock, length)) {
        return false;
    }
    if (length < 0 || length > 1024 * 1024) { // Ограничение в 1 МБ для имени
        std::cerr << "Некорректная длина строки: " << length << "\n";
        return false;
    }
    if (length == 0) {
        str.clear();
        return true;
    }
    
    char* buffer = new char[length];
    bool success = recvAll(sock, buffer, static_cast<int>(length));
    if (success) {
        str.assign(buffer, length);
    }
    delete[] buffer;
    return success;
}

// Безопасный ввод целого числа
bool getIntInput(int& value, int minVal, int maxVal) {
    while (true) {
        if (std::cin >> value) {
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            if (value >= minVal && value <= maxVal) {
                return true;
            }
            std::cout << "Число должно быть в диапазоне от " << minVal << " до " << maxVal << ". Попробуйте снова: ";
        } else {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Некорректный ввод. Введите целое число: ";
        }
    }
}

// Безопасный ввод строки
std::string getStringInput(const std::string& prompt) {
    std::string input;
    std::cout << prompt;
    std::getline(std::cin, input);
    return input;
}

void uploadFile(SOCKET serverSocket) {
    std::string fileName = getStringInput("Введите путь к файлу для отправки: ");
    if (fileName.empty()) {
        std::cerr << "Имя файла не может быть пустым.\n";
        return;
    }

    std::ifstream inFile(fileName, std::ios::binary);
    if (!inFile.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл \"" << fileName << "\".\n";
        return;
    }

    // Получаем размер файла
    inFile.seekg(0, std::ios::end);
    int64_t fileSize = inFile.tellg();
    inFile.seekg(0, std::ios::beg);

    if (fileSize < 0) {
        std::cerr << "Ошибка определения размера файла.\n";
        inFile.close();
        return;
    }

    if (fileSize == 0) {
        std::cout << "Предупреждение: файл пустой.\n";
    }

    // Запрашиваем имя файла на сервере
    std::string serverFileName = getStringInput("Введите имя для сохранения на сервере (Enter - оригинальное имя): ");
    if (serverFileName.empty()) {
        // Извлекаем имя файла из пути
        size_t pos = fileName.find_last_of("\\/");
        serverFileName = (pos != std::string::npos) ? fileName.substr(pos + 1) : fileName;
    }

    std::cout << "Отправка файла \"" << fileName << "\" (" << fileSize << " байт) как \"" << serverFileName << "\"...\n";

    // Отправляем протокол: UPLOAD <имя_файла> <размер>
    if (!sendString(serverSocket, "UPLOAD")) {
        std::cerr << "Ошибка отправки команды. Возможно, сервер недоступен.\n";
        inFile.close();
        return;
    }

    if (!sendString(serverSocket, serverFileName)) {
        std::cerr << "Ошибка отправки имени файла. Возможно, сервер недоступен.\n";
        inFile.close();
        return;
    }

    if (!sendInt64(serverSocket, fileSize)) {
        std::cerr << "Ошибка отправки размера файла. Возможно, сервер недоступен.\n";
        inFile.close();
        return;
    }

    // Отправляем содержимое файла
    char buffer[BUFFER_SIZE];
    int64_t totalSent = 0;
    
    while (totalSent < fileSize) {
        int64_t remaining = fileSize - totalSent;
        int toRead = static_cast<int>((remaining < BUFFER_SIZE) ? remaining : BUFFER_SIZE);
        
        inFile.read(buffer, toRead);
        std::streamsize bytesRead = inFile.gcount();
        
        if (bytesRead <= 0) {
            std::cerr << "Ошибка чтения файла.\n";
            inFile.close();
            return;
        }

        if (!sendAll(serverSocket, buffer, static_cast<int>(bytesRead))) {
            std::cerr << "Ошибка отправки данных файла. Передача прервана.\n";
            inFile.close();
            return;
        }
        
        totalSent += bytesRead;
    }
    
    inFile.close();
    std::cout << "Файл успешно отправлен (" << totalSent << " байт).\n";

    // Получаем ответ сервера
    std::string response;
    if (recvString(serverSocket, response)) {
        std::cout << "Ответ сервера: " << response << "\n";
    } else {
        std::cerr << "Ошибка получения ответа от сервера. Возможно, сервер недоступен.\n";
    }
}

void downloadFile(SOCKET serverSocket) {
    std::string serverFileName = getStringInput("Введите имя файла на сервере для скачивания: ");
    if (serverFileName.empty()) {
        std::cerr << "Имя файла не может быть пустым.\n";
        return;
    }

    std::string localFileName = getStringInput("Введите имя для сохранения (Enter - использовать имя с сервера): ");
    if (localFileName.empty()) {
        localFileName = serverFileName;
    }

    // Отправляем команду DOWNLOAD <имя_файла>
    if (!sendString(serverSocket, "DOWNLOAD")) {
        std::cerr << "Ошибка отправки команды. Возможно, сервер недоступен.\n";
        return;
    }

    if (!sendString(serverSocket, serverFileName)) {
        std::cerr << "Ошибка отправки имени файла. Возможно, сервер недоступен.\n";
        return;
    }

    // Получаем ответ: статус (OK/ERROR) и размер файла
    std::string status;
    if (!recvString(serverSocket, status)) {
        std::cerr << "Ошибка получения статуса от сервера. Возможно, сервер недоступен.\n";
        return;
    }

    if (status == "ERROR") {
        std::string errorMsg;
        if (recvString(serverSocket, errorMsg)) {
            std::cerr << "Ошибка сервера: " << errorMsg << "\n";
        } else {
            std::cerr << "Файл не найден или ошибка на сервере.\n";
        }
        return;
    }

    if (status != "OK") {
        std::cerr << "Неизвестный статус от сервера: " << status << "\n";
        return;
    }

    // Получаем размер файла
    int64_t fileSize;
    if (!recvInt64(serverSocket, fileSize)) {
        std::cerr << "Ошибка получения размера файла. Возможно, сервер недоступен.\n";
        return;
    }

    if (fileSize < 0) {
        std::cerr << "Некорректный размер файла: " << fileSize << "\n";
        return;
    }

    std::cout << "Получение файла \"" << serverFileName << "\" (" << fileSize << " байт)...\n";

    // Открываем файл для записи
    std::ofstream outFile(localFileName, std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл \"" << localFileName << "\" для записи.\n";
        return;
    }

    // Получаем данные файла
    char buffer[BUFFER_SIZE];
    int64_t totalReceived = 0;

    while (totalReceived < fileSize) {
        int64_t remaining = fileSize - totalReceived;
        int toReceive = static_cast<int>((remaining < BUFFER_SIZE) ? remaining : BUFFER_SIZE);

        if (!recvAll(serverSocket, buffer, toReceive)) {
            std::cerr << "Ошибка получения данных файла. Передача прервана.\n";
            outFile.close();
            return;
        }

        outFile.write(buffer, toReceive);
        if (!outFile) {
            std::cerr << "Ошибка записи в файл.\n";
            outFile.close();
            return;
        }

        totalReceived += toReceive;
    }

    outFile.close();

    std::cout << "Файл успешно скачан и сохранен как \"" << localFileName 
              << "\" (" << totalReceived << " байт).\n";
}

void interactWithServer(SOCKET serverSocket) {
    while (true) {
        std::cout << "\n========== МЕНЮ ==========\n"
                  << "1. Отправить файл на сервер (upload)\n"
                  << "2. Скачать файл с сервера (download)\n"
                  << "3. Выйти\n"
                  << "==========================\n"
                  << "Введите номер команды (1-3): ";
        
        int choice;
        if (!getIntInput(choice, 1, 3)) {
            continue;
        }

        switch (choice) {
        case 1:
            uploadFile(serverSocket);
            break;
        case 2:
            downloadFile(serverSocket);
            break;
        case 3:
            std::cout << "Завершение работы клиента...\n";
            if (!sendString(serverSocket, "EXIT")) {
                std::cerr << "Предупреждение: не удалось отправить команду завершения серверу.\n";
            }
            return;
        }
    }
}

int main() {
    WSADATA wsaData;
    SOCKET clientSocket = INVALID_SOCKET;
    sockaddr_in serverAddr{};

    setlocale(LC_ALL, "Russian");

    // Инициализация Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Ошибка инициализации Winsock.\n";
        system("pause");
        return 1;
    }

    // Создаем сокет TCP
    clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (clientSocket == INVALID_SOCKET) {
        std::cerr << "Ошибка создания сокета: " << WSAGetLastError() << "\n";
        WSACleanup();
        system("pause");
        return 1;
    }

    // Настраиваем адрес сервера
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);

    std::string serverIP = getStringInput("Введите IP-адрес сервера (Enter - 127.0.0.1): ");
    
    if (serverIP.empty()) {
        serverIP = "127.0.0.1";
        std::cout << "Используется адрес по умолчанию: " << serverIP << "\n";
    }

    if (inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr) <= 0) {
        std::cerr << "Некорректный IP-адрес \"" << serverIP << "\".\n";
        closesocket(clientSocket);
        WSACleanup();
        system("pause");
        return 1;
    }

    // Подключаемся к серверу
    std::cout << "Попытка подключения к серверу " << serverIP << ":" << PORT << "...\n";
    if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Ошибка подключения к серверу: " << WSAGetLastError() << "\n";
        std::cerr << "Убедитесь, что сервер запущен и доступен.\n";
        closesocket(clientSocket);
        WSACleanup();
        system("pause");
        return 1;
    }

    std::cout << "Подключение к серверу успешно установлено.\n";
    
    // Взаимодействие с сервером
    interactWithServer(clientSocket);

    // Закрываем сокет и очищаем Winsock
    std::cout << "\nЗакрытие соединения...\n";
    
    // Корректное закрытие соединения
    shutdown(clientSocket, SD_BOTH); // Закрываем отправку и получение
    closesocket(clientSocket);
    WSACleanup();
    
    std::cout << "Соединение закрыто.\n";
    std::cout << "\nНажмите любую клавишу для выхода...\n";
    system("pause");
    
    return 0;
}
