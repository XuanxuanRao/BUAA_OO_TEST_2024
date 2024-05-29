package com.oocourse.library1;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LibraryForTest {
    private static final DataGenerator dg = new DataGenerator();
    private static final String LOG_FILE_PATH = "library_log.txt";
    private static final String INPUT_FILE_PATH = "library_input.txt";
    private static PrintWriter writer;
    private static PrintWriter input;

    public LibraryForTest() {
        File logFile = new File(LOG_FILE_PATH);
        if (logFile.exists()) {
            try {
                PrintWriter clearWriter = new PrintWriter(new FileWriter(LOG_FILE_PATH, false));
                clearWriter.close();
            } catch (IOException ignored) {
            }
        }

        try {
            // 创建新的 PrintWriter 对象以写入日志文件
            writer = new PrintWriter(new FileWriter(LOG_FILE_PATH, true));
        } catch (IOException ignored) {
        }

        File inputFile = new File(INPUT_FILE_PATH);
        if (inputFile.exists()) {
            try {
                PrintWriter clearInput = new PrintWriter(new FileWriter(INPUT_FILE_PATH, false));
                clearInput.close();
            } catch (IOException ignored) {
            }
        }

        try {
            // 创建新的 PrintWriter 对象以写入输入文件
            input = new PrintWriter(new FileWriter(INPUT_FILE_PATH, true));
        } catch (IOException ignored) {
        }
    }

    private static void logToFile(String message) {
        if (writer != null) {
            writer.println(message);
            writer.flush();
        }
    }

    private static void inputToFile(String message) {
        if (input != null) {
            input.println(message);
            input.flush();
        }
    }

    @Override
    protected void finalize() throws Throwable {
        if (writer != null) {
            writer.close();
        }
        super.finalize();
    }


    static class Scanner implements LibraryScanner {
        @Override
        public Map<LibraryBookId, Integer> getInventory() {
            Map<LibraryBookId, Integer> inventory = dg.getInventory();
            inputToFile(String.valueOf(inventory.size()));
            for (Map.Entry<LibraryBookId, Integer> entry : inventory.entrySet()) {
                inputToFile(entry.getKey() + " " + entry.getValue());
            }
            return inventory;
        }

        @Override
        public LibraryCommand<?> nextCommand() {
            LibraryCommand<?> command = dg.generateCommand();
            if (command != null) {
                logToFile(command.toString());
                inputToFile(command.toString());
            }
            return command;
        }
    }

    static class Printer implements LibraryPrinter {
        @Override
        public void reject(LocalDate date, LibraryRequest request) {
            dg.getOutput(date, request, false);
            logToFile("[" + LibrarySystem.DTF.format(date) + "] [reject] " + request + "\n");
        }

        @Override
        public void accept(LocalDate date, LibraryRequest request) {
            dg.getOutput(date, request, true);
            logToFile("[" + LibrarySystem.DTF.format(date) + "] [accept] " + request);
            logToFile(dg.libraryInformation() + "\n");
        }

        @Override
        public void info(LocalDate date, LibraryBookId bookId, int count) {
            dg.getOutput(date, bookId, count);
            logToFile("[" + LibrarySystem.DTF.format(date) + "] " + bookId + " " + count + "\n");
        }

        @Override
        public void move(LocalDate date, List<LibraryMoveInfo> info) {
            dg.getOutput(date, info);
            logToFile(String.valueOf(info.size()));
            for (LibraryMoveInfo item : info) {
                logToFile("[" + LibrarySystem.DTF.format(date) + "] " + item);
            }
            logToFile(dg.libraryInformation() + "\n");
        }
    }

    public static void show() {
        dg.showStatistic();
    }
}
