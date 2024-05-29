package com.oocourse.library1;

import java.time.format.DateTimeFormatter;

public class LibrarySystem {
    public static final LibrarySystem INSTANCE;
    public static final LibraryScanner SCANNER;
    public static final LibraryPrinter PRINTER;

    public static final DateTimeFormatter DTF = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    private final LibraryScanner scanner;
    private final LibraryPrinter printer;

    static {
        LibraryForTest libraryForTest = new LibraryForTest();
        INSTANCE = new LibrarySystem(new LibraryForTest.Scanner(), new LibraryForTest.Printer());
        SCANNER = INSTANCE.scanner;
        PRINTER = INSTANCE.printer;
    }


    private LibrarySystem(LibraryScanner scanner, LibraryPrinter printer) {
        this.scanner = scanner;
        this.printer = printer;
    }

    /**
     *  统计 Borrow 和 Pick 请求的完成情况，输出到控制台，可以在所有请求完成后调用查看结果，一个例子如下：
     *  <blockquote><pre>
     *  while (input != null) {
     *      library.run(input);
     *      input = sc.nextCommand();
     *  }
     *  // finish all requests, then show the result
     *  LibrarySystem.show();
     */
    public static void show() {
        LibraryForTest.show();
    }
}
