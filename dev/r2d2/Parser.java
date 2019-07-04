import java.util.*;
import java.io.*;

public class Parser extends Object {

  String filename;
  Vector vec;

  public Parser ( String filename ) {
    this.filename = filename;
    this.vec = new Vector ( );
  }

  public Vector parse ( )
  {
    try {
      FileReader fr = new FileReader ( new File ( this.filename ) );
      LineNumberReader lnr = new LineNumberReader ( fr );
      Word current=null;
      
      while ( true ) {
	
	String str = lnr.readLine ( );
	if ( str == null )
	  break;

	if ( str.length () > 0 ) {
	  if ( str.charAt(0) == '#' ) {
	    current = new Word ( str );
	  }

	  else if ( str.charAt(0) == '@' ) {
	    vec.addElement ( current );
	    current = null;
	  }
	  
	  else 
	    current.addLine ( str );
	}
	else
	  current.addLine ( str );

      }

    }
    catch (Exception ex) {
      System.out.println ( "Det gick inge vidare." );
      System.out.println ( ex );
      ex.printStackTrace ( );
      return null;
    }
    return vec;

  }
  
}
