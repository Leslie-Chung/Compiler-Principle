import java.io.IOException;

public class Starter {
    public static void main(String[] args) throws IOException {
        Lexical lexical = new Lexical("src/files/");
        lexical.analyse();
    }
}
