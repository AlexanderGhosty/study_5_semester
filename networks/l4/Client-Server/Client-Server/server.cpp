#include <iostream>
#include <fstream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 1024

void handleClient(SOCKET clientSocket) {
    char buffer[BUFFER_SIZE];

    while (true) {
        memset(buffer, 0, BUFFER_SIZE);

        // Получаем команду от клиента
        int bytesReceived = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
        if (bytesReceived <= 0) {
            std::cout << "Клиент отключился.\n";
            break;
        }

        std::string command(buffer);
        command = command.substr(0, command.find('\n'));

        if (command == "upload") {
            std::string folderPath = "uploads/"; // Папка для сохранения файлов

            // Преобразование в LPCWSTR
            std::wstring wideFolderPath(folderPath.begin(), folderPath.end());
            if (!CreateDirectory(wideFolderPath.c_str(), nullptr)) {
                if (GetLastError() != ERROR_ALREADY_EXISTS) {
                    std::cerr << "Ошибка при создании папки: " << GetLastError() << "\n";
                    continue;
                }
            }

            std::string fileName = "uploaded_file"; // Имя файла
            std::string filePath = folderPath + fileName;

            std::ofstream outFile(filePath, std::ios::binary);
            if (!outFile) {
                std::cerr << "Ошибка при открытии файла для записи.\n";
                continue;
            }

            memset(buffer, 0, BUFFER_SIZE);
            bytesReceived = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
            if (bytesReceived > 0) {
                outFile.write(buffer, bytesReceived);
            }
            outFile.close();

            std::cout << "Файл успешно загружен от клиента: " << filePath << "\n";
            send(clientSocket, "Файл загружен.\n", 15, 0);
        }
        else if (command == "download") {
            std::string folderPath = "uploads/"; // Путь к папке
            std::string fileName = "uploaded_file"; // Имя файла
            std::string filePath = folderPath + fileName; // Полный путь к файлу

            std::ifstream inFile(filePath, std::ios::binary); // Открываем файл из папки
            if (!inFile) {
                std::cerr << "Файл для отправки не найден: " << filePath << "\n";
                send(clientSocket, "Файл не найден.\n", 16, 0);
                continue;
            }

            while (inFile.read(buffer, BUFFER_SIZE)) {
                send(clientSocket, buffer, inFile.gcount(), 0); // Отправляем данные блоками
            }

             //Отправляем оставшиеся данные, если они есть
            send(clientSocket, buffer, inFile.gcount(), 0); // Отправляем остаток
            inFile.close();

            std::cout << "Файл успешно отправлен клиенту: " << filePath << "\n";
        }
        else if (command == "exit") {
            std::cout << "Клиент завершил соединение.\n";
            break;
        }
        else {
            std::string errorMsg = "Неизвестная команда: " + command + "\n";
            send(clientSocket, errorMsg.c_str(), errorMsg.size(), 0);
        }
    }
    closesocket(clientSocket);
}

int main() {
    WSADATA wsaData;
    SOCKET serverSocket, clientSocket;
    sockaddr_in serverAddr{}, clientAddr{};
    int clientAddrSize = sizeof(clientAddr);

    setlocale(LC_ALL, "Russian");

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Ошибка инициализации Winsock.\n";
        return 1;
    }

    // Создаем сокет
    serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serverSocket == INVALID_SOCKET) {
        std::cerr << "Ошибка создания сокета: " << WSAGetLastError() << "\n";
        WSACleanup();
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
        return 1;
    }

    // Запускаем сервер на прослушивание
    if (listen(serverSocket, 5) == SOCKET_ERROR) {
        std::cerr << "Ошибка при прослушивании порта: " << WSAGetLastError() << "\n";
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }
    std::cout << "Сервер запущен на порту " << PORT << ". Ожидание подключения...\n";

    // Обрабатываем клиентов в цикле
    while (true) {
        clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrSize);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "Ошибка при подключении клиента: " << WSAGetLastError() << "\n";
            continue;
        }
        std::cout << "Клиент подключен.\n";

        handleClient(clientSocket);
    }

    // Закрываем сокет и очищаем Winsock
    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
