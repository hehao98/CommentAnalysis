
/**
 * Take a piece of java code as input, parse it into Abstract Syntax Tree
 * Generate function and comment pairs
 * 
 * @author He, Hao
 */

import java.io.File;
import java.util.ArrayList;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.GenericVisitorAdapter;
import com.github.javaparser.ast.visitor.Visitable;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class JavaCode {
    public class MethodInfo {
        String name;
        String code;
        String comment;
        int lineCount;

        public MethodInfo() {

        }

        public MethodInfo(String name, String code, int lineCount, String comment) {
            this.name = name;
            this.code = code;
            this.lineCount = lineCount;
            this.comment = comment;
        }
    }

    public File file;

    public String code;

    public JavaParser parser;

    public CompilationUnit cu;

    public ArrayList<MethodInfo> methodInfo;

    public JavaCode(String code, File file) {
        this.code = code;
        this.file = file;

        // Start Parsing Code
        this.parser = new JavaParser();
        ParseResult<CompilationUnit> result = this.parser.parse(code);
        if (result.isSuccessful()) {
            this.cu = result.getResult().get();
        } else {
            System.out.println("Something goes wrong while parsing code from");
            System.out.println(result.getProblems().toString());
        }

        // Initialize statistics
        this.getStatistics();
    }

    public void getStatistics() {
        // Extract all method declarations and count its statistics here.
        this.methodInfo = new ArrayList<MethodInfo>();
        this.cu.accept(new VoidVisitorAdapter<ArrayList<MethodInfo>>() {
            @Override
            public void visit(MethodDeclaration n, ArrayList<MethodInfo> arg) {
                super.visit(n, arg);

                MethodInfo method = new MethodInfo();

                method.code = n.toString();
                method.name = n.getNameAsString();
                if (n.getRange().isPresent()) {
                    method.lineCount = n.getRange().get().getLineCount();
                } else {
                    method.lineCount = 0;
                }
                if (n.getComment().isPresent()) {
                    method.comment = n.getComment().get().toString();
                } else {
                    method.comment = "";
                }

                arg.add(method);
                return;
            }
        }, this.methodInfo);
    }

    public String toJson() {

        Gson gson = new GsonBuilder().setPrettyPrinting().create();

        String methodInfoJson = gson.toJson(methodInfo);
        return methodInfoJson;
    }
}