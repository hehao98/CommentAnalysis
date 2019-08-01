/**
 * This is a file header comment
 */

import java.util.*;

public class sample {
    /** This is a variable */
    int member;

    public static int func_no_doc() {
        // Here is a normal comment
        int x;
        /* This is another normal comment */
        int y;
        return 0; // This is another nomal comment
    }

    /**
     * This is the main function
     */
    public static void main(String[] args) {
        /*
         * int a = b + c; // There is another nasty comment
         */
        System.out.printf("This is a nasty comment /*");
        return;
    }
}

interface Inter {
    /**Documentation */
    public void f();
}
