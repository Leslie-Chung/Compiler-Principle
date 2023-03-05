import java.lang.reflect.Field;
import java.util.*;

public class TypeCompare {
    private static final List<String> keyword = new ArrayList(Arrays.asList(
            "short", "int", "long", "auto", "float", "double", "char",
            "struct", "union", "enum", "typedef", "const", "unsigned", "signed",
            "extern", "register", "static", "volatile", "void", "if",
            "else", "switch", "case", "for", "do", "while",
            "goto", "continue", "break", "default", "sizeof", "return", "true", "false"));

    private static final List<String> se = new ArrayList(Arrays.asList(
            "(", ")", "{", "}", "[", "]", ",", ";",
            "<", ">", "#", "/*", "*/", "//"
    ));

    private static final List<String> op = new ArrayList(Arrays.asList(
            "->", ".", "!", "~", "++", "--", "+", "-", "*", "&",
            "/", "%",
            "<<", ">>", "<", "<=", ">", ">=", "==", "!=", "^", "|",
            "&&", "||", "?:", "=", "+=", "-=", "*=", "/=", "%=", "&=", "^=", "|=", "<<=", ">>="
    ));

    private static final List<String> trans = new ArrayList(Arrays.asList(
            "\\a", "\\b", "\\f", "\\n", "\\r", "\\t", "\\v", "\\", "\\'", "\\\"", "\\\\"
    ));

    private Map<Integer, String> map;
    private Map<String, String> seMap;
    private Map<String, String> opMap;

    public TypeCompare() {
        map = new HashMap<>();
        opMap = new HashMap<>();
        seMap = new HashMap<>();
        setOpMap(opMap);
        setSeMap(seMap);
    }

    public boolean isKeyWord(String str) {
        int pos = keyword.indexOf(str);
        return pos != -1;
    }

    public boolean isSe(String str) {
        int pos = se.indexOf(str);
        return pos != -1;
    }

    public boolean isOp(String str) {
        int pos = op.indexOf(str);
        return pos != -1;
    }

    public int getType(String type) {
        Field[] fields = SymbolTable.class.getDeclaredFields();
        for (Field field : fields) {
            if (field.getName().equals(type)) {
                try {
                    Integer tmp = (Integer) field.get(new SymbolTable());
                    addMap(tmp, type);
                    return tmp;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
        return -1;
    }

    public boolean isTransChar(String token) {
        String str = token.substring(1, token.length() - 1);
        int pos = trans.indexOf(str);
        return pos != -1;
    }

    public boolean isTrans(String token) {
        int pos = trans.indexOf(token);
        return pos != -1;
    }

    public boolean isTransString(String token) {
        String str = token.substring(1, token.length() - 1);
        if (str.charAt(str.length() - 1) == '\\') return false;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == '\\') {
                char ch = str.charAt(i);
                i++;
                String temp = "";
                temp = temp + ch + str.charAt(i);
                if (!isTrans(temp)) return false;
            }
        }
        return true;
    }

    public Map<String, String> getOpMap() {
        return this.opMap;
    }

    public Map<String, String> getSeMap() {
        return this.seMap;
    }

    public void addMap(Integer key, String value) {
        if (!map.containsKey(key))
            map.put(key, value);
    }

    public Map<Integer, String> getSymbolTable() {
        if (map == null || map.isEmpty()) {
            return null;
        }
        Map<Integer, String> sortedMap = new TreeMap<Integer, String>(new Comparator<Integer>() {
            public int compare(Integer key1, Integer key2) {
                return key1 - key2;
            }
        });
        sortedMap.putAll(map);
        return sortedMap;
    }

    public void setOpMap(Map<String, String> map) {
        map.put("->", "ARROWHEAD");
        map.put(".", "POINT");
        map.put("!", "NOT");
        map.put("~", "CPL");
        map.put("++", "PP");
        map.put("--", "MM");
//        map.put("+", "POSITIVE");
//        map.put("-", "NEGATIVE");
//        map.put("*", "READADD");
//        map.put("&", "GETADD");
        map.put("*", "MUL");
        map.put("/", "DIV");
        map.put("%", "REMAINDER");
        map.put("+", "PLUS");
        map.put("-", "SUB");
        map.put("<<", "SHL");
        map.put(">>", "SHR");
        map.put("<", "LT");
        map.put("<=", "LET");
        map.put(">", "BT");
        map.put(">=", "BET");
        map.put("==", "EQ");
        map.put("!=", "NEQ");
        map.put("&", "SINGLEAND");
        map.put("^", "EXCLUSIVEOR");
        map.put("|", "SINGLEOR");
        map.put("&&", "DOUBLEAND");
        map.put("||", "DOUBLEOR");
        map.put("?:", "TRIPLE");
        map.put("=", "ASSIGN");
        map.put("+=", "PLUSE");
        map.put("-=", "MINE");
        map.put("*=", "MULE");
        map.put("/=", "DIVE");
        map.put("%=", "REMAINDERE");
        map.put("&=", "SINGLEANDE");
        map.put("^=", "EXCLUSIVEORE");
        map.put("|=", "SINGLEORE");
        map.put("<<=", "SHLE");
        map.put(">>=", "SHRE");
    }

    public void setSeMap(Map<String, String> map){
        map.put("(", "OPENPARENTHESIS");
        map.put(")", "CLOSEPARENTHESIS");
        map.put("{", "OPENBRACE");
        map.put("}", "CLOSEBRACE");
        map.put("[", "OPENBRACKETS");
        map.put("]", "CLOSEBRACKETS");
        map.put("<", "OPENANGLE");
        map.put(">", "CLOSEANGLE");
        map.put("#", "POUND");
        map.put("/*", "OPENBLOCKCOMMENT");
        map.put("*/", "CLOSEBLOCKCOMMENT");
        map.put("//", "LINECOMMENT");
        map.put("#include", "MACRO");
        map.put("#define", "MACRO");
    }
}
