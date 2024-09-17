@echo off
:: Устанавливаем кодировку UTF-8
chcp 65001 >nul

:: Активируем виртуальное окружение
call myenv\Scripts\activate

:: Спрашиваем, что пользователь хочет конвертировать
echo.
echo Выберите, что вы хотите конвертировать:
echo 1. Аниме
echo 2. Манга
echo 3. Аниме и Манга
echo 4. Стоп
set /p choice="Введите ваш выбор (1-4): "

if "%choice%"=="1" (
    echo Запуск конвертации аниме...
    python src\anime_import.py
) else if "%choice%"=="2" (
    echo Запуск конвертации манги...
    python src\manga_import.py
) else if "%choice%"=="3" (
    echo Запуск конвертации аниме и манги...
    python src\anime_import.py
    python src\manga_import.py
) else if "%choice%"=="4" (
    echo Остановка работы.
    echo Нажмите любую клавишу для выхода...
    pause >nul
    exit
) else (
    echo Неверный выбор. Попробуйте снова.
    echo Нажмите любую клавишу для выхода...
    pause >nul
    exit
)

:: Завершаем работу скрипта
echo Завершено. Нажмите любую клавишу для выхода...
pause >nul
