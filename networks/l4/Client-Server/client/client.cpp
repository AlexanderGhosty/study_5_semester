#include <iostream>
#include <fstream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 1024

void uploadFile(SOCKET serverSocket) {
    std::cout << "Введите имя файла для отправки: ";
    std::string fileName;
    std::cin >> fileName;

    std::ifstream inFile(fileName, std::ios::binary);
    if (!inFile) {
        std::cerr << "Ошибка: не удалось открыть файл.\n";
        return;
    }

    // Отправляем команду "upload" серверу
    std::string command = "upload\n";
    send(serverSocket, command.c_str(), command.size(), 0);

    // Отправляем содержимое файла
    char buffer[BUFFER_SIZE];
    while (inFile.read(buffer, BUFFER_SIZE)) {
        send(serverSocket, buffer, inFile.gcount(), 0);
    }
    send(serverSocket, buffer, inFile.gcount(), 0); // Отправляем остаток
    inFile.close();

    std::cout << "Файл отправлен серверу.\n";

    // Получаем подтверждение от сервера
    memset(buffer, 0, BUFFER_SIZE);
    int bytesReceived = recv(serverSocket, buffer, BUFFER_SIZE - 1, 0);
    if (bytesReceived > 0) {
        std::cout << "Ответ сервера: " << buffer << "\n";
    }
}

void downloadFile(SOCKET serverSocket) {
    // Отправляем команду "download" серверу
    std::string command = "download\n";
    send(serverSocket, command.c_str(), command.size(), 0);

    // Получаем файл от сервера
    std::ofstream outFile("downloaded_file", std::ios::binary);
    if (!outFile) {
        std::cerr << "Ошибка: не удалось открыть файл для записи.\n";
        return;
    }

    char buffer[BUFFER_SIZE];
    int bytesReceived;
    bytesReceived = recv(serverSocket, buffer, BUFFER_SIZE - 1, 0);
    if (bytesReceived > 0) {
        outFile.write(buffer, bytesReceived);
    }
    outFile.close();

    std::cout << "Файл успешно загружен с сервера (сохранен как 'downloaded_file').\n";
}

void interactWithServer(SOCKET serverSocket) {
    while (true) {
        std::cout << "\nВыберите действие:\n"
            << "1. Отправить файл на сервер (upload)\n"
            << "2. Скачать файл с сервера (download)\n"
            << "3. Выйти\n"
            << "Введите номер команды: ";
        int choice;
        std::cin >> choice;

        switch (choice) {
        case 1:
            uploadFile(serverSocket);
            break;
        case 2:
            downloadFile(serverSocket);
            break;
        case 3:
            std::cout << "Завершение работы клиента.\n";
            send(serverSocket, "exit\n", 5, 0);
            system("pause");
            return;
        default:
            std::cout << "Некорректный выбор. Попробуйте снова.\n";
            break;
        }
    }
}

int main() {
    WSADATA wsaData;
    SOCKET clientSocket;
    sockaddr_in serverAddr{};

    setlocale(LC_ALL, "Russian");

    // Инициализация Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Ошибка инициализации Winsock.\n";
        return 1;
    }

    // Создаем сокет TCP дуплексный
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

    std::cout << "Введите IP-адрес сервера: ";
    std::string serverIP;
    std::cin >> serverIP;

    if (inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr) <= 0) {
        std::cerr << "Некорректный IP-адрес.\n";
        closesocket(clientSocket);
        WSACleanup();
        system("pause");
        return 1;
    }

    // Подключаемся к серверу
    if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Ошибка подключения к серверу: " << WSAGetLastError() << "\n";
        closesocket(clientSocket);
        WSACleanup();
        system("pause");
        return 1;
    }

    std::cout << "Подключение к серверу успешно.\n";
    interactWithServer(clientSocket);

    // Закрываем сокет и очищаем Winsock
    closesocket(clientSocket);
    WSACleanup();
    return 0;
}
