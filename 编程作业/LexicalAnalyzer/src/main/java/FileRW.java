
import javax.annotation.Resource;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.BufferedWriter;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/**
 * 该类负责将源代码文件读入缓冲区
 * 也可以将生成的token序列和符号表存入写入文件
 */
@Resource(name = "FileRW")
public class FileRW {
    public BufferedReader readFile(String filename){
        try {
            FileReader fileReader = new FileReader(filename);
            BufferedReader br = new BufferedReader(fileReader);
            return br;
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }

    public BufferedWriter getBufferedWriter(String filename) {
        try {
            File file = new File(filename);
            if(!file.exists()) {
                file.createNewFile();
            }
            FileWriter fileWriter = new FileWriter(file.getAbsoluteFile());
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
            return bufferedWriter;
        }catch(IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void writeFile(BufferedWriter bufferedWriter, String str) {
        try {
            bufferedWriter.write(str + "\n");
            bufferedWriter.flush();
        }catch(IOException e) {
            e.printStackTrace();
        }
    }

    public void endWriteFile(BufferedWriter bufferedWriter) {
        try {
            bufferedWriter.close();
        }catch(IOException e) {
            e.printStackTrace();
        }
    }

    public void writeFileByMap(BufferedWriter bufferedWriter, Map<Integer, String> map) {
        String str = String.format("%10s", "Symbol") + " | " + String.format("%8s", "Number");
        writeFile(bufferedWriter, str);
        Set<Map.Entry<Integer, String>> entrySet = map.entrySet();
        Iterator<Map.Entry<Integer, String>> it = entrySet.iterator();
        while(it.hasNext()){
            Map.Entry<Integer, String> me = it.next();
            Integer key = me.getKey();
            String value = me.getValue();
            str = String.format("%10s", value) + " | " + String.format("%8s", key.toString());
            writeFile(bufferedWriter, str);
        }
    }
}