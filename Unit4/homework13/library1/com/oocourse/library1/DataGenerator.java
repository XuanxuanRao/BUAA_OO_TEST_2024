package com.oocourse.library1;

import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class DataGenerator {
    private final ArrayList<LibraryBookId> bookIdPool;
    private final HashMap<LibraryBookId, Integer> bookShelf;
    private final HashMap<LibraryBookId, Integer> appointmentOffice;
    private final HashMap<LibraryBookId, Integer> borrowReturnOffice;
    private final HashMap<String, User> users;
    private final Statistic statistic;
    private static final Random random = new Random();
    private LocalDate currentDate;
    private boolean shouldOpen = true;
    private int bookSum = 0;

    private class User {
        public final String studentId;
        public final HashSet<LibraryBookId> borrowedBooks;
        public final HashMap<LibraryBookId, Integer> orderedBooks;
        public User(String studentId) {
            this.studentId = studentId;
            borrowedBooks = new HashSet<>();
            orderedBooks = new HashMap<>();
        }

        public void borrowBook(LibraryBookId bookId) {
            assert !bookId.isTypeA();
            assert !bookShelf.containsKey(bookId);
            assert bookShelf.containsKey(bookId) && bookShelf.get(bookId) > 0;
            bookShelf.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
            borrowedBooks.add(bookId);
        }

        public void pickBook(LibraryBookId bookId) {
            assert !bookId.isTypeA();
            assert orderedBooks.containsKey(bookId);
            assert appointmentOffice.containsKey(bookId) && appointmentOffice.get(bookId) > 0;
            assert !borrowedBooks.contains(bookId);
            appointmentOffice.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
            orderedBooks.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
            borrowedBooks.add(bookId);
        }

        public void orderBook(LibraryBookId bookId) {
            assert !bookId.isTypeA();
            assert !bookShelf.containsKey(bookId);
            orderedBooks.put(bookId, orderedBooks.getOrDefault(bookId, 0) + 1);
        }

        public void returnBook(LibraryBookId bookId) {
            assert !bookId.isTypeA();
            assert borrowedBooks.contains(bookId);
            borrowedBooks.remove(bookId);
            borrowReturnOffice.put(bookId, borrowReturnOffice.getOrDefault(bookId, 0) + 1);
        }

        public LibraryBookId getOrderedBook() {
            return getRandomKeyFromMap(orderedBooks);
        }

        public LibraryBookId getBorrowedBook() {
            return getRandomFromSet(borrowedBooks);
        }

        public boolean hasBorrowBookTypeB() {
            return borrowedBooks.stream().anyMatch(LibraryBookId::isTypeB);
        }

        @Override
        public String toString() {
            return "[" + studentId + " borrow: " + borrowedBooks + "]";
        }
    }

    public DataGenerator() {
        bookIdPool = new ArrayList<>();
        statistic = new Statistic();
        bookShelf = new HashMap<>();
        appointmentOffice = new HashMap<>();
        borrowReturnOffice = new HashMap<>();
        users = new HashMap<>();
        users.put("22373053", new User("22373053"));
        users.put("22371562", new User("22371562"));
        int n = random.nextInt(10) + 5;
        for (int i = 0; i < n; i++) {
            LibraryBookId bookId;
            do {
                LibraryBookId.Type type = LibraryBookId.Type.values()[random.nextInt(3)];
                if (type == LibraryBookId.Type.A) {
                    type = LibraryBookId.Type.values()[random.nextInt(3)];
                }
                String uid = String.valueOf(random.nextInt(9000) + 1000);
                bookId = new LibraryBookId(type, uid);
            } while (bookShelf.containsKey(bookId));
            int copyNumber = random.nextInt(10) + 1;
            bookSum += copyNumber;
            bookShelf.put(bookId, copyNumber);
            bookIdPool.add(bookId);
        }
        currentDate = LocalDate.now().plusDays(random.nextInt(10) - 100);
    }

    public String libraryInformation() {
        return "\t\t\tLibrary information: \n" +
                "BookShelf: " + bookShelf + "\n" +
                "AppointmentOffice: " + appointmentOffice + "\n" +
                "BorrowReturnOffice: " + borrowReturnOffice + "\n" +
                "Users: " + users.values() + "\n";
    }

    /**
     * 获取库存信息，应该在对象创建后立刻调用
     *
     * @return Library information for each book
     */
    public Map<LibraryBookId, Integer> getInventory() {
        return new HashMap<>(bookShelf);
    }

    /**
     * 生成一条 LibraryCommand 信息
     *
     * @return 生成的 LibraryCommand 信息
     */
    public LibraryCommand<?> generateCommand() {
        if (shouldOpen) {
            shouldOpen = false;
            currentDate = currentDate.plusDays(random.nextInt(10) + 1);
            if (!currentDate.isBefore(LocalDate.ofYearDay(2025, 1))) {
                return null;
            }
            return new LibraryCommand<>(currentDate, "OPEN");
        } else if (random.nextInt(10) == 9) {
            shouldOpen = true;
            return new LibraryCommand<>(currentDate, "CLOSE");
        } else {
            LibraryRequest libraryRequest = generateRequest();
            while (libraryRequest == null) {
                libraryRequest = generateRequest();
            }
            return new LibraryCommand<>(currentDate, libraryRequest);
        }
    }

    /**
     * 获取请求信息的处理结果，并据此更新数据
     *
     * @param date    请求信息的日期
     * @param request 输入的请求信息
     * @param result  图书馆处理结果
     */
    public void getOutput(LocalDate date, LibraryRequest request, boolean result) {
        User user = users.get(request.getStudentId());
        LibraryBookId bookId = request.getBookId();
        statistic.receiveInformation(request.getType(), result);
        switch (request.getType()) {
            case PICKED:
                if (result) { user.pickBook(bookId); }
                break;
            case BORROWED:
                if (result) { user.borrowBook(bookId); }
                else if (bookShelf.containsKey(bookId) && !bookId.isTypeA()) {
                    if (bookId.isTypeC() && !user.borrowedBooks.contains(bookId)) {
                        throw new RuntimeException("Can borrow this book but rejected");
                    } else if (bookId.isTypeB() && !user.hasBorrowBookTypeB()) {
                        throw new RuntimeException("Can borrow this book but rejected");
                    }
                    bookShelf.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
                    borrowReturnOffice.put(bookId, borrowReturnOffice.getOrDefault(bookId, 0) + 1);
                }
                break;
            case ORDERED:
                if (result) { user.orderBook(bookId); }
                else if (bookId.isTypeC() && !user.borrowedBooks.contains(bookId) && bookShelf.containsKey(bookId)) {
                    throw new RuntimeException("Can order this book but rejected");
                } else if (bookId.isTypeB() && !user.hasBorrowBookTypeB() && bookShelf.containsKey(bookId)) {
                    throw new RuntimeException("Can order this book but rejected");
                }
                break;
            case RETURNED:
                if (result) { user.returnBook(bookId); }
                break;
            default:
                throw new RuntimeException("Invalid request type");
        }
    }

    public void getOutput(LocalDate date, LibraryBookId bookId, int result) {
        assert result == bookShelf.getOrDefault(bookId, 0);
    }

    /**
     * 获取移动信息的处理结果，并据此更新数据
     *
     * @param date  请求信息的日期
     * @param moves 输出的移动信息
     */
    public void getOutput(LocalDate date, List<LibraryMoveInfo> moves) {
        for (LibraryMoveInfo move : moves) {
            if (!checkMove(date, move)) {
                throw new RuntimeException("Invalid move: " + move + ". The moved book does not exist.");
            } else if (!checkBookSum()) {
                throw new RuntimeException("Invalid move: " + move + ". Some books are missing or extra.");
            }
        }
    }

    public void showStatistic() {
        statistic.showResult();
    }

    private boolean checkMove(LocalDate date, LibraryMoveInfo move) {
        String from = move.getFrom();
        String to = move.getTo();
        LibraryBookId bookId = move.getBookId();
        String studentId = move.getReserveFor();
        switch (from) {
            case "bs":
                if (!bookShelf.containsKey(bookId)) return false;
                bookShelf.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
                break;
            case "ao":
                if (!appointmentOffice.containsKey(bookId)) return false;
                appointmentOffice.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
                break;
            case "bro":
                if (!borrowReturnOffice.containsKey(bookId)) return false;
                borrowReturnOffice.computeIfPresent(bookId, (id, count) -> count == 1 ? null : count - 1);
                break;
            default:
                throw new RuntimeException("Invalid move from");
        }
        switch (to) {
            case "bs":
                bookShelf.put(bookId, bookShelf.getOrDefault(bookId, 0) + 1);
                break;
            case "ao":
                if (!users.get(studentId).orderedBooks.containsKey(bookId)) return false;
                appointmentOffice.put(bookId, appointmentOffice.getOrDefault(bookId, 0) + 1);
                break;
            case "bro":
                borrowReturnOffice.put(bookId, borrowReturnOffice.getOrDefault(bookId, 0) + 1);
                break;
            default:
                throw new RuntimeException("Invalid move to");
        }
        return true;
    }

    private User getUser(boolean isNewUser) {
        User user;
        if (!isNewUser) {
            user = getRandomValueFromMap(users);
            if (user != null)   return user;
        }
        user = new User(String.valueOf(random.nextInt(90000000) + 10000000));
        users.put(user.studentId, user);
        return user;
    }

    private User getUserForPick() {
        User user;
        int chance = 15;
        do {
            user = getUser(false);
            chance--;
        } while (chance > 0 && user.orderedBooks.isEmpty());
        return user;
    }

    private User getUserForReturn() {
        User user;
        int chance = 15;
        do {
            user = getUser(false);
            chance--;
        } while (chance > 0 && user.borrowedBooks.isEmpty());
        return user;
    }

    private LibraryRequest generateRequest() {
        User user;
        LibraryBookId bookId;
        LibraryRequest.Type type = LibraryRequest.Type.values()[random.nextInt(LibraryRequest.Type.values().length)];
        if (type.equals(LibraryRequest.Type.QUERIED)) {
            type = LibraryRequest.Type.values()[random.nextInt(LibraryRequest.Type.values().length)];
        }
        switch (type) {
            case PICKED:
                user = getUserForPick();
                bookId = user.getOrderedBook();
                if (bookId == null) {
                    return null;
                }
                break;
            case BORROWED:
            case ORDERED:
                user = getUser(users.size() <= 10 ? random.nextBoolean() : random.nextInt(10) == 9);
                bookId = bookIdPool.get(random.nextInt(bookIdPool.size()));
                break;
            case RETURNED:
                user = getUserForReturn();
                bookId = user.getBorrowedBook();
                if (bookId == null) {
                    return null;
                }
                break;
            case QUERIED:
                user = getUser(false);
                bookId = bookIdPool.get(random.nextInt(bookIdPool.size()));
                break;
            default:
                throw new RuntimeException("Invalid request type");
        }
        return new LibraryRequest(type, user.studentId, bookId);
    }

    private static <K, V> V getRandomValueFromMap(HashMap<K, V> map) {
        if (map.isEmpty()) {
            return null;
        }

        // Convert the values to a list
        List<V> valuesList = new ArrayList<>(map.values());

        // Generate a random index
        int randomIndex = random.nextInt(valuesList.size());

        // Get the value at the random index
        return valuesList.get(randomIndex);
    }

    private static <K, V> K getRandomKeyFromMap(HashMap<K, V> map) {
        if (map.isEmpty()) {
            return null;
        }

        // Convert the keys to a list
        List<K> keysList = new ArrayList<>(map.keySet());

        // Generate a random index
        int randomIndex = random.nextInt(keysList.size());

        // Get the key at the random index
        return keysList.get(randomIndex);
    }

    private static <V> V getRandomFromSet(HashSet<V> set) {
        if (set.isEmpty()) {
            return null;
        }

        // Convert the set to a list
        List<V> list = new ArrayList<>(set);

        // Generate a random index
        int randomIndex = random.nextInt(list.size());

        // Get the value at the random index
        return list.get(randomIndex);
    }

    private boolean checkBookSum() {
        AtomicInteger sum = new AtomicInteger();
        for (int value : bookShelf.values()) {
            sum.addAndGet(value);
        }
        for (int value : appointmentOffice.values()) {
            sum.addAndGet(value);
        }
        for (int value : borrowReturnOffice.values()) {
            sum.addAndGet(value);
        }
        users.values().forEach(
                user -> sum.addAndGet(user.borrowedBooks.size())
        );
        return sum.get() == bookSum;
    }

}
