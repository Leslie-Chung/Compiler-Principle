import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.IOException;
import java.util.Locale;
import java.io.FileWriter;
import java.io.IOException;
import java.io.BufferedWriter;
import java.util.Map;

public class Lexical {
    private String codeLine;
    private BufferedReader bufferedReader;
    private BufferedWriter bufferedWriter_token;
    private BufferedWriter bufferedWriter_symTable;
    private int index;  //当前代码行的指针
    private int line;  //当前行数
    private char ch;  //当前读到的字符
    private FileRW fileRW;
    private String token;   //当前token序列
    private String str;
    private Map map;

    private TypeCompare typeCompare;

    public Lexical(String srcFile) {
        codeLine = "";
        fileRW = new FileRW();
        typeCompare = new TypeCompare();
        bufferedReader = fileRW.readFile(srcFile + "src.txt");
        bufferedWriter_token = fileRW.getBufferedWriter(srcFile + "token.txt");
        bufferedWriter_symTable = fileRW.getBufferedWriter(srcFile + "SymbolTable.txt");
        index = 0;
        line = 0;
        token = "";
    }

    public void readCh() {   //读字符
        if (index >= codeLine.length()) {
            index++;
            ch = ' ';
            return;
        }
        ch = codeLine.charAt(index++);
    }

    public boolean isDigit(char ch) {
        if (ch <= '9' && ch >= '0') return true;
        return false;
    }

    public boolean isLetter(char ch) {
        if (ch <= 'z' && ch >= 'a') return true;
        else if (ch <= 'Z' && ch >= 'A') return true;
        else return false;
    }

    public void analyse() throws IOException {
        while ((codeLine = bufferedReader.readLine()) != null) {
            line++;
            index = 0;
            token = "";
            while (index < codeLine.length()) {
                tempJudge();
            }
        }
        fileRW.writeFileByMap(bufferedWriter_symTable, typeCompare.getSymbolTable());
        fileRW.endWriteFile(bufferedWriter_token);
    }

    public void judgeKey() {
        if (typeCompare.isKeyWord(token)) {
            typeCompare.getType(token.toUpperCase(Locale.ROOT));
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <" + token.toUpperCase(Locale.ROOT) + ",_>";
            fileRW.writeFile(bufferedWriter_token, str);
            token = "";
        }
    }

    public void judgeID() {
        if (token == "") return;
        typeCompare.getType("ID");
        str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ID," + token + ">";
        fileRW.writeFile(bufferedWriter_token, str);
        token = "";
    }

    public void getKeyOrID() {
        token += ch;
        readCh();
        while (isLetter(ch) || isDigit(ch) || ch == '_') {
            token += ch;
            readCh();
        }
        index--;
        judgeKey();
        judgeID();
    }

    public int countDot(String token) {
        int coun = 0;
        for (int i = 0; i < token.length(); i++)
            if (token.charAt(i) == '.') coun++;
        return coun;
    }

    public void judgeFLOAT() {
        if (!token.contains(".")) {
            judgeINT();
            return;
        }
        int dot = countDot(token);
        if (dot == 1) {
            typeCompare.getType("FLONUM");
            if (token.charAt(0) == '.') {
                token = "0" + token;
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <FLOATDIGIT," + token + ">";
                fileRW.writeFile(bufferedWriter_token, str);
                token = "";
            } else if (token.charAt(token.length() - 1) == '.') {
                token = token + "0";
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <FLOATDIGIT," + token + ">";
                fileRW.writeFile(bufferedWriter_token, str);
                token = "";
            } else {
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <FLOATDIGIT," + token + ">";
                fileRW.writeFile(bufferedWriter_token, str);
                token = "";
            }
        } else {
            typeCompare.getType("ERROR");
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR," + token + ">";
            fileRW.writeFile(bufferedWriter_token, str);
            token = "";
        }

    }

    public void judgeDIGIT() {
        if (token.equals(".")) {
            typeCompare.getType("ERROR");
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR," + token + ">";
            fileRW.writeFile(bufferedWriter_token, str);
            token = "";
            return;
        }
        judgeFLOAT();
    }

    public void getDigit() {
        while (isDigit(ch) || ch == '.') {
            token += ch;
            readCh();
        }
        index--;
        judgeDIGIT();
    }

    public void getSe() {
        if(ch == '#'){
            token += ch;
            readCh();
            while (index <= codeLine.length()) {
                token += ch;
                readCh();
            }
            if(token.contains("include") || token.contains("define")){
                judgeSe();
            }
            else{
                judgeStrap();
            }
            return;
        }
        if(ch == '<'){
            getOp();
            return;
        }
        token += ch;
        judgeSe();
    }

    public void getOp() {
        token += ch;
        if(ch == '/'){//可能是 //，或者/*
            readCh();
            if(ch == '/'){
                token += ch;
                judgeSe();
                while (index <= codeLine.length()) {
                    readCh();
                    token += ch;
                }
                typeCompare.getType("STR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <String,_>";
                fileRW.writeFile(bufferedWriter_token, str);
                return;
            }
            else if(ch == '*'){
                token += ch;
                judgeSe();
                while (index <= codeLine.length()) {
                    readCh();
                    token += ch;

                    if(token.length() >= 2 && token.charAt(token.length() - 2) == '*' && ch == '/'){ // 注释结束
                        token = token.substring(0, token.length() - 2);
                        index -= 2;
                        break;
                    }
                }
                typeCompare.getType("STR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <String,_>";
                fileRW.writeFile(bufferedWriter_token, str);
                token = "";
                return;
            }
            else {
                index--;
            }
        }
        else if(ch == '*'){
            readCh();
            if(ch == '/'){
                token += ch;
                judgeSe();
                return;
            }
        }
        readCh();
        token += ch;
        readCh();
        token += ch; // 运算符最大长度为3
        if (!typeCompare.isOp(token)) {
            token = token.substring(0, 2);
            index--;
            if (!typeCompare.isOp(token)) {
                token = token.substring(0, 1);
                index--;
            }
        }
        judgeOp();
    }

    public void getChar() {
        token += ch;
        readCh();
        while (ch != '\'') {
            token += ch;
            if (ch == '\\') {
                readCh();
                token += ch;
            }
            readCh();
            if (index >= codeLine.length()) break;
        }
        token += ch;
        judgeChar();
    }

    public void getString() {
        token += ch;
        readCh();
        while (ch != '"') {
            token += ch;
            if (ch == '\\') {
                readCh();
                token += ch;
            }
            readCh();
            if (index >= codeLine.length()) break;
        }
        token += ch;
        judgeString();
    }

    public void tempJudge() {
        readCh();
        if (isLetter(ch) || ch == '_') {
            getKeyOrID();
        } else if (isDigit(ch) || ch == '.') {
            getDigit();
        } else if (typeCompare.isSe(Character.toString(ch))) { // 特殊情况：宏、<>
            getSe();
        } else if (typeCompare.isOp(Character.toString(ch))) {
            getOp();
        } else if (ch == '\'') {
            getChar();
        } else if (ch == '"') {
            getString();
        } else if (ch != ' ' && ch != '\t') {
            token += ch;
            judgeStrap();
        }
    }

    public void judgeINT() {
        typeCompare.getType("INTNUM");
        str = "<" + String.valueOf(line) + ">" + "  " + token + "  <INTEGER," + token + ">";
        fileRW.writeFile(bufferedWriter_token, str);
        token = "";
    }

    public void judgeSe() {
        token = token.replaceAll(" +","");
        typeCompare.getType(typeCompare.getSeMap().get(token));
        str = "<" + String.valueOf(line) + ">" + "  " + token + "  <" + typeCompare.getSeMap().get(token) + ",_>";
        fileRW.writeFile(bufferedWriter_token, str);
        token = "";
    }

    public void judgeOp() {
        typeCompare.getType(typeCompare.getOpMap().get(token));
        str = "<" + String.valueOf(line) + ">" + "  " + token + "  <" + typeCompare.getOpMap().get(token) + ",_>";
        fileRW.writeFile(bufferedWriter_token, str);
        token = "";
    }

    public void judgeStrap() {
        typeCompare.getType("ERROR");
        str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR,_>";
        fileRW.writeFile(bufferedWriter_token, str);
        token = "";
    }

    public void judgeChar() {
        if (token.length() == 3) {
            if (token.charAt(0) == '\'' && token.charAt(2) == '\'') {
                typeCompare.getType("SINGLECHAR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <CHAR," + token + ">";
                fileRW.writeFile(bufferedWriter_token, str);
            } else {
                typeCompare.getType("ERROR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR,_>";
                fileRW.writeFile(bufferedWriter_token, str);
            }
        } else if (typeCompare.isTransChar(token)) {
            typeCompare.getType("SINGLECHAR");
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <CHAR," + token + ">";
            fileRW.writeFile(bufferedWriter_token, str);
        } else {
            typeCompare.getType("ERROR");
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR,_>";
            fileRW.writeFile(bufferedWriter_token, str);
        }
        token = "";
    }

    public void judgeString() {
        if (token.charAt(0) == '"' && token.charAt(token.length() - 1) == '"') {
            if (typeCompare.isTransString(token)) {
                typeCompare.getType("STR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <String,_>";
                fileRW.writeFile(bufferedWriter_token, str);
            } else {
                typeCompare.getType("ERROR");
                str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR,_>";
                fileRW.writeFile(bufferedWriter_token, str);
            }
        } else {
            typeCompare.getType("ERROR");
            str = "<" + String.valueOf(line) + ">" + "  " + token + "  <ERROR,_>";
            fileRW.writeFile(bufferedWriter_token, str);
        }
        token = "";
    }
}

