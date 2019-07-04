import java.util.*;

public class Word extends Object
{
  public String[] words;
  public String text;

  public Word ( String wordString ) {
    text = "";

    wordString = wordString.substring(1);
    StringTokenizer st = new StringTokenizer(wordString, "~");
    words = new String[st.countTokens()];
    int i = 0;
    while(st.hasMoreTokens())
      words[i++] = st.nextToken();
  }

  public void addLine ( String str ) {
    text = text + "\n"+str;
  }

  public String toString ( ) {
    return "Word["+words+","+text+"]";
  }
  

}


