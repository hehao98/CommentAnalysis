
/**
 * Given a Java project path, extract all functions and its corresponding
 * comments from its java source files.
 * 
 * @author He, Hao
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.ArrayList;

public class FunctionExtractor {
    private static ArrayList<File> getSourceCodeFilePath(final File folder) {
        ArrayList<File> list = new ArrayList<File>();
        for (final File fileEntry : folder.listFiles()) {
            if (fileEntry.isDirectory()) {
                list.addAll(getSourceCodeFilePath(fileEntry));
            } else {
                if (fileEntry.getName().endsWith(".java"))
                    list.add(fileEntry);
            }
        }
        return list;
    }

    private static JavaCode parseJavaFile(File file) {
        try (Scanner sc = new Scanner(file);) {
            String code = sc.useDelimiter("\\Z").next();
            return new JavaCode(code, file);
        } catch (FileNotFoundException e) {
            System.out.println(e.toString());
            return null;
        }
    }

    public static void main(String[] args) {
        final File projectFolder = new File(args[0]);
        ArrayList<File> srcFiles = getSourceCodeFilePath(projectFolder);
        JavaCode code;

        System.out.println(srcFiles.get(0).getName());
        code = parseJavaFile(srcFiles.get(0));

        try (PrintWriter out = new PrintWriter("output/test.json")) {
            out.println(code.toJson());
            out.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.toString());
        }
    }
}