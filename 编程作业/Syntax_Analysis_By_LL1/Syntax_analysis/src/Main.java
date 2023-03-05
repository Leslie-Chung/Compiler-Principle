import com.SyntaxAnalysis.SyntaxAnalysisLL1;

public class Main
{
    public static void main(String[] args)
    {
        SyntaxAnalysisLL1 LL1 = new SyntaxAnalysisLL1(System.getProperty("user.dir")+"\\src\\com\\Grammars\\grammar.txt");
        LL1.printGrammarRules();
        String Sentence = LL1.canBeAccepted("a--a((a))") ? "给定的表达式能被识别！" : "给定的表达式不符合产生式的要求，无法识别！";
        LL1.printLoggingInfo();
        LL1.savePredictionTableToPicture();
        System.out.println(Sentence);
    }
}
