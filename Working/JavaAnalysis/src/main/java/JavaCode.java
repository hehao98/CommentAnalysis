
/**
 * Take a piece of java code as input, parse it into Abstract Syntax Tree
 * Generate function and comment pairs
 * 
 * @author He, Hao
 */

import java.io.File;
import java.util.ArrayList;
import java.util.LinkedList;

import com.alibaba.fastjson.annotation.JSONField;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.visitor.GenericVisitorAdapter;
import com.github.javaparser.ast.visitor.Visitable;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import com.github.javaparser.printer.PrettyPrinterConfiguration;

public class JavaCode {
    public class MethodInfo {
        @JSONField(name = "name")
        String name;
        @JSONField(name = "code")
        String code;
        @JSONField(name = "comment")
        String comment;
        @JSONField(name = "lineCount")
        int lineCount;
        @JSONField(name = "maxIndentation")
        int maxIndentation;
        @JSONField(name = "commentsInMethod")
        String[] commentsInMethod;

        public MethodInfo() {

        }

        public MethodInfo(String name, String code, int lineCount, String comment) {
            this.name = name;
            this.code = code;
            this.lineCount = lineCount;
            this.comment = comment;
        }
    }

    public boolean isOk;

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
            this.isOk = true;
        } else {
            this.isOk = false;
            System.out.println("Something goes wrong while parsing code from " + file.getPath());
            System.out.println(result.getProblems().toString());
            return;
        }

        // Initialize statistics
        this.getStatistics();
    }

    /**
     * Given a piece of Java code, find its maximum indentation depth Assume 4-space
     * indentation
     * 
     * @return the maximum indentation depth of this code
     */
    public int maxIndentation(String code) {
        int depth = 0;
        for (String line : code.split("\n")) {
            int i = 0;
            while (i < line.length() && line.charAt(i) == ' ')
                i++;
            if (i / 4 > depth)
                depth = i / 4;
        }
        return depth;
    }

    public void getStatistics() {
        // Extract all method declarations and count its statistics here.
        this.methodInfo = new ArrayList<MethodInfo>();
        this.cu.accept(new VoidVisitorAdapter<ArrayList<MethodInfo>>() {
            @Override
            public void visit(MethodDeclaration n, ArrayList<MethodInfo> arg) {
                super.visit(n, arg);

                MethodInfo method = new MethodInfo();

                PrettyPrinterConfiguration codePrinterConfig = new PrettyPrinterConfiguration();
                codePrinterConfig.setPrintComments(false);
                method.code = n.toString(codePrinterConfig);
                method.name = n.getNameAsString();
                if (n.getRange().isPresent()) {
                    method.lineCount = n.getRange().get().getLineCount();
                } else {
                    method.lineCount = 0;
                }
                if (n.getComment().isPresent()) {
                    method.comment = n.getComment().get().toString();
                } else {
                    method.comment = null;
                }
                LinkedList<Comment> containedComments = (LinkedList<Comment>) n.getAllContainedComments();
                method.commentsInMethod = new String[containedComments.size()];
                for (int i = 0; i < containedComments.size(); ++i) {
                    method.commentsInMethod[i] = containedComments.get(i).toString();
                }

                method.maxIndentation = maxIndentation(method.code);

                arg.add(method);
                return;
            }
        }, this.methodInfo);
    }
}