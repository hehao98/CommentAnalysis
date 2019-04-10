
/**
 * Take a piece of java code as input, parse it into Abstract Syntax Tree
 * Generate function and comment pairs
 * 
 * @author He, Hao
 */

import com.google.gson.Gson;

public class JavaCode {
    public String code;

    public JavaCode(String code) {
        this.code = code;
    }

    public String toJson() {
        Gson gson = new Gson();
        return gson.toJson(this);
    }
}