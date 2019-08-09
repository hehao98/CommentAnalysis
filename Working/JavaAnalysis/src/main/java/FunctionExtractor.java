
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
import java.util.NoSuchElementException;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;



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

    private static JavaCode parseJavaFile(final File file) {
        try (Scanner sc = new Scanner(file);) {
            String code = sc.useDelimiter("\\Z").next();
            return new JavaCode(code, file);
        } catch (FileNotFoundException e) {
            System.out.println(e.toString());
            return null;
        } catch (NoSuchElementException e) {
            System.out.println(e.toString());
            return null;
        }
    }

    private static String buildJson(ArrayList<JavaCode> codeList) {
        JSONObject json = new JSONObject();
        for (JavaCode code : codeList) {
            JSONObject thisObject = new JSONObject();
            JSONArray methodArray = new JSONArray();
            for (JavaCode.MethodInfo method : code.methodInfo) {
                JSONObject methodObject = new JSONObject();
                methodObject.put("name", method.name);
                methodObject.put("code", method.code);
                methodObject.put("comment", method.comment);
                methodObject.put("lineCount", method.lineCount);
                methodObject.put("maxIndentation", method.maxIndentation);
                methodObject.put("commentsInMethod", method.commentsInMethod);
                methodObject.put("visibility", method.visibility);
                methodObject.put("isAbstract", method.isAbstract);
                methodObject.put("isStatic", method.isStatic);
                methodObject.put("isNative", method.isNative);
                methodObject.put("isSynchronized", method.isSynchronized);
                methodArray.add(methodObject);
            }
            thisObject.put("methodInfo", methodArray);
            json.put(code.file.getPath(), thisObject);
        }
        return json.toJSONString();
    }

    public static void main(String[] args) {
        final File projectFolder = new File(args[0]);
        final File outputFile = new File(args[1]);
        ArrayList<File> srcFiles = getSourceCodeFilePath(projectFolder);
        ArrayList<JavaCode> codeList = new ArrayList<JavaCode>();

        int successfullyParsed = 0;
        for (File src : srcFiles) {
            //System.out.println(src.getAbsolutePath());
            JavaCode code = parseJavaFile(src);
            if (code != null && code.isOk) {
                codeList.add(code);
                successfullyParsed++;
            }
        }
        System.out.printf("Read %d Java files in which %d files are successfully parsed\n", 
            srcFiles.size(), successfullyParsed);

        try (PrintWriter out = new PrintWriter(outputFile)) {
            out.println(buildJson(codeList));
            out.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.toString());
        }
    }
}