/**
 * 符号表，此类为关键词，标识符，运算符，边界符，常数等进行种类编码
 */
public class SymbolTable {
    /**
    关键字
     */
    public static final int SHORT = 1;
    public static final int INT = 2;
    public static final int LONG = 3;
    public static final int AUTO = 4;
    public static final int FLOAT = 5;
    public static final int DOUBLE = 6;
    public static final int CHAR = 7;
    public static final int STRUCT = 8;
    public static final int UNION = 9;
    public static final int ENUM = 10;
    public static final int TYPEDEF = 11;
    public static final int CONST = 12;
    public static final int UNSIGNED = 13;
    public static final int SIGNED = 14;
    public static final int EXTERN = 15;
    public static final int REGISTER = 16;
    public static final int STATIC = 17;
    public static final int VOLATILE = 18;
    public static final int VOID = 19;
    public static final int IF = 20;
    public static final int ELSE = 21;
    public static final int SWITCH = 22;
    public static final int CASE = 23;
    public static final int FOR = 24;
    public static final int DO = 25;
    public static final int WHILE = 26;
    public static final int GOTO = 27;
    public static final int CONTINUE = 28;
    public static final int BREAK = 29;
    public static final int DEFAULT = 30;
    public static final int SIZEOF = 31;
    public static final int RETURN = 32;
    public static final int TRUE = 33;
    public static final int FALSE = 34;
    /**
    运算符
     */
    public static final int ARROWHEAD = 100; // ->
    public static final int POINT = 101; // .
    public static final int NOT = 102; // ！
    public static final int CPL = 102; // 按位取反
    public static final int PP = 103; // ++
    public static final int MM = 104; // --
    public static final int POSITIVE = 105; // -
    public static final int NEGATIVE = 106; // +
    public static final int READADD = 107; // 读地址*
    public static final int GETADD = 108; // 取地址&
    public static final int MUL = 109; // *
    public static final int DIV = 110; // /
    public static final int REMAINDER = 111;  // %
    public static final int PLUS = 112; // +
    public static final int SUB = 113; // -
    public static final int SHL = 113; // <<
    public static final int SHR = 113; // >>
    public static final int LT = 114;  //小于
    public static final int LET = 115; //小于等于
    public static final int BT = 116;  //大于
    public static final int BET = 117; //大于等于
    public static final int EQ = 118;  //等于==
    public static final int NEQ = 119; //不等号 !=
    public static final int SINGLEAND = 120; // 按位与&
    public static final int EXCLUSIVEOR = 121; // 按位异或^
    public static final int SINGLEOR = 122; // 按位或|
    public static final int DOUBLEAND = 123; //条件与&&
    public static final int DOUBLECOR = 124; //条件或||
    public static final int TRIPLE = 125; // ?:
    public static final int ASSIGN = 126;  // 赋值=
    public static final int PLUSE = 127; // +=
    public static final int MINE = 128; // -=
    public static final int MULE = 129; // *=
    public static final int DIVE = 130; // /=
    public static final int REMAINDERE = 131; // %=
    public static final int SINGLEANDE = 132; // &=
    public static final int EXCLUSIVEORE = 133; // ^=
    public static final int SINGLEORE = 134; // |=
    public static final int SHLE = 135; // <<=
    public static final int SHRE = 136; // >>=

    /**
     * 界符
     */
    public static final int OPENPARENTHESIS = 200; // (
    public static final int CLOSEPARENTHESIS = 201; // )
    public static final int OPENBRACE = 202; // {
    public static final int CLOSEBRACE = 203; // }
    public static final int OPENBRACKETS = 204; // [
    public static final int CLOSEBRACKETS = 205; // ]
    public static final int OPENANGLE = 206; // <
    public static final int CLOSEANGLE = 207; // >
    public static final int POUND = 208; // #
    public static final int OPENBLOCKCOMMENT = 209; // /*
    public static final int CLOSEBLOCKCOMMENT = 210; // */
    public static final int LINECOMMENT = 211; // //
    public static final int MACRO = 212; // 宏定义


    public static final int ID = 301;    //标识符


    /**
     * 常数
     */
    public static final int INTNUM = 401;  //整数
    public static final int FLOATNUM = 402;  //浮点数
    public static final int SINGLECHAR = 403; //字符
    public static final int STR = 404; //字符串
    //错误字符
    public static final int ERROR = -1;
}
