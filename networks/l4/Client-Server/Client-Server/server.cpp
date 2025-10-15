#include <iostream>
#include <fstream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <direct.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 4096

// Отправка байтов
bool sendAll(SOCKET sock, const char* buffer, int length) {
    int totalSent = 0;
    while (totalSent < length) {
        int sent = send(sock, buffer + totalSent, length - totalSent, 0);
        if (sent == SOCKET_ERROR) {
            std::cerr << "Ошибка отправки данных: " << WSAGetLastError() << "\n";
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
            std::cerr << "Ошибка получения данных: " << WSAGetLastError() << "\n";
            return false;
        }
        if (received == 0) {
            std::cerr << "Соединение закрыто удаленной стороной.\n";
            return false;
        }
        totalReceived += received;
    }
    return true;
}

// Отправка 64-битного числа
bool sendInt64(SOCKET sock, int64_t value) {
    int64_t networkValue = _byteswap_uint64(value);
    return sendAll(sock, reinterpret_cast<const char*>(&networkValue), sizeof(networkValue));
}

// Получение 64-битного числа
bool recvInt64(SOCKET sock, int64_t& value) {
    int64_t networkValue;
    if (!recvAll(sock, reinterpret_cast<char*>(&networkValue), sizeof(networkValue))) {
        return false;
    }
    value = _byteswap_uint64(networkValue);
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
    if (length < 0 || length > 1024 * 1024) {
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

void handleUpload(SOCKET clientSocket) {
    // Получаем имя файла
    std::string fileName;
    if (!recvString(clientSocket, fileName)) {
        std::cerr << "Ошибка получения имени файла.\n";
        return;
    }

    // Получаем размер файла
    int64_t fileSize;
    if (!recvInt64(clientSocket, fileSize)) {
        std::cerr << "Ошибка получения размера файла.\n";
        return;
    }

    if (fileSize < 0) {
        std::cerr << "Некорректный размер файла: " << fileSize << "\n";
        sendString(clientSocket, "Ошибка: некорректный размер файла.");
        return;
    }

    std::cout << "Получение файла \"" << fileName << "\" (" << fileSize << " байт)...\n";

    // Создаем папку uploads если её нет
    _mkdir("uploads");

    // Формируем путь к файлу
    std::string filePath = "uploads/" + fileName;

    // Открываем файл для записи
    std::ofstream outFile(filePath, std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Ошибка открытия файла для записи: " << filePath << "\n";
        sendString(clientSocket, "Ошибка: не удалось создать файл на сервере.");
        return;
    }

    // Получаем данные файла
    char buffer[BUFFER_SIZE];
    int64_t totalReceived = 0;

    while (totalReceived < fileSize) {
        int64_t remaining = fileSize - totalReceived;
        int toReceive = static_cast<int>((remaining < BUFFER_SIZE) ? remaining : BUFFER_SIZE);

        if (!recvAll(clientSocket, buffer, toReceive)) {
            std::cerr << "Ошибка получения данных файла.\n";
            outFile.close();
            sendString(clientSocket, "Ошибка: не удалось получить файл полностью.");
            return;
        }

        outFile.write(buffer, toReceive);
        if (!outFile) {
            std::cerr << "Ошибка записи в файл.\n";
            outFile.close();
            sendString(clientSocket, "Ошибка: не удалось записать файл на диск.");
            return;
        }

        totalReceived += toReceive;
    }

    outFile.close();

    std::cout << "Файл успешно получен и сохранен: " << filePath 
              << " (" << totalReceived << " байт).\n";
    
    sendString(clientSocket, "Файл успешно загружен на сервер.");
}

void handleDownload(SOCKET clientSocket) {
    // Получаем имя файла
    std::string fileName;
    if (!recvString(clientSocket, fileName)) {
        std::cerr << "Ошибка получения имени файла.\n";
        return;
    }

    std::cout << "Запрос на скачивание файла \"" << fileName << "\"...\n";

    // Формируем путь к файлу
    std::string filePath = "uploads/" + fileName;

    // Открываем файл для чтения
    std::ifstream inFile(filePath, std::ios::binary);
    if (!inFile.is_open()) {
        std::cerr << "Файл не найден: " << filePath << "\n";
        sendString(clientSocket, "ERROR");
        sendString(clientSocket, "Файл не найден на сервере.");
        return;
    }

    // Получаем размер файла
    inFile.seekg(0, std::ios::end);
    int64_t fileSize = inFile.tellg();
    inFile.seekg(0, std::ios::beg);

    if (fileSize < 0) {
        std::cerr << "Ошибка определения размера файла.\n";
        inFile.close();
        sendString(clientSocket, "ERROR");
        sendString(clientSocket, "Ошибка чтения файла на сервере.");
        return;
    }

    std::cout << "Отправка файла \"" << fileName << "\" (" << fileSize << " байт)...\n";

    // Отправляем статус OK и размер файла
    if (!sendString(clientSocket, "OK")) {
        std::cerr << "Ошибка отправки статуса.\n";
        inFile.close();
        return;
    }

    if (!sendInt64(clientSocket, fileSize)) {
        std::cerr << "Ошибка отправки размера файла.\n";
        inFile.close();
        return;
    }

    // Отправляем данные файла
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

        if (!sendAll(clientSocket, buffer, static_cast<int>(bytesRead))) {
            std::cerr << "Ошибка отправки данных файла.\n";
            inFile.close();
            return;
        }

        totalSent += bytesRead;
    }

    inFile.close();
    std::cout << "Файл успешно отправлен клиенту (" << totalSent << " байт).\n";
}

void handleClient(SOCKET clientSocket) {
    char clientIP[INET_ADDRSTRLEN] = "unknown";
    
    while (true) {
        // Получаем команду от клиента
        std::string command;
        if (!recvString(clientSocket, command)) {
            std::cout << "Клиент отключился (соединение разорвано).\n";
            break;
        }

        std::cout << "Получена команда: " << command << "\n";

        if (command == "UPLOAD") {
            handleUpload(clientSocket);
        }
        else if (command == "DOWNLOAD") {
            handleDownload(clientSocket);
        }
        else if (command == "EXIT") {
            std::cout << "Клиент запросил завершение соединения.\n";
            break;
        }
        else {
            std::cout << "Неизвестная команда: " << command << "\n";
            if (!sendString(clientSocket, "ERROR")) {
                std::cout << "Клиент отключился (не удалось отправить ответ).\n";
                break;
            }
            if (!sendString(clientSocket, "Неизвестная команда: " + command)) {
                std::cout << "Клиент отключился (не удалось отправить сообщение об ошибке).\n";
                break;
            }
        }
    }
    
    // Корректное закрытие соединения
    shutdown(clientSocket, SD_BOTH);
    closesocket(clientSocket);
}

int main() {
    WSADATA wsaData;
    SOCKET serverSocket, clientSocket;
    sockaddr_in serverAddr{}, clientAddr{};
    int clientAddrSize = sizeof(clientAddr);

    setlocale(LC_ALL, "Russian");

    // Инициализация Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Ошибка инициализации Winsock.\n";
        system("pause");
        return 1;
    }

    // Создаем сокет
    serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "Ошибка создания сокета: " << WSAGetLastError() << "\n";
        WSACleanup();
        system("pause");
        return 1;
    }

    // Настраиваем адрес сервера
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    // Привязываем сокет
    if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Ошибка привязки сокета: " << WSAGetLastError() << "\n";
        closesocket(serverSocket);
        WSACleanup();
        system("pause");
        return 1;
    }

    // Запускаем сервер на прослушивание
    if (listen(serverSocket, 5) == SOCKET_ERROR) {
        std::cerr << "Ошибка при прослушивании порта: " << WSAGetLastError() << "\n";
        closesocket(serverSocket);
        WSACleanup();
        system("pause");
        return 1;
    }
    
    std::cout << "========================================\n";
    std::cout << "Сервер запущен на порту " << PORT << "\n";
    std::cout << "Ожидание подключения клиентов...\n";
    std::cout << "========================================\n";

    // Обрабатываем клиентов в цикле
    while (true) {
        clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrSize);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "Ошибка при подключении клиента: " << WSAGetLastError() << "\n";
            continue;
        }
        
        char clientIP[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);
        std::cout << "\n>>> Клиент подключен: " << clientIP << ":" << ntohs(clientAddr.sin_port) << "\n";

        handleClient(clientSocket);
        
        std::cout << ">>> Клиент отключен: " << clientIP << ":" << ntohs(clientAddr.sin_port) << "\n\n";
    }

    // Закрываем сокет и очищаем Winsock
    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
