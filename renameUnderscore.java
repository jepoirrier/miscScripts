/*
 * RenameUnderscore list all files in the directory and rename files starting
 * with the underscore character ("_"). Useful for photos from my Canon camera
 * where photos taken in auto modes are labeled "IMG_xxx.JPG" and photos taken
 * in manual modes are labeled "_MG_yyy.JPG" with yyy = xxx + 1 (renaming thus
 * allows sorting on filename).
 * http://www.poirrier.be/
 * RENAME it to Main.java before compiling
 */

package renameundescore;

import java.io.File;

/**
 * Main class
 * @author jepoirrier
 */
public class Main {
    
    private static File[] myFileList;
    private static File myFile;
    private static String aFile;
    private static boolean result;
    
    private static String currentDir = ".";
    
    /**
     * main & only function :-)
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        myFile = new File(currentDir);
        myFileList = myFile.listFiles();
        
        for(File f: myFileList) {
            if(f.isFile()) {
                aFile = f.toString();
                if(aFile.charAt(2) == '_' && aFile.endsWith(".JPG")) {
                    result = f.renameTo(new File(aFile.replaceFirst("_", "I")));
                    if(result == false)
                        System.err.println("Error renaming: " + aFile);
                }
            }
        }
    }
}
