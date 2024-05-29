package com.oocourse.library1;

public class Statistic {
    private int borrowCount = 0;
    private int successBorrowCount = 0;
    private int pickCount = 0;
    private int successPickCount = 0;

    public void receiveInformation(LibraryRequest.Type type, boolean result) {
        if (type == LibraryRequest.Type.BORROWED) {
            borrowCount++;
            if (result) {
                successBorrowCount++;
            }
        } else if (type == LibraryRequest.Type.PICKED) {
            pickCount++;
            if (result) {
                successPickCount++;
            }
        }
    }

    public void showResult() {
        System.out.println("Request Completion Status Information");
        System.out.println("Total Borrow Request Count: " + borrowCount + ", Success Count: " + successBorrowCount);
        System.out.println("Total Pick Request Count: " + pickCount + ", Success Count: " + successPickCount);
    }
}
